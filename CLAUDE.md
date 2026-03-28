# JobReforgerAI — Workspace Root

## Structure

```
JobReforgerAI/
├── _jobreforger/          # Tool source code (Python, scoring engines, data)
├── base-resume/            # Your master resume (personal, gitignored)
├── tailored-resumes/       # Generated tailored resumes + JDs (personal, gitignored)
├── cover-letters/          # Generated cover letters (personal, gitignored)
├── job-tracker/            # Job application tracker (personal, gitignored)
├── .claude/commands/       # Slash commands for Claude Code CLI
└── .claude/skills/         # Skills for Claude Cowork (desktop app)
```

## How It Works

All Python source code lives in `_jobreforger/`. The project supports two Claude interfaces:

- **Claude Code (CLI):** Uses slash commands in `.claude/commands/`
- **Claude Cowork (Desktop App):** Uses skills in `.claude/skills/`

Both interfaces share the same Python backend and command logic in `_jobreforger/.claude/commands/`.

Python scripts are invoked with `cd _jobreforger && python ...` so imports resolve correctly. File paths in Python code use `../` to reference root-level folders (e.g., `../tailored-resumes/`, `../base-resume/`).

## Quick Start — Claude Code (CLI)

```bash
/setup                              # One-time configuration
/resume [paste job description]     # Full package: resume + cover letter + DOCX
/tailor-resume [paste JD]           # Resume only
/cover-letter [paste JD]            # Cover letter only
/find-jobs [title] [location]       # Search and score jobs
/batch-resume                       # Process multiple JDs
/writing-coach [file]               # Improve resume writing
```

## Quick Start — Claude Cowork (Desktop App)

### First-Time Install

Install the `jobreforger.skill` file from the project root. This adds the JobReforgerAI skill to your Cowork environment.

### Usage

Just describe what you need in natural language. The skill triggers automatically:

- "Help me apply to this job: [paste JD]" — Full resume + cover letter package
- "Tailor my resume for this role: [paste JD]" — Resume only
- "Write a cover letter for this position: [paste JD]" — Cover letter only
- "Find data scientist jobs in NYC" — Job search & scoring
- "Is this job a good fit? [paste JD]" — Quick GO/NO-GO pre-screen
- "Review my resume writing and make it stronger" — Writing coach
- "Process all the JDs in my batch folder" — Batch processing
- "Set up JobReforger" — One-time configuration

### If the skill is not installed

You can also use the skill by asking Claude to read the skill file directly:
"Read `.claude/skills/jobreforger/SKILL.md` and follow its instructions to [your request]"

## Configuration

- `_jobreforger/config.json` — User name, email, phone, resume path, output directory
- `_jobreforger/config.example.json` — Template for new users
- `_jobreforger/.env` — API keys (optional, for LLM-augmented scoring)

See `_jobreforger/CLAUDE.md` for full project documentation including scoring system details, architecture, and development guide.
