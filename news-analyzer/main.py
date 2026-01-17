import json
import os
import datetime
from dotenv import load_dotenv
from news_fetcher import NewsFetcher
from llm_analyzer import LLMAnalyzer
from llm_validator import LLMValidator

# Load environment variables
load_dotenv()

def main():
    print("=== News Analysis Pipeline Started ===")
    
    # Configuration
    QUERY = "India politics"
    LIMIT = 12 
    OUTPUT_DIR = "output"
    
    # Ensure output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Initialize Components
    try:
        fetcher = NewsFetcher()
        analyzer = LLMAnalyzer()
        validator = LLMValidator()
    except ValueError as e:
        print(f"Configuration Error: {e}")
        return

    # 1. Fetch News
    print(f"\n[Step 1] Fetching news for '{QUERY}'...")
    articles = fetcher.fetch_articles(query=QUERY, limit=LIMIT)
    
    if not articles:
        print("No articles found. Exiting.")
        return

    # Save raw articles
    with open(os.path.join(OUTPUT_DIR, "raw_articles.json"), "w", encoding='utf-8') as f:
        json.dump(articles, f, indent=4)

    # 2. Analyze and Validate
    print(f"\n[Step 2 & 3] Analyzing and Validating {len(articles)} articles...")
    
    results = []
    summary_stats = {"positive": 0, "negative": 0, "neutral": 0}

    for i, article in enumerate(articles, 1):
        print(f"Processing ({i}/{len(articles)}): {article['title'][:50]}...")
        
        # Analyze
        analysis = analyzer.analyze_article(article['content'] or article['description'])
        if not analysis:
            print(f"  - Analysis failed for article {i}")
            continue
            
        # Update stats
        sentiment = analysis.get('sentiment', 'neutral').lower()
        summary_stats[sentiment] = summary_stats.get(sentiment, 0) + 1

        # Validate
        validation = validator.validate_analysis(article, analysis)
        
        result_entry = {
            "article": article,
            "analysis": analysis,
            "validation": validation
        }
        results.append(result_entry)

    # Save results
    with open(os.path.join(OUTPUT_DIR, "analysis_results.json"), "w", encoding='utf-8') as f:
        json.dump(results, f, indent=4)

    # 3. Generate Report
    print(f"\n[Step 4] Generating Report...")
    generate_report(results, summary_stats, OUTPUT_DIR)
    
    print(f"\n=== Pipeline Completed. Check {OUTPUT_DIR}/final_report.md ===")

def generate_report(results, stats, output_dir):
    date_str = datetime.datetime.now().strftime("%Y-%m-%d")
    
    md_content = f"""# News Analysis Report
**Date:** {date_str}
**Articles Analyzed:** {len(results)}
**Source:** NewsAPI

## Summary
- Positive: {stats.get('positive', 0)} articles
- Negative: {stats.get('negative', 0)} articles
- Neutral: {stats.get('neutral', 0)} articles

## Detailed Analysis
"""

    for i, item in enumerate(results, 1):
        art = item['article']
        ana = item['analysis']
        val = item['validation']
        
        validation_icon = "✓" if val.get('is_correct') else "⚠"
        
        md_content += f"""
### Article {i}: "{art['title']}"
- **Source:** [{art['source']}]({art['url']})
- **Gist:** {ana.get('gist')}
- **LLM#1 Sentiment:** {ana.get('sentiment').capitalize()}
- **Tone:** {ana.get('tone')}
- **LLM#2 Validation:** {validation_icon} {val.get('is_correct')}
    - **Reasoning:** {val.get('reasoning')}
    - **Corrections:** {val.get('corrections')}

---
"""
    
    with open(os.path.join(output_dir, "final_report.md"), "w", encoding='utf-8') as f:
        f.write(md_content)

if __name__ == "__main__":
    main()
