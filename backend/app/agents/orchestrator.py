"""
Orchestrator Agent - Manages the full workflow
"""

from typing import Dict, Any, List
from langgraph.graph import StateGraph, END
from app.agents.research_agent import research_agent
from app.agents.qualification_agent import qualification_agent
from app.agents.personalization_agent import personalization_agent


class OrchestratorState(Dict[str, Any]):
    """State for orchestrator"""
    pass


class OrchestratorAgent:
    """Main orchestrator for the sales agent workflow"""
    
    async def research_step(self, state: OrchestratorState) -> OrchestratorState:
        """Research leads"""
        criteria = state.get("campaign_criteria", {})
        
        leads = await research_agent.run(
            industry=criteria.get("industry", ""),
            location=criteria.get("location", ""),
            company_size=criteria.get("company_size", "")
        )
        
        state["leads"] = leads
        return state
    
    async def qualification_step(self, state: OrchestratorState) -> OrchestratorState:
        """Qualify leads"""
        leads = state.get("leads", [])
        criteria = state.get("campaign_criteria", {})
        
        qualified_leads = []
        for lead in leads:
            score_result = await qualification_agent.score_lead(lead, criteria)
            lead["quality_score"] = score_result["score"]
            lead["quality"] = score_result["quality"]
            lead["qualification_reasoning"] = score_result["reasoning"]
            
            # Identify pain points
            pain_points = await qualification_agent.identify_pain_points(lead)
            lead["pain_points"] = pain_points
            
            if qualification_agent.is_qualified(score_result["score"]):
                qualified_leads.append(lead)
        
        state["qualified_leads"] = qualified_leads
        return state
    
    async def personalization_step(self, state: OrchestratorState) -> OrchestratorState:
        """Generate personalized emails"""
        leads = state.get("qualified_leads", [])
        template = state.get("email_template")
        
        for lead in leads:
            email_content = await personalization_agent.generate_email(
                lead_data=lead,
                template=template,
                email_type="initial"
            )
            lead["email_subject"] = email_content["subject"]
            lead["email_body"] = email_content["body"]
        
        state["qualified_leads"] = leads
        return state
    
    def create_graph(self) -> StateGraph:
        """Create orchestrator workflow graph"""
        workflow = StateGraph(OrchestratorState)
        
        # Add nodes
        workflow.add_node("research", self.research_step)
        workflow.add_node("qualify", self.qualification_step)
        workflow.add_node("personalize", self.personalization_step)
        
        # Add edges
        workflow.set_entry_point("research")
        workflow.add_edge("research", "qualify")
        workflow.add_edge("qualify", "personalize")
        workflow.add_edge("personalize", END)
        
        return workflow.compile()
    
    async def run_campaign(self, campaign_criteria: Dict[str, Any]) -> List[Dict]:
        """Run full campaign workflow"""
        graph = self.create_graph()
        
        initial_state: OrchestratorState = {
            "campaign_criteria": campaign_criteria,
            "email_template": campaign_criteria.get("email_template"),
            "leads": [],
            "qualified_leads": [],
        }
        
        try:
            final_state = await graph.ainvoke(initial_state)
            
            # Handle None or invalid final_state
            if final_state is None:
                print("WARNING Warning: orchestrator graph.ainvoke() returned None")
                return []
            
            return final_state.get("qualified_leads", [])
        except Exception as e:
            print(f"ERROR Orchestrator error: {str(e)}")
            import traceback
            traceback.print_exc()
            return []


# Global instance
orchestrator_agent = OrchestratorAgent()