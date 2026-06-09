<div align="center">

# 🔍 REPILOT
### Multi-Agent AI Research System

*Automate deep research with a pipeline of specialized AI agents — search, scrape, write, and critique in one command.*

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python&logoColor=white)](https://python.org)
[![LangChain](https://img.shields.io/badge/LangChain-Powered-1C3C3C?logo=chainlink&logoColor=white)](https://langchain.com)
[![Mistral AI](https://img.shields.io/badge/Mistral_AI-small--2506-FF7000?logoColor=white)](https://mistral.ai)
[![Google Gemini](https://img.shields.io/badge/Google-Gemini_2.5-4285F4?logo=google&logoColor=white)](https://deepmind.google/technologies/gemini)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

</div>

---

## 📖 Overview

**Repilot** is a production-grade, multi-agent AI research system that transforms any topic into a structured, peer-reviewed research report — fully automated. It orchestrates a pipeline of specialized LangChain agents and LLM chains, each with a distinct role: searching the web, scraping source content, drafting professional reports, and delivering rigorous critique.

No more manual research tabs. No more copy-paste. Just a topic — and a comprehensive report.

---

## ✨ Key Features

- **🤖 4-Stage Agentic Pipeline** — Search → Scrape → Write → Critique, fully automated
- **🌐 Live Web Research** — Tavily-powered search agent fetches fresh, reliable sources
- **📄 Deep Content Scraping** — BeautifulSoup reader agent extracts full page content from top URLs
- **📝 Professional Report Writing** — Structured reports with Executive Summary, Key Findings, Analysis, and Recommendations
- **🧑‍⚖️ AI Peer Review** — A critic chain scores the report across 5 dimensions and flags issues with actionable fixes
- **⚡ Dual-LLM Architecture** — Mistral AI for agents and chains; Gemini 2.5 Flash as a configurable backbone
- **🖥️ Streamlit Web UI** — Clean browser interface alongside a CLI mode
- **🎨 Rich Console Output** — Color-formatted, stage-by-stage terminal feedback via `rich`

---

## 🏗️ Architecture

```
User Input (Topic)
       │
       ▼
┌─────────────────────────────────────────────────────┐
│                  Research Pipeline                  │
│                                                     │
│  ┌──────────────┐     ┌──────────────────────────┐  │
│  │ Search Agent │────▶│ Tavily Web Search Tool   │  │
│  │  (Gemini)   │     │ (Recent & Reliable URLs)  │  │
│  └──────────────┘     └──────────────────────────┘  │
│          │                                          │
│          ▼                                          │
│  ┌──────────────┐     ┌──────────────────────────┐  │
│  │ Reader Agent │────▶│ BeautifulSoup Scraper   |   │
│  │  (Gemini)   │      │ (Full Page Content)     |   │
│  └──────────────┘     └──────────────────────────┘  │
│          │                                          │
│          ▼                                          │
│  ┌──────────────────────────────────────────────┐   │
│  │           Writer Chain (Gemini)              │   │
│  │  Executive Summary → Key Findings → Analysis │   │
│  │  → Conclusion → Recommendations → Sources    │   │
│  └──────────────────────────────────────────────┘   │
│          │                                          │
│          ▼                                          │
│  ┌──────────────────────────────────────────────┐   │
│  │           Critic Chain (Gemini)              │   │
│  │  Scores: Accuracy · Depth · Structure ·      │   │
│  │  Clarity · Usefulness  →  Verdict            │   │
│  └──────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────┘
       │
       ▼
 Final Report + Peer Review
```

---

## 📁 Project Structure

```
repilot/
├── agents.py          # Agent definitions + Writer & Critic LangChain chains
├── pipeline.py        # 4-stage orchestration pipeline
├── tools.py           # Tavily search + BeautifulSoup scraping tools
├── app.py             # Streamlit web interface
├── requirements.txt   # Python dependencies
├── .env               # API keys (not committed)
└── .gitignore
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.9 or higher
- API keys for **Mistral AI**, **Google Gemini**, and **Tavily**

### 1. Clone the Repository

```bash
git clone https://github.com/VivekChouhan1/Multi_Agent_AI_Research_System.git
cd Multi_Agent_AI_Research_System
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate       # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the root directory:

```env
MISTRAL_API_KEY=your_mistral_api_key_here
GOOGLE_API_KEY=your_google_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

| Variable | Where to Get |
|---|---|
| `MISTRAL_API_KEY` | [console.mistral.ai](https://console.mistral.ai) |
| `GOOGLE_API_KEY` | [aistudio.google.com](https://aistudio.google.com) |
| `TAVILY_API_KEY` | [tavily.com](https://tavily.com) |

---

## 💻 Usage

### CLI Mode

Run the research pipeline directly from your terminal:

```bash
python pipeline.py
```

You'll be prompted to enter a topic:

```
Enter research topic: The rise of agentic AI in 2025
```

Repilot will then execute all 4 stages and print a formatted report + peer review to the console.

### Web UI (Streamlit)

```bash
streamlit run app.py
```

Then open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 📊 Pipeline Stages

| Stage | Component | Description |
|---|---|---|
| 1 | Search Agent | Queries Tavily for recent, reliable sources on the topic |
| 2 | Reader Agent | Selects top URLs and scrapes full content via BeautifulSoup |
| 3 | Writer Chain | Synthesizes research into a structured professional report |
| 4 | Critic Chain | Peer-reviews the report across 5 quality dimensions |

### Report Structure (Writer Output)

- **Executive Summary** — 2–3 sentence overview
- **Introduction** — Background, relevance, scope
- **Key Findings** — Minimum 4 findings with subheadings, data, and implications
- **Analysis & Insights** — Patterns, contradictions, context
- **Conclusion** — Synthesis + forward-looking statement
- **Recommendations** — Actionable steps grounded in evidence
- **Sources** — All scraped URLs, properly listed

### Critic Scoring Dimensions

| Dimension | What It Evaluates |
|---|---|
| Accuracy | Are claims factual and properly sourced? |
| Depth | Does it go beyond surface-level observations? |
| Structure | Is it logically organized with smooth flow? |
| Clarity | Is language precise, concise, and jargon-free? |
| Usefulness | Does it deliver real insight or actionable value? |

---

## 🛠️ Tech Stack

| Library | Role |
|---|---|
| `langchain` | Agent framework & chain composition |
| `langgraph` | Agent execution graph |
| `langchain_mistralai` | Mistral AI LLM integration |
| `langchain_google_genai` | Google Gemini LLM integration |
| `langchain_community` | Community tools & utilities |
| `tavily-python` | Real-time web search API |
| `beautifulsoup4` | HTML content scraping |
| `requests` | HTTP requests for scraping |
| `streamlit` | Web UI |
| `rich` | Beautiful terminal output |
| `python-dotenv` | Environment variable management |

---

## 🤝 Contributing

Contributions are welcome! Here's how to get started:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Commit your changes: `git commit -m "feat: add your feature"`
4. Push to the branch: `git push origin feature/your-feature-name`
5. Open a Pull Request

Please follow [conventional commits](https://www.conventionalcommits.org/) and ensure your code is clean and documented.

---

## 📜 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Vivek Chouhan**

[![GitHub](https://img.shields.io/badge/GitHub-VivekChouhan1-181717?logo=github)](https://github.com/VivekChouhan1)

---

<div align="center">

*Built with ❤️ using LangChain, Mistral AI, and Python*

⭐ Star this repo if you find it useful!

</div>
