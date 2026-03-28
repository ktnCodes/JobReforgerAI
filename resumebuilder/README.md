# JobReforgerAI

> Forge tailored resumes with AI-powered ATS + HR dual scoring — fully local, no subscriptions, no API keys required.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Plugin-blueviolet)](https://docs.anthropic.com/en/docs/claude-code)

---

## What It Does

JobReforgerAI takes your master resume and a job description, then:

1. **Pre-screens the fit** — job fit scorer checks for knockout disqualifiers before investing time tailoring
2. **Tailors your resume** — rewrites bullets with JD terminology, updates core competencies with matching keywords
3. **Scores with two independent engines** — ATS keyword/semantic scoring + HR recruiter simulation
4. **Iterates automatically** — revises and re-scores until targets are hit (ATS 75-85%, HR 70%+)
5. **Generates production-ready DOCX** — ATS/Workday-compliant formatting, no tables or graphics
6. **Writes a cover letter** — tailored to the role and company
7. **Tracks every application** — auto-updates an Excel spreadsheet with scores and file links
8. **Finds matching jobs** — searches Indeed, LinkedIn, ZipRecruiter, Glassdoor, and Remotive, ranked by fit with your resume

Everything runs **locally on your machine**. No cloud, no subscriptions, no API keys required for scoring or job search.

> **Note:** The repo includes a legacy `resume_builder.py` CLI that requires an Anthropic API key. This has been **superseded by Claude Code slash commands** (`/resume`, `/tailor-resume`, `/cover-letter`) which need no API key — they run through your Claude Code subscription. The legacy CLI is kept for historical reference only.

---

## How It Compares

| Feature | Jobscan | Rezi | Teal | **JobReforgerAI** |
|---------|---------|------|------|--------------------|
| ATS keyword scoring | ✅ | ✅ | ✅ | ✅ |
| HR / recruiter simulation | ❌ | ❌ | ❌ | ✅ |
| Job fit pre-screen | ❌ | ❌ | ❌ | ✅ |
| Discover matching jobs (no API key) | ❌ | ❌ | ❌ | ✅ |
| Score jobs against your resume | ❌ | ❌ | ❌ | ✅ |
| Auto-tailor resume to JD | ✅ | ✅ | ❌ | ✅ |
| ATS-compliant DOCX output | ❌ | ✅ | ❌ | ✅ |
| Cover letter generation | ❌ | ✅ | ❌ | ✅ |
| Application tracker (Excel) | ❌ | ❌ | ✅ | ✅ |
| 100% local — no subscriptions | ❌ | ❌ | ❌ | ✅ |
| Works in Claude Code / claude.ai | ❌ | ❌ | ❌ | ✅ |
| Open source | ❌ | ❌ | ❌ | ✅ |

---

## Quick Start

### Prerequisites

- Python 3.10+
- [Claude Code](https://docs.anthropic.com/en/docs/claude-code)

### Setup

```bash
git clone https://github.com/ktnCodes/JobReforgerAI.git
cd JobReforgerAI

pip install -r resumebuilder/requirements.txt

# Download NLTK data (one-time)
python -c "import nltk; nltk.download('wordnet'); nltk.download('punkt_tab')"

cp resumebuilder/.env.example resumebuilder/.env
cp resumebuilder/config.example.json resumebuilder/config.json
```

Edit `resumebuilder/config.json` with your name, email, phone, and LinkedIn. Set `master_resume_path` to your resume file (e.g., `../base-resume/YOUR_MASTER_RESUME.md`).

Edit `.env` — the API key is only needed if you plan to use the legacy `resume_builder.py` CLI. The modern slash commands work through Claude Code's subscription with no API key:

```bash
ANTHROPIC_API_KEY=sk-ant-...   # Optional — only for legacy resume_builder.py CLI
```

### Configure the MCP Server

Create a `.mcp.json` file in the project root (excluded from git — contains your local path):

```json
{
  "mcpServers": {
    "ai-resume-tuner": {
      "command": "python",
      "args": ["mcp_scorer.py"],
      "cwd": "/path/to/JobReforgerAI/resumebuilder"
    }
  }
}
```

### Run it

```
/setup
/resume [paste a job description]
```

Or find jobs first:

```
/find-jobs Software Engineer Austin TX
```

---

## Slash Commands

| Command | What It Does |
|---------|-------------|
| `/setup` | One-time setup — installs deps, walks through config |
| `/resume [JD]` | Full package: tailored resume + cover letter + DOCX + tracker update |
| `/tailor-resume [JD]` | Resume only (no cover letter) |
| `/cover-letter [JD]` | Cover letter only |
| `/find-jobs [title] [location]` | Search live job boards, score each result against your resume |
| `/job-fit [JD]` | Quick GO/NO-GO fit check before committing to tailoring |
| `/batch-resume` | Process multiple JDs in parallel |
| `/writing-coach [file]` | Audit and improve resume bullets using 14 writing rules |

---

## MCP Tools

The MCP server (`mcp_scorer.py`) runs locally via FastMCP and exposes these tools to Claude:

| Tool | What It Does |
|------|-------------|
| `score_resume` | Full ATS + HR analysis in one call (recommended) |
| `score_ats` | ATS keyword + semantic scoring (8 components) |
| `score_hr` | HR recruiter simulation (6 factors + F-pattern visual) |
| `explain_score` | Top missing keywords + improvement suggestions |
| `extract_text` | Read text from DOCX, PDF, MD, or TXT files |
| `discover_jobs` | Search job boards and score each job against your resume |

---

## Dual Scoring System

### ATS Scorer — 8 Weighted Components

Simulates how Applicant Tracking Systems filter resumes before a human sees them.

| Component | Weight | What It Measures |
|-----------|--------|------------------|
| Phrase Match | 25% | Multi-word industry phrases |
| Keyword Match | 20% | Lemmatized keywords with synonym expansion |
| Weighted Industry Terms | 15% | Domain-specific terminology with recency decay |
| Semantic Similarity | 10% | SBERT vector cosine similarity (all-MiniLM-L6-v2) |
| BM25 Score | 10% | Probabilistic relevance ranking (BM25Plus) |
| Job Title Match | 10% | Exact JD title in resume header/summary |
| Graph Centrality | 5% | Infers missing skills from related skills (NetworkX) |
| Skill Recency | 5% | Exponential decay — recent experience weighted higher |

**Bonus checks:** Hidden text detection, readability analysis (Flesch-Kincaid Grade 10-12 optimal), format risk flags.

**Score ratings:**

| Score | Rating |
|-------|--------|
| 80-100% | Excellent — top candidate |
| 65-79% | Good — strong match |
| 50-64% | Fair — competitive |
| 35-49% | Low — needs work |
| 0-34% | Poor — unlikely to pass filters |

### HR Scorer — 6 Factors + Visual Analysis

Simulates how a human recruiter evaluates a resume in a 7-second scan.

| Factor | Weight | What It Measures |
|--------|--------|------------------|
| Experience Fit | 30% | Years of experience vs. JD requirements |
| Skills Match | 20% | Demonstrated skills (action verbs) vs. listed skills |
| Career Trajectory | 20% | Title progression via regression slope |
| Impact Signals | 20% | Metrics density + Bloom's Taxonomy verb power |
| Competitive Edge | 10% | Company/university prestige signals |
| F-Pattern Visual | ±5pts | Eye-tracking compliance (golden triangle, left-rail) |

**Risk penalties:** Job hopping (-8 to -15 pts), unexplained gaps (-5 to -15 pts), recent instability.

**Recommendations:**

| Score | Recommendation |
|-------|---------------|
| 85%+ | STRONG INTERVIEW |
| 70-84% | INTERVIEW |
| 55-69% | MAYBE |
| <55% | PASS |

---

## Job Discovery

The `/find-jobs` command and `discover_jobs` MCP tool search live job boards ranked by fit with your resume — no API keys required.

```
/find-jobs Embedded Software Engineer Austin TX
/find-jobs Data Scientist remote
```

**Sources (no API keys needed):**
- **Indeed, LinkedIn, ZipRecruiter, Glassdoor** — via `python-jobspy` (scrapes without keys)
- **Remotive** — remote-only jobs, public API

**How it works:**
1. Searches all sources for the job title + location
2. Pre-filters top candidates by title relevance
3. Lightweight scores all candidates (keyword + phrase + BM25)
4. Full ATS + HR scores top finalists
5. Returns a ranked list with scores and apply links

**Optional Adzuna integration** (free API, 16 countries, salary data): add `ADZUNA_APP_ID` and `ADZUNA_APP_KEY` to `.env`.

---

## Workflow

```
1. /setup                    One-time setup (install deps, create config)
2. Create master resume       YOUR_MASTER_RESUME.md (or .docx / .pdf)
3. /find-jobs [title] [loc]  Optional — discover and score matching jobs
4. /job-fit [JD]             Optional — quick GO/NO-GO before tailoring
5. /resume [JD]              Paste a JD — get a full application package
6. /writing-coach            Optional — audit and improve writing quality
```

Each `/resume` run executes in parallel phases:
- **Phase 1:** Research (reads master resume, finds best prior match, sets up output folder)
- **Phase 2:** Background base scoring + resume writing (non-blocking)
- **Phase 3:** Parallel tailored scoring + cover letter generation
- **Phase 4:** Auto-iteration if scores < target (max 2 rounds)
- **Phase 5:** Parallel DOCX creation + tracker update
- **Phase 6:** Cleanup + final score report

---

## Your Master Resume

Supported formats: `.md`, `.docx`, `.pdf`, `.txt`. Recommended structure:

```
FULL NAME
City, State | Phone | Email | LinkedIn

PROFESSIONAL SUMMARY
[3-4 lines with core expertise]

PROFESSIONAL EXPERIENCE

JOB TITLE | COMPANY NAME | City, State
Month Year – Month Year

• Achievement with quantified impact
• Another achievement with metrics

EDUCATION

Degree Name | University | Graduated Month Year

TECHNICAL SKILLS

Languages: ...
Tools: ...
```

Set `master_resume_path` in `config.json` to point to this file.

---

## Authenticity Rules

JobReforgerAI tailors content without fabricating experience:

**Can be modified:**
- Professional Summary — incorporate JD keywords naturally
- Core Competencies — match to JD keywords (primary keyword location)
- Bullet points — reframe achievements using JD language

**Never modified:**
- Job titles — must match master resume exactly
- Company names, dates, education, certifications
- Publications and professional memberships

Each keyword appears **1-2 times max** across the entire resume. Authentic content at 75% ATS beats keyword stuffing at 90%.

---

## Project Structure

```
JobReforgerAI/
├── .claude/commands/               # Slash commands (invoked from root)
│   ├── resume.md                   # Full application workflow
│   ├── tailor-resume.md            # Resume only
│   ├── cover-letter.md             # Cover letter only
│   ├── find-jobs.md                # Job discovery
│   ├── batch-resume.md             # Batch processing
│   ├── setup.md                    # One-time setup
│   └── writing-coach.md            # Writing enhancement (14 rules)
├── base-resume/                    # Your master resume (gitignored)
├── tailored-resumes/               # Generated tailored resumes + JDs (gitignored)
├── cover-letters/                  # Generated cover letters (gitignored)
├── job-trackcsv/                   # Job application tracker (gitignored)
├── CLAUDE.md                       # Root workspace context
├── resumebuilder/                  # Tool source code
│   ├── data/                       # Scoring reference databases
│   │   ├── keywords_*.json         # Domain keyword databases (6 domains)
│   │   ├── skill_taxonomy.json     # Skill decay constants
│   │   ├── company_prestige.json   # Prestige scoring
│   │   └── action_verbs.json       # Bloom's Taxonomy verb classifications
│   ├── taxonomy/                   # O*NET skill taxonomy loader
│   ├── scoring/                    # Modular scoring package
│   ├── ats_scorer.py               # ATS scoring engine (8 components)
│   ├── hr_scorer.py                # HR scoring engine (6 factors)
│   ├── mcp_scorer.py               # FastMCP server (6 tools, local-only)
│   ├── job_discovery.py            # Job search (JobSpy + Remotive + Adzuna)
│   ├── job_fit_scorer.py           # Job fit pre-screener
│   ├── docx_generator.py           # ATS/Workday-compliant DOCX generator
│   ├── text_extractor.py           # PDF/DOCX/MD/TXT text extraction
│   ├── orchestration_state.py      # Multi-agent state management
│   ├── tracker_utils.py            # Excel application tracker
│   ├── config.example.json         # Config template
│   ├── requirements.txt            # Python dependencies
│   └── CLAUDE.md                   # Full project documentation
```

---

## Tech Stack

| Component | Technology |
|-----------|------------|
| AI Agent Framework | [Claude Code](https://docs.anthropic.com/en/docs/claude-code) |
| MCP Server | [FastMCP 3.0](https://gofastmcp.com/) (local-only) |
| Embeddings | [Sentence Transformers](https://sbert.net/) (all-MiniLM-L6-v2) |
| NLP | NLTK (lemmatization), TextStat (readability) |
| Search | BM25Plus (rank-bm25), NetworkX (skill graphs) |
| Job Discovery | python-jobspy (Indeed/LinkedIn/ZipRecruiter/Glassdoor) + Remotive |
| JD Scraping | trafilatura + BeautifulSoup |
| Document Generation | python-docx |
| PDF Parsing | pdfplumber |
| Application Tracking | openpyxl (Excel) |

---

## License

MIT License — see the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- Built with [Claude Code](https://docs.anthropic.com/en/docs/claude-code) by [Anthropic](https://www.anthropic.com/)
- ATS scoring informed by real-world Applicant Tracking System behavior research
- HR scoring model informed by eye-tracking research on recruiter behavior patterns
- Domain keyword databases curated from real job descriptions across 6 industries
- Job search powered by [python-jobspy](https://github.com/Bunsly/JobSpy) and [Remotive](https://remotive.com/)
