# JobReforgerAI Workspace

## What This Workspace Is

AI resume toolkit with ATS + HR dual scoring. Fully local, no subscriptions.
Supports two interfaces: Claude Code (slash commands) and Claude Cowork (skill).

All source code lives in `_jobreforger/`. Personal files (resumes, cover letters, job tracker) are gitignored.

Repo: https://github.com/ktnCodes/JobReforgerAI

---

## Folder Structure

```
JobReforgerAI/
├── _jobreforger/       # Python source code (scoring engines, tools, data)
├── base-resume/        # Your master resume — always kept up to date (gitignored)
├── tailored-resumes/   # Generated tailored resumes + JDs (gitignored)
├── cover-letters/      # Generated cover letters (gitignored)
└── job-tracker/        # Application tracker spreadsheet (gitignored)
```

---

## Routing Table

| Task                              | Load These                                              | Skip These                     |
|-----------------------------------|---------------------------------------------------------|--------------------------------|
| Run the tool (Claude Code)        | `CLAUDE.md`, then use slash commands                   | `_jobreforger/` source files   |
| Run the tool (Cowork)             | `CLAUDE.md`, install `jobreforger.skill`               | `_jobreforger/` source files   |
| Update the base resume            | `base-resume/Kevin_Nguyen_master_resume.md`            | tailored-resumes/, cover-letters/ |
| Tailor a resume manually          | `base-resume/`, job description                        | Other tailored files           |
| Debug scoring or scoring logic    | `_jobreforger/ats_scorer.py` or `hr_scorer.py`         | -                              |
| Add a feature or fix a bug        | `_jobreforger/CLAUDE.md`, relevant source file         | Personal output folders        |
| Review architecture               | `_jobreforger/CLAUDE.md`                               | -                              |

---

## Quick Start (Claude Code)

```bash
/setup                              # One-time configuration
/resume [paste job description]     # Full package: resume + cover letter + DOCX
/find-jobs [title] [location]       # Search and score matching jobs
/job-fit [paste JD]                 # Quick GO/NO-GO pre-screen
```

## Quick Start (Cowork)

Install `jobreforger.skill` from the project root, then use natural language:
- "Help me apply to this job: [paste JD]"
- "Find embedded software engineer jobs in Austin TX"

---

## Resume Principles

- Lead with impact, not responsibilities ("Built X that reduced Y by Z%")
- Keep to one page unless 10+ years experience
- Use keywords from job descriptions — ATS systems scan for them
- Quantify everything possible
- Authentic content at 75% ATS beats keyword stuffing at 90%

