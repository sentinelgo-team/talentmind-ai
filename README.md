<div align="center">

<img src="https://img.shields.io/badge/%F0%9F%A7%A0-TalentMind_AI-blueviolet?style=for-the-badge&labelColor=1a1a2e" alt="TalentMind AI"/>

# TalentMind AI

**Where Artificial Intelligence Meets Human Potential**

[![Build](https://img.shields.io/badge/build-passing-brightgreen?style=flat-square)](.)
[![Python](https://img.shields.io/badge/python-3.10+-blue?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Gemini](https://img.shields.io/badge/Powered_by-Google_Gemini-4285F4?style=flat-square&logo=google&logoColor=white)](https://ai.google.dev)
[![LangChain](https://img.shields.io/badge/LangChain-Orchestrated-green?style=flat-square)](https://langchain.com)
[![Docker](https://img.shields.io/badge/docker-ready-2496ED?style=flat-square&logo=docker&logoColor=white)](https://docker.com)
[![License](https://img.shields.io/badge/license-proprietary-lightgrey?style=flat-square)](.)

<br/>

<kbd>
<br/>
&nbsp;&nbsp; A production-grade multi-agent AI system that orchestrates 12 specialized agents &nbsp;&nbsp;<br/>
&nbsp;&nbsp; to deliver deep recruitment intelligence and personalized career guidance. &nbsp;&nbsp;<br/>
<br/>
</kbd>

<br/><br/>

[**Explore Features**](#features) | [**Quick Start**](#quick-start) | [**Architecture**](#architecture) | [**AI Agents**](#the-12-ai-agents) | [**Deploy**](#deployment)

</div>

<br/>

---

<br/>

## The Problem

> 75% of resumes are rejected by ATS systems before a human ever reads them. Meanwhile, professionals lack personalized guidance to bridge skill gaps and navigate career transitions.

**TalentMind AI** solves both sides:

```diff
- Traditional ATS: keyword matching, static scoring, zero guidance
+ TalentMind AI: semantic understanding, multi-agent reasoning, actionable roadmaps
```

<br/>

## Features

<table>
<tr>
<td width="50%">

### For Recruiters

| Feature | What it does |
|:--------|:-------------|
| ATS Scoring | Multi-dimensional resume scoring beyond keywords |
| Candidate Ranking | AI-powered comparison with explainable reasoning |
| Risk Detection | Flags gaps, inconsistencies, red flags |
| Job Matching | Semantic fit between JD and candidate |
| PDF Reports | One-click professional assessment exports |

</td>
<td width="50%">

### For Candidates

| Feature | What it does |
|:--------|:-------------|
| Resume Analysis | Strengths, weaknesses, improvement areas |
| Skill Detection | Auto-extract and categorize all skills |
| Gap Analysis | What you're missing for your target role |
| Interview Prep | Personalized questions by difficulty |
| Career Paths | AI-recommended next moves + learning plans |

</td>
</tr>
</table>

<br/>

## The 12 AI Agents

Each agent is a **domain specialist** powered by Google Gemini. The Orchestrator coordinates them through a multi-step pipeline:

```
                          +------------------+
                          |   ORCHESTRATOR   |
                          |  (LangGraph DAG) |
                          +--------+---------+
                                   |
              +--------------------+--------------------+
              |                    |                    |
     +--------v------+    +-------v-------+    +-------v--------+
     | Resume Agent  |    |   ATS Agent   |    |  Skill Agent   |
     | Parse & Model |    | Score & Grade |    | Detect & Rate  |
     +--------+------+    +-------+-------+    +-------+--------+
              |                    |                    |
     +--------v------+    +-------v-------+    +-------v--------+
     | Skill Gap     |    | Job Matching  |    | Interview      |
     | Find Deficits |    | Semantic Fit  |    | Gen Questions  |
     +--------+------+    +-------+-------+    +-------v--------+
              |                    |                    |
     +--------v------+    +-------v-------+    +-------v--------+
     | Ranking       |    |  Risk Agent   |    | Recommendation |
     | Compare All   |    | Flag Issues   |    | Career Paths   |
     +--------+------+    +-------+-------+    +-------+--------+
              |                    |                    |
              +--------------------+--------------------+
                                   |
                          +--------v---------+
                          | Reflection Agent |
                          | QA & Consistency |
                          +--------+---------+
                                   |
                          +--------v---------+
                          |  PDF Report Agent |
                          |  Export & Deliver |
                          +------------------+
```

<br/>

## Tech Stack

```yaml
Frontend:       Streamlit + Plotly (interactive dashboards, dark theme)
AI Engine:      Google Gemini 1.5 Pro via google-genai SDK
Orchestration:  LangChain + LangGraph (multi-agent DAG workflows)
NLP:            SpaCy, NLTK, scikit-learn
Database:       SQLite + SQLAlchemy ORM
Vector Search:  FAISS (semantic similarity)
Documents:      PyPDF, python-docx (PDF/DOCX/TXT parsing)
Reports:        ReportLab (professional PDF generation)
Security:       cryptography, input sanitization, non-root Docker
Testing:        Pytest + coverage + mocking
Deployment:     Docker multi-stage build + Docker Compose
```

<br/>

## Architecture

```
talentmind-ai/
|
+-- app/
|   +-- agents/           # 12 specialized AI agents
|   +-- core/             # Settings, constants, exceptions, logging
|   +-- database/         # SQLAlchemy models + repository pattern
|   +-- memory/           # FAISS-backed session memory + embeddings
|   +-- models/           # Pydantic v2 data models
|   +-- orchestrator/     # LangGraph workflow coordination
|   +-- processors/       # File parsing (PDF, DOCX, TXT)
|   +-- prompts/          # Structured prompt templates
|   +-- services/         # Business logic layer
|   +-- ui/
|   |   +-- pages/        # 10 Streamlit page modules
|   |   +-- charts/       # Plotly visualization components
|   |   +-- theme.py      # Dark glassmorphism theme
|   +-- utils/            # Validators, benchmarks, roadmap gen
|   +-- main.py           # Application entry point
|
+-- tests/
|   +-- unit/             # 8 unit test modules
|   +-- integration/      # 2 integration test modules
|   +-- fixtures/         # Test data
|
+-- scripts/              # init_db.py, setup.sh
+-- data/                 # uploads/, processed/, reports/, vector_db/
+-- docs/                 # Phase documentation
+-- Dockerfile            # Multi-stage production build
+-- docker-compose.yml    # Container orchestration
+-- requirements.txt      # Pinned dependencies
+-- pytest.ini            # Test configuration
```

<br/>

## Quick Start

### Prerequisites

- **Python 3.10+**
- **Google Gemini API Key** - [Get yours free](https://ai.google.dev)

### Installation

```bash
# 1. Clone
git clone https://github.com/sentinelgo-team/talentmind-ai.git
cd talentmind-ai

# 2. Virtual environment
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. NLP models
python -m spacy download en_core_web_sm
python -m nltk.downloader punkt stopwords

# 5. Configure
cp .env.example .env
# Edit .env -> add your GOOGLE_API_KEY

# 6. Initialize database
python scripts/init_db.py

# 7. Launch
streamlit run app/main.py
```

Open **http://localhost:8501** and upload your first resume.

<br/>

## Deployment

### Docker (Recommended for Production)

```bash
# One command to build + run
docker-compose up --build -d

# Health check
curl http://localhost:8501/_stcore/health
```

The Docker setup includes:
- Multi-stage build (smaller image)
- Non-root user (security)
- Health checks (reliability)
- Persistent volumes for data & logs
- Auto-restart policy

<br/>

## How It Works

```
Resume Upload --> File Processor --> Text Extraction
                                          |
                                          v
                                   Agent Orchestrator
                                          |
                    +---------+---------+--+--+---------+---------+
                    |         |         |     |         |         |
                    v         v         v     v         v         v
                 Resume    ATS      Skills  Gap     Matching  Interview
                 Agent    Agent     Agent   Agent    Agent     Agent
                    |         |         |     |         |         |
                    +---------+---------+--+--+---------+---------+
                                          |
                                          v
                              Ranking + Risk + Recommendation
                                          |
                                          v
                              Reflection Agent (QA Pass)
                                          |
                                          v
                              PDF Report Generation
                                          |
                                          v
                              Dashboard + Interactive UI
```

<br/>

## Testing

```bash
# Full suite
pytest

# With coverage report
pytest --cov=app --cov-report=html --cov-report=term-missing

# Unit tests only
pytest tests/unit/ -v

# Integration tests only
pytest tests/integration/ -v
```

<br/>

## Configuration

All settings are managed via environment variables (`.env` file):

| Variable | Purpose | Default |
|----------|---------|---------|
| `GOOGLE_API_KEY` | Gemini API authentication | *required* |
| `GEMINI_MODEL` | Model version | `gemini-1.5-pro` |
| `APP_ENV` | Environment mode | `development` |
| `MAX_FILE_SIZE_MB` | Upload size limit | `10` |
| `LOG_LEVEL` | Logging verbosity | `INFO` |

See `.env.example` for the complete list.

<br/>

## Project Stats

| Metric | Value |
|--------|-------|
| Total Files | 100 |
| Python Source Files | 74 |
| AI Agents | 12 |
| UI Pages | 10 |
| Test Cases | 40+ |
| Lines of Code | ~8,000+ |

<br/>

---

<div align="center">

<br/>

**TalentMind AI** | Built by the **SentinelGo Team**

*Transforming recruitment through collaborative AI intelligence.*

<br/>

[![GitHub](https://img.shields.io/badge/View_on-GitHub-181717?style=for-the-badge&logo=github)](https://github.com/sentinelgo-team/talentmind-ai)

<br/>

</div>
