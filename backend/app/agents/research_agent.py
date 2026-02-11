"""
Research Agent - Finds potential leads
"""

from typing import List, Dict, Any
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, END
from app.config import settings
from app.tools.web_scraper import web_scraper
from app.utils.gemini_client import gemini_client


class ResearchAgentState(Dict[str, Any]):
    """State for research agent"""
    pass


class ResearchAgent:
    """Agent for researching and finding leads"""
    
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model=settings.GEMINI_MODEL,
            google_api_key=settings.GEMINI_API_KEY,
            temperature=0.3,
        )
    
    async def generate_search_queries(self, state: ResearchAgentState) -> ResearchAgentState:
        """Generate search queries based on criteria"""
        prompt = f"""
Generate 5 specific search queries to find companies matching these criteria:
- Industry: {state.get('industry', 'any')}
- Location: {state.get('location', 'any')}
- Company Size: {state.get('company_size', 'any')}

Return as JSON array of strings.
Example: ["SaaS companies in San Francisco", "fintech startups in NYC"]
"""
        
        try:
            result = await gemini_client.generate_json(prompt)
            # Handle None or invalid result
            if result and isinstance(result, list):
                state["search_queries"] = result
            else:
                state["search_queries"] = []
        except Exception as e:
            state["errors"] = state.get("errors", []) + [str(e)]
            state["search_queries"] = []
        
        return state
    
    async def search_companies(self, state: ResearchAgentState) -> ResearchAgentState:
        """Search for companies using generated queries"""
        from app.config import settings
        
        results = []
        queries = state.get("search_queries", [])
        
        # Use real search if enabled, otherwise mock
        for query in queries[:3]:
            if settings.USE_REAL_SEARCH:
                # Use real Google search via SerpAPI
                search_results = await web_scraper.google_search_real(query, num_results=5)
            else:
                # Use mock search for testing
                search_results = await web_scraper.google_search_mock(query, num_results=5)
            
            # Handle None or invalid results
            if not search_results:
                continue
            for company in search_results:
                # Skip None or invalid company data
                if not company or not isinstance(company, dict):
                    continue
                results.append({
                    "company_name": company.get("title", "Unknown Company"),
                    "website": company.get("url", ""),
                    "domain": web_scraper.user_agent,  # Placeholder
                    "industry": state.get("industry", "Technology"),
                    "location": state.get("location", "USA"),
                    "source": "google_search_real" if settings.USE_REAL_SEARCH else "google_search_mock",
                    "description": company.get("snippet", "")
                })
        
        state["results"] = results[:settings.MAX_RESEARCH_RESULTS]
        return state
    
    async def enrich_companies(self, state: ResearchAgentState) -> ResearchAgentState:
        """Enrich company data with additional information"""
        enriched_results = []
        
        for company in state.get("results", [])[:10]:  # Limit to first 10 for speed
            try:
                # Try to scrape company website
                if company.get("website"):
                    info = await web_scraper.extract_company_info(company["website"])
                    company.update(info)
            except Exception as e:
                company["enrichment_error"] = str(e)
            
            enriched_results.append(company)
        
        state["results"] = enriched_results
        return state
    
    def create_graph(self) -> StateGraph:
        """Create the research workflow graph"""
        workflow = StateGraph(ResearchAgentState)
        
        # Add nodes
        workflow.add_node("generate_queries", self.generate_search_queries)
        workflow.add_node("search", self.search_companies)
        workflow.add_node("enrich", self.enrich_companies)
        
        # Add edges
        workflow.set_entry_point("generate_queries")
        workflow.add_edge("generate_queries", "search")
        workflow.add_edge("search", "enrich")
        workflow.add_edge("enrich", END)
        
        return workflow.compile()
    
    async def run(
        self,
        industry: str,
        location: str = "",
        company_size: str = ""
    ) -> List[Dict]:
        """Run research agent"""
        graph = self.create_graph()
        
        initial_state: ResearchAgentState = {
            "query": "",
            "industry": industry,
            "location": location,
            "company_size": company_size,
            "results": [],
            "errors": [],
        }
        
        try:
            final_state = await graph.ainvoke(initial_state)
            
            # Handle None or invalid final_state
            if final_state is None:
                print("WARNING Warning: graph.ainvoke() returned None")
                return []
            
            return final_state.get("results", [])
        except Exception as e:
            print(f"ERROR Research agent error: {str(e)}")
            return []


# Global instance
research_agent = ResearchAgent()