"""
Qualification Agent - Scores and qualifies leads
"""

from typing import Dict, Any
from app.utils.gemini_client import gemini_client
from app.config import settings


class QualificationAgent:
    """Agent for qualifying and scoring leads"""
    
    async def score_lead(self, lead_data: Dict[str, Any], criteria: Dict[str, Any]) -> Dict[str, Any]:
        """Score a lead based on qualification criteria"""
        prompt = f"""
You are a B2B lead qualification expert. Score this lead from 0.0 to 1.0.

LEAD INFORMATION:
- Company: {lead_data.get('company_name', 'Unknown')}
- Industry: {lead_data.get('industry', 'Unknown')}
- Size: {lead_data.get('company_size', 'Unknown')}
- Location: {lead_data.get('location', 'Unknown')}
- Description: {lead_data.get('description', 'No description')}

QUALIFICATION CRITERIA:
{criteria}

Provide a JSON response with:
{{
    "score": 0.0-1.0,
    "quality": "hot" | "warm" | "cold",
    "reasoning": "explanation",
    "fit_score": 0.0-1.0,
    "urgency_score": 0.0-1.0,
    "budget_likelihood": 0.0-1.0
}}

Scoring guide:
- 0.8-1.0: HOT - Perfect fit, high urgency, clear budget
- 0.6-0.8: WARM - Good fit, some urgency
- 0.0-0.6: COLD - Poor fit or low priority
"""
        
        try:
            result = await gemini_client.generate_json(prompt)
            
            # Handle None or invalid result
            if not result or not isinstance(result, dict):
                result = {}
            
            # Ensure score is within bounds
            score = max(0.0, min(1.0, result.get("score", 0.5)))
            
            # Determine quality based on score
            if score >= 0.8:
                quality = "hot"
            elif score >= 0.6:
                quality = "warm"
            else:
                quality = "cold"
            
            return {
                "score": score,
                "quality": quality,
                "reasoning": result.get("reasoning", ""),
                "fit_score": result.get("fit_score", 0.5),
                "urgency_score": result.get("urgency_score", 0.5),
                "budget_likelihood": result.get("budget_likelihood", 0.5),
            }
        except Exception as e:
            return {
                "score": 0.5,
                "quality": "warm",
                "reasoning": f"Error during qualification: {str(e)}",
                "fit_score": 0.5,
                "urgency_score": 0.5,
                "budget_likelihood": 0.5,
            }
    
    async def identify_pain_points(self, company_data: Dict[str, Any]) -> list[str]:
        """Identify potential pain points for a company"""
        prompt = f"""
Based on this company information, identify 3-5 potential business pain points:

Company: {company_data.get('company_name', 'Unknown')}
Industry: {company_data.get('industry', 'Unknown')}
Description: {company_data.get('description', 'No description')}

Return as JSON array of strings.
Example: ["manual data entry", "lack of automation", "scaling challenges"]
"""
        
        try:
            result = await gemini_client.generate_json(prompt)
            return result if isinstance(result, list) else []
        except:
            return []
    
    def is_qualified(self, score: float) -> bool:
        """Check if lead meets qualification threshold"""
        return score >= settings.QUALIFICATION_THRESHOLD


# Global instance
qualification_agent = QualificationAgent()