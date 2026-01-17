import unittest
from unittest.mock import patch, MagicMock
from news_fetcher import NewsFetcher
import os

class TestNewsFetcher(unittest.TestCase):
    
    def setUp(self):
        os.environ["NEWSAPI_KEY"] = "test_key"

    def test_init_raises_error_without_key(self):
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(ValueError):
                NewsFetcher(api_key=None)

    @patch("news_fetcher.requests.get")
    def test_fetch_articles_success(self, mock_get):
        # Mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "status": "ok",
            "articles": [
                {
                    "title": "Test Hit",
                    "content": "Some content", 
                    "description": "Some desc",
                    "source": {"name": "Test Source"}, 
                    "publishedAt": "2023-01-01",
                    "url": "http://test.com"
                },
                {
                    "title": "[Removed]",
                    "content": "Nothing",
                    "description": "Gone"
                }
            ]
        }
        mock_get.return_value = mock_response

        fetcher = NewsFetcher()
        articles = fetcher.fetch_articles()
        
        self.assertEqual(len(articles), 1)
        self.assertEqual(articles[0]['title'], "Test Hit")
        self.assertEqual(articles[0]['source'], "Test Source")

    @patch("news_fetcher.requests.get")
    def test_fetch_articles_api_error(self, mock_get):
        # Mock response
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.raise_for_status.side_effect = Exception("API Key Missing")
        mock_get.return_value = mock_response

        fetcher = NewsFetcher()
        articles = fetcher.fetch_articles()
        
        self.assertEqual(articles, [])

if __name__ == "__main__":
    unittest.main()
