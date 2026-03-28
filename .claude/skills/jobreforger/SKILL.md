---
name: jobreforger
description: "AI-powered resume builder with ATS/HR scoring. Use this skill whenever the user mentions resumes, cover letters, job applications, tailoring a resume, ATS optimization, job searching, job fit checks, or writing coaching for resumes. Trigger on any of these: 'tailor my resume', 'create a resume', 'help me apply', 'cover letter', 'find jobs', 'job search', 'is this job a good fit', 'should I apply', 'improve my resume writing', 'batch process resumes', 'resume builder', 'ATS score', 'HR score', 'optimize for ATS', 'application package', 'job description', or any request involving resume/CV creation, editing, or optimization. Even if the user just pastes a job description, this skill should trigger."
---

# JobReforgerAI — Resume Builder & Job Application Toolkit

AI-powered resume tailoring with dual ATS/HR scoring, cover letter generation, job discovery, and writing coaching.

## Workflow Router

Determine which workflow the user needs based on their request, then follow the instructions for that workflow.

### 1. Full Application Package (resume + cover letter)
**Trigger:** User wants both a resume and cover letter, says "apply to this job", "full package", or pastes a JD without specifying resume-only or cover-letter-only.

Read these files in order:
```
Read: _jobreforger/.claude/commands/resume.md
Read: _jobreforger/.claude/commands/lib/scoring-rules.md
```

### 2. Resume Only
**Trigger:** User says "tailor my resume", "just the resume", "resume only", "ATS optimize my resume".

Read these files:
```
Read: _jobreforger/.claude/commands/tailor-resume.md
Read: _jobreforger/.claude/commands/lib/scoring-rules.md
```

### 3. Cover Letter Only
**Trigger:** User says "write a cover letter", "just the cover letter", "cover letter only".

```
Read: _jobreforger/.claude/commands/cover-letter.md
```

### 4. Job Search & Discovery
**Trigger:** User says "find jobs", "search for jobs", "what jobs match my resume", "look for openings".

```
Read: _jobreforger/.claude/commands/find-jobs.md
```

### 5. Job Fit Pre-Screen (Quick GO/NO-GO)
**Trigger:** User says "is this job a good fit?", "should I apply?", "job fit check", "pre-screen this".

```
Read: _jobreforger/.claude/commands/job-fit.md
```

### 6. Writing Coach (Resume Enhancement)
**Trigger:** User says "improve my resume writing", "writing coach", "review my resume", "make my bullets stronger".

```
Read: _jobreforger/.claude/commands/writing-coach.md
```

### 7. Batch Processing
**Trigger:** User says "batch resume", "process multiple JDs", "bulk applications".

```
Read: _jobreforger/.claude/commands/batch-resume.md
```

### 8. Setup (First-Time Configuration)
**Trigger:** User says "setup", "configure", "install", or this is their first time using the tool.

```
Read: _jobreforger/.claude/commands/setup.md
```

## Global Rules (Apply to ALL Workflows)

- All Python scripts live in `_jobreforger/`. Run them with: `cd _jobreforger && python ...`
- Configuration: `_jobreforger/config.json` (created during setup from `config.example.json`)
- Output folder: `_jobreforger/applications/{Company} - {JobTitle}/`
- NEVER change: job titles, company names, dates, education, publications, certifications, memberships
- NEVER use `**bold**` markdown in .md files — the DOCX generator handles formatting
- NEVER exceed 2 appearances of any keyword across the resume
- Score targets: ATS 75-85%, HR 70%+
- Format-aware file reading: `.md`/`.txt` use Read tool directly; `.docx` use `extract_text` MCP tool or python-docx; `.pdf` use Read tool directly
- The `$ARGUMENTS` placeholder in command files refers to the user's input — extract the job description or query from the conversation context

## First-Time Detection

If `_jobreforger/config.json` does not exist, the user needs to run setup first. Prompt them: "It looks like JobReforgerAI hasn't been configured yet. Let me walk you through the one-time setup first."

Then read and follow `_jobreforger/.claude/commands/setup.md`.
