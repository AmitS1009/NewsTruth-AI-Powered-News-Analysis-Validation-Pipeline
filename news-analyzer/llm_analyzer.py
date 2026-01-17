import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class LLMAnalyzer:
    def __init__(self, api_key=None, model_name='gemini-1.5-flash-latest'):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables.")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(model_name)

    def analyze_article(self, text):
        """
        Analyzes the article text for gist, sentiment, and tone.
        
        Args:
            text (str): Article text.
        
        Returns:
            dict: {gist, sentiment, tone} or None if failed.
        """
        if not text:
            return None

        prompt = f"""
        Analyze the following news article. Return ONLY a valid JSON object with the following keys:
        1. "gist": A 1-2 sentence summary.
        2. "sentiment": One of [positive, negative, neutral].
        3. "tone": One word describing the tone (e.g., urgent, analytical, satirical, balanced).

        Article Text:
        {text[:8000]} 
        """
        # Truncate to avoid context window issues, though 1.5 flash has large window.

        try:
            response = self.model.generate_content(prompt)
            raw_text = response.text
            
            # Clean up markdown code blocks if present
            cleaned_text = raw_text.replace('```json', '').replace('```', '').strip()
            
            analysis = json.loads(cleaned_text)
            return analysis
            
        except json.JSONDecodeError:
            print(f"Failed to parse JSON from Gemini response: {raw_text}")
            return default_analysis_error()
        except Exception as e:
            print(f"Error calling Gemini API: {e}")
            return default_analysis_error()

def default_analysis_error():
    return {
        "gist": "Analysis failed.",
        "sentiment": "neutral",
        "tone": "unknown"
    }

