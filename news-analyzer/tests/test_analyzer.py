import unittest
from unittest.mock import patch, MagicMock
from llm_analyzer import LLMAnalyzer
import os
import json

class TestLLMAnalyzer(unittest.TestCase):
    
    def setUp(self):
        os.environ["GEMINI_API_KEY"] = "test_gemini_key"

    def test_init_raises_error_without_key(self):
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(ValueError):
                LLMAnalyzer(api_key=None)

    @patch("llm_analyzer.genai.GenerativeModel")
    @patch("llm_analyzer.genai.configure")
    def test_analyze_article_success(self, mock_configure, mock_model_cls):
        # Mock model response
        mock_model_instance = MagicMock()
        mock_response = MagicMock()
        
        # Valid JSON response
        mock_response.text = '{"gist": "Summary", "sentiment": "neutral", "tone": "analytical"}'
        mock_model_instance.generate_content.return_value = mock_response
        mock_model_cls.return_value = mock_model_instance

        analyzer = LLMAnalyzer()
        result = analyzer.analyze_article("Some text")
        
        self.assertEqual(result['gist'], "Summary")
        self.assertEqual(result['sentiment'], "neutral")

    @patch("llm_analyzer.genai.GenerativeModel")
    @patch("llm_analyzer.genai.configure")
    def test_analyze_article_json_error(self, mock_configure, mock_model_cls):
        mock_model_instance = MagicMock()
        mock_response = MagicMock()
        
        # Invalid JSON
        mock_response.text = 'Not JSON'
        mock_model_instance.generate_content.return_value = mock_response
        mock_model_cls.return_value = mock_model_instance

        analyzer = LLMAnalyzer()
        result = analyzer.analyze_article("Some text")
        
        self.assertEqual(result['gist'], "Analysis failed.")

if __name__ == "__main__":
    unittest.main()
