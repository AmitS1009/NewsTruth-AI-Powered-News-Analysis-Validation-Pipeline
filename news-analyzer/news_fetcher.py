import os
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class NewsFetcher:
    BASE_URL = "https://newsapi.org/v2/everything"

    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("NEWSAPI_KEY")
        if not self.api_key:
            raise ValueError("NEWSAPI_KEY not found in environment variables.")

    def fetch_articles(self, query="India politics", limit=15):
        """
        Fetches articles from NewsAPI.
        
        Args:
            query (str): Search query.
            limit (int): Number of articles to fetch (max 100).
        
        Returns:
            list: List of dictionaries containing article details.
        """
        params = {
            "q": query,
            "apiKey": self.api_key,
            "pageSize": limit,
            "language": "en",
            "sortBy": "publishedAt"
        }

        try:
            response = requests.get(self.BASE_URL, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            if data.get("status") != "ok":
                print(f"Error from NewsAPI: {data.get('message')}")
                return []

            articles = data.get("articles", [])
            cleaned_articles = []
            
            for art in articles:
                # Skip removed articles or empty content
                if art['title'] == "[Removed]" or not art.get('content') or not art.get('description'):
                    continue
                    
                cleaned_articles.append({
                    "title": art.get("title"),
                    "content": art.get("content"), # Note: NewsAPI free tier truncates content
                    "description": art.get("description"),
                    "source": art.get("source", {}).get("name"),
                    "date": art.get("publishedAt"),
                    "url": art.get("url")
                })
            
            print(f"Fetched {len(cleaned_articles)} articles for query '{query}'")
            return cleaned_articles

        except requests.exceptions.RequestException as e:
            print(f"Network error fetching news: {e}")
            return []
        except Exception as e:
            print(f"Unexpected error: {e}")
            return []

