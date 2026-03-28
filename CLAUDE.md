# JobReforgerAI — Workspace Root

## Structure

```
JobReforgerAI/
├── resumebuilder/          # Tool source code (Python, scoring engines, data)
├── base-resume/            # Your master resume (personal, gitignored)
├── tailored-resumes/       # Generated tailored resumes + JDs (personal, gitignored)
├── cover-letters/          # Generated cover letters (personal, gitignored)
├── job-trackcsv/           # Job application tracker (personal, gitignored)
└── .claude/commands/       # Slash commands (run from this root directory)
```

## How It Works

All Python source code lives in `resumebuilder/`. Slash commands are in `.claude/commands/` at the root level so they can be invoked from this directory.

Python scripts are invoked with `cd resumebuilder && python ...` so imports resolve correctly. File paths in Python code use `../` to reference root-level folders (e.g., `../tailored-resumes/`, `../base-resume/`).

## Quick Start

```bash
/setup                              # One-time configuration
/resume [paste job description]     # Full package: resume + cover letter + DOCX
/tailor-resume [paste JD]           # Resume only
/cover-letter [paste JD]            # Cover letter only
/find-jobs [title] [location]       # Search and score jobs
/batch-resume                       # Process multiple JDs
/writing-coach [file]               # Improve resume writing
```

## Configuration

- `resumebuilder/config.json` — User name, email, phone, resume path, output directory
- `resumebuilder/config.example.json` — Template for new users
- `resumebuilder/.env` — API keys (optional, for LLM-augmented scoring)

See `resumebuilder/CLAUDE.md` for full project documentation including scoring system details, architecture, and development guide.
