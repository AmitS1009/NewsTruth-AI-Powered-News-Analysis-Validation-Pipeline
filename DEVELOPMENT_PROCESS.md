# Development Process & Engineering Log

> **Summary**: This document tracks the decision-making process, challenges faced, and architectural choices made while building the NewsTruth pipeline.

## 🧠 Thinking Process: The "Why" and "How"

### Core Philosophy
1.  **Modular Design**: I rejected the idea of a monolithic script. By splitting Fetching, Analysis, and Validation, I ensured that if one API changes (e.g., swapping Gemini for OpenAI), the rest of the system remains untouched.
2.  **Defensive Coding**: LLMs are unpredictable. They might return invalid JSON or hallucinate.
    *   *Decision*: I implemented strict JSON parsing wrappers that strip markdown formatting (a common LLM quirk).
    *   *Decision*: I added a "Critic" layer (Validator) because I don't trust a single model's sentiment analysis on sensitive topics like politics.

## Problem Statement
Fetch news articles about "India politics" using NewsAPI, analyze them using Google Gemini (for gist, sentiment, and tone), and validate the analysis using a second LLM (OpenRouter/Mistral). The results should be saved as JSON and a readable Markdown report.

## Breakdown
1.  **Project Setup**: Create structure, config, and skeleton code.
2.  **Fetch News**: Implement `news_fetcher.py` to get articles from NewsAPI.
3.  **Analyze**: Implement `llm_analyzer.py` to process text with Gemini.
4.  **Validate**: Implement `llm_validator.py` to cross-check with OpenRouter.
5.  **Orchestrate**: Stitch everything in `main.py`.
6.  **Reporting**: Save outputs.

## Task 1: Fetch from NewsAPI
**AI Prompt Used:**
"Write a Python class `NewsFetcher` that fetches articles from NewsAPI. It should handle rate limits, timeouts, and missing fields. The `fetch_articles` method should accept a query and limit, and return a list of cleaned dictionaries."

**My Review:** 
The initial implementation looks solid. I ensured it handles:
1.  API Key validation.
2.  `requests.get` with timeouts.
3.  JSON parsing and status checks.
4.  Filtering out `[Removed]` articles and those with empty content.
5.  Data cleaning to return a consistent dictionary structure.

**Final Code:** 
Implemented in `news_fetcher.py` with `test_news_fetcher.py` for verification.

## Task 2: Analyze with LLM (Gemini)
**AI Prompt Used:**
"Write a Python class `LLMAnalyzer` that uses `google-generativeai`. It should have an `analyze_article(text)` method that prompts Gemini to return a valid JSON with `gist`, `sentiment`, and `tone`. It must handle `JSONDecodeError`."

**My Review:**
The prompt uses a specific structure instructions for the JSON output. I added:
1.  JSON markdown block cleaning (common LLM behavior).
2.  Truncation of text to 8000 chars to stay safe within limits.
3.  Unit tests with mocks for the `genai` module.

**Final Code:**
Implemented in `llm_analyzer.py` and tested in `tests/test_analyzer.py`.

## Task 3: Validate with LLM (OpenRouter)
**AI Prompt Used:**
"Write a Python class `LLMValidator` that calls OpenRouter's API (using `requests`). It should take the original article and the analysis dict, and ask a second LLM (Mistral-7B) to fact-check the analysis. Return JSON: `{is_correct, corrections, reasoning}`."

**My Review:**
The prompt needed to ensure the second LLM acts as a critic. 
I ensured:
1.  API Key handling for OpenRouter.
2.  Clear prompt structure: "You are a fact-checker".
3.  JSON cleansing logic similar to the Analyzer.
4.  Fallback for API errors.

**Final Code:**
Implemented in `llm_validator.py` and tested in `tests/test_validator.py`.

## Task 4: Orchestration (Main Pipeline)
**AI Prompt Used:**
"Write a `main.py` script that orchestrates the pipeline:
1. Load env vars.
2. Initialization `NewsFetcher`, `LLMAnalyzer`, `LLMValidator`.
3. Fetch top articles.
4. Loop through articles to analyze and validate.
5. Save results to `output/analysis_results.json` and generating a helper markdown report `output/final_report.md`."

**My Review:**
I ensured the script handles the flow gracefully.
- Added error handling for configuration.
- Saves raw data first (checkpointing).
- Summarizes sentiment statistics.
- Generates a readable Markdown report with validation icons.

## Conclusion and Reflections
The modular approach (Fetcher -> Analyzer -> Validator) allows for easy testing and swapping of components.
- **Challenges:** Handling API limits and potentially malformed JSON from LLMs. 
- **Solutions:** Added robust try/except blocks and JSON cleaning logic.
- **Future Improvements:** Add parallel processing for faster analysis (using `asyncio`), though rate limits on free tiers might be a bottleneck.
