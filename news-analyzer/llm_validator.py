import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

class LLMValidator:
    BASE_URL = "https://openrouter.ai/api/v1/chat/completions"

    def __init__(self, api_key=None, model="mistralai/mistral-7b-instruct"):
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY")
        self.model = model
        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY not found in environment variables.")

    def validate_analysis(self, article, analysis):
        """
        Validates the analysis against the article content.
        
        Args:
            article (dict): Article details including 'content' or 'description'.
            analysis (dict): The result from LLMAnalyzer.
        
        Returns:
            dict: {is_correct, corrections, reasoning}
        """
        if not article or not analysis:
            return default_validation_error()

        # Construct a validation prompt
        article_text = article.get('content', '') or article.get('description', '')
        
        prompt = f"""
        You are a fact-checker. 
        
        Article Text:
        {article_text[:4000]}
        
        Proposed Analysis:
        Gist: {analysis.get('gist')}
        Sentiment: {analysis.get('sentiment')}
        Tone: {analysis.get('tone')}
        
        Task:
        Does this analysis accurately reflect the article? 
        Return ONLY a JSON object with:
        1. "is_correct": boolean
        2. "corrections": string (if any errors, otherwise "None")
        3. "reasoning": string (why you agree or disagree, cite specific words from text)
        """

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self.model,
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }

        try:
            response = requests.post(self.BASE_URL, headers=headers, json=data, timeout=15)
            response.raise_for_status()
            
            result_json = response.json()
            content = result_json['choices'][0]['message']['content']
            
            # Clean markdown if present
            cleaned_content = content.replace('```json', '').replace('```', '').strip()
            return json.loads(cleaned_content)

        except requests.exceptions.RequestException as e:
            print(f"Network error validating with OpenRouter: {e}")
            return default_validation_error()
        except json.JSONDecodeError:
            print(f"Failed to parse JSON from OpenRouter: {content}")
            return default_validation_error()
        except Exception as e:
            print(f"Unexpected error in validator: {e}")
            return default_validation_error()

def default_validation_error():
    return {
        "is_correct": False,
        "corrections": "Validation Refused",
        "reasoning": "Error in validation process or no response."
    }

