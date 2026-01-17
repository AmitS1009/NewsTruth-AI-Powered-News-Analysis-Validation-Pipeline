# 🗞️ NewsTruth: AI-Powered News Analysis & Validation Pipeline

> **"Trust, but verify."** — This project implements a **Dual-LLM Architecture** to fetch, analyze, and fact-check political news in real-time.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)
![Gemini](https://img.shields.io/badge/Analysis-Google%20Gemini-orange?style=for-the-badge)
![Mistral](https://img.shields.io/badge/Validation-OpenRouter%20%2F%20Mistral-purple?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Operational-green?style=for-the-badge)

## 🚀 The Concept
In the age of AI hallucinations, a single model isn't enough. **NewsTruth** builds a self-correcting pipeline where:
1.  **The Analyst (Gemini)** reads the news and extracts sentiment, tone, and a gist.
2.  **The Critic (Mistral/OpenRouter)** reviews the Analyst's work against the source text to flag inconsistencies or bias.

This **Agentic Workflow** ensures higher reliability than standard "wrapper" scripts.

## 🏗️ Architecture
## 🏗️ Architecture
```mermaid
graph TD
    A[NewsAPI] -->|Raw Articles| B(NewsFetcher)
    B -->|Cleaned Text| C{LLM #1: Analyst}
    C -->|Gist & Sentiment| D{LLM #2: Critic}
    D -->|Validation| E[Final Report]
    
    subgraph "The Analyzer (Gemini)"
    C
    end
    
    subgraph "The Validator (OpenRouter)"
    D
    end

    %% High contrast styling
    style A fill:#2d3436,stroke:#fff,stroke-width:2px,color:#fff
    style B fill:#2d3436,stroke:#fff,stroke-width:2px,color:#fff
    style C fill:#d35400,stroke:#e67e22,stroke-width:2px,color:#fff
    style D fill:#8e44ad,stroke:#9b59b6,stroke-width:2px,color:#fff
    style E fill:#27ae60,stroke:#2ecc71,stroke-width:2px,color:#fff
```

## ✨ Key Features
-   **🛡️ Dual-Layer Verification**: Analysis is only accepted if it passes the Critic's validation.
-   **🔌 Plug-and-Play Modules**: Separate classes for Fetching, Analyzing, and Validating allow for easy API swaps.
-   **⚡ Robust Error Handling**: Gracefully handles API timeouts, rate limits, and malformed JSON responses.
-   **📊 Automated Reporting**: Generates a human-readable Markdown report + raw JSON data for downstream tasks.

## 🛠️ Installation & Setup

### 1. Clone the Repo
```bash
git clone https://github.com/AmitS1009/NewsTruth-AI-Powered-News-Analysis-Validation-Pipeline.git
cd NewsTruth-AI-Powered-News-Analysis-Validation-Pipeline
```

### 2. Install Dependencies
```bash
pip install -r news-analyzer/requirements.txt
```

### 3. Configure API Keys
Create a `.env` file in `news-analyzer/` and add your keys:
```env
NEWSAPI_KEY=your_key
GEMINI_API_KEY=your_key
OPENROUTER_API_KEY=your_key
```

### 4. Run the Pipeline
```bash
python news-analyzer/main.py
```

## 🧪 Testing
We use `pytest` with `unittest.mock` to verify logic without burning API credits.
```bash
# Windows (PowerShell)
$env:PYTHONPATH="news-analyzer"; pytest news-analyzer/tests/
```

## 📂 Project Structure
```text
.
├── news-analyzer/           # Core source code
│   ├── tests/               # Unit tests
│   ├── llm_analyzer.py      # Gemini integration
│   ├── llm_validator.py     # OpenRouter/Mistral integration
│   ├── main.py              # Orchestrator script
│   ├── news_fetcher.py      # NewsAPI client
│   └── requirements.txt     # Python dependencies
├── output/                  # Generated reports (JSON/Markdown)
├── DEVELOPMENT_PROCESS.md   # Engineering log & Evaluator guide
└── README.md                # Project documentation
```

## 📝 Sample Output
> *From `output/final_report.md`*

### Article: "New Policy Announced..."
- **Source:** [India Today](...)
- **Gist:** The government introduced a new bill targeting...
- **LLM#1 Sentiment:** Positive
- **LLM#2 Validation:** ✓ Correct.
    - **Reasoning:** The text uses words like "historic gain" and "breakthrough".

---
