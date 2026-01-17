import unittest
from unittest.mock import patch, MagicMock
from llm_validator import LLMValidator
import os
import json

class TestLLMValidator(unittest.TestCase):
    
    def setUp(self):
        os.environ["OPENROUTER_API_KEY"] = "test_router_key"

    def test_init_raises_error_without_key(self):
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(ValueError):
                LLMValidator(api_key=None)

    @patch("llm_validator.requests.post")
    def test_validate_analysis_success(self, mock_post):
        # Mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{
                "message": {
                    "content": '{"is_correct": true, "corrections": "None", "reasoning": "Matches text."}'
                }
            }]
        }
        mock_post.return_value = mock_response

        validator = LLMValidator()
        result = validator.validate_analysis({"content": "text"}, {"gist": "summary"})
        
        self.assertTrue(result['is_correct'])
        self.assertEqual(result['reasoning'], "Matches text.")

    @patch("llm_validator.requests.post")
    def test_validate_analysis_api_failure(self, mock_post):
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = Exception("API Error")
        mock_post.return_value = mock_response

        validator = LLMValidator()
        result = validator.validate_analysis({"content": "text"}, {"gist": "summary"})
        
        self.assertFalse(result['is_correct'])
        self.assertEqual(result['corrections'], "Validation Refused")

if __name__ == "__main__":
    unittest.main()
