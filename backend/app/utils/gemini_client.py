"""
Gemini API Client
"""

import google.generativeai as genai
from app.config import settings


class GeminiClient:
    """Wrapper for Google Gemini API"""
    
    def __init__(self):
        if settings.GEMINI_API_KEY:
            genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(settings.GEMINI_MODEL)
    
    async def generate(
        self,
        prompt: str,
        temperature: float = None,
        max_tokens: int = None
    ) -> str:
        """Generate text using Gemini"""
        try:
            response = await self.model.generate_content_async(
                prompt,
                generation_config=genai.GenerationConfig(
                    temperature=temperature or settings.GEMINI_TEMPERATURE,
                    max_output_tokens=max_tokens or settings.GEMINI_MAX_TOKENS,
                )
            )
            return response.text
        except Exception as e:
            raise Exception(f"Gemini API error: {str(e)}")
    
    async def generate_json(
        self,
        prompt: str,
        temperature: float = 0.3
    ) -> dict:
        """Generate JSON output"""
        import json
        
        full_prompt = f"{prompt}\n\nRespond ONLY with valid JSON, no markdown or explanations."
        
        response = await self.generate(full_prompt, temperature=temperature)
        
        # Clean markdown if present
        cleaned = response.strip()
        if cleaned.startswith("```json"):
            cleaned = cleaned[7:]
        if cleaned.startswith("```"):
            cleaned = cleaned[3:]
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]
        cleaned = cleaned.strip()
        
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError as e:
            raise Exception(f"Failed to parse JSON: {str(e)}")


# Global instance
gemini_client = GeminiClient()