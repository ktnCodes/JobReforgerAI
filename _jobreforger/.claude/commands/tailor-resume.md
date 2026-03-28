# Tailor Resume Only (ATS + HR Optimized) — Swarm v3.0

Optimize and tailor the resume using **parallel agent execution** for maximum speed. Target: 75-85% ATS + 70%+ HR with AUTHENTIC content.

## Job Description
$ARGUMENTS

## Instructions

You are an expert ATS optimization specialist with access to **parallel agents** (Task tool). The user has provided a job description above. Execute the following phases, launching background agents wherever possible.

---

## PHASE 0.5: JOB FIT PRE-CHECK (mandatory gate)

Before investing time in tailoring, run the Job Fit Scorer to check for knockout disqualifiers:

```python
from job_fit_scorer import calculate_job_fit, format_report
result = calculate_job_fit(resume_text, jd_text)
```

**Decision gate:**
- **STRONG FIT (75+)**: Proceed to Phase 1.
- **MODERATE FIT (55-74)**: Proceed — show the user fixable gaps and note them for writing.
- **WEAK FIT (35-54)**: PAUSE. Show the user the report and ask: "This job is a weak fit (score: X). [Show knockouts/gaps]. Continue anyway?"
- **NO-GO (<35 or hard knockouts)**: STOP. Show the full report with knockouts and alternative job titles. Do NOT proceed. Tell the user: "This job has disqualifying requirements: [list knockouts]. Better-fit roles: [alternatives]."

Display the fit score, any knockouts, and key dimensions before proceeding.

---

## PHASE 1: PARALLEL RESEARCH (launch all simultaneously)

Execute these **3 actions in a single parallel tool call** (no agents — use Read, Glob, Write tools simultaneously):

**Action A — Find best matching resume:**
- Use `Glob` to find all `applications/**/*Resume*.docx` files
- From folder names (`{Company} - {JobTitle}`), identify the most semantically similar role
- **If match found (PREFERRED)**: Read `.docx` via Bash: `python -c "from docx import Document; [print(p.text) for p in Document('path').paragraphs]"`
- **If no match**: Fall back to the master resume (read `config.json` for `master_resume_path`, or glob for `*MASTER*RESUME*.md`, `*MASTER*RESUME*.docx`, `*MASTER*RESUME*.pdf`)

**Action B — Read master resume:**
- Read the master resume (path from `config.json` → `master_resume_path`) for canonical job titles, dates, company names, education, certifications, publications, memberships (NEVER change these)
- **Format-aware reading:** `.md`/`.txt` → use `Read` tool directly. `.pdf` → use `Read` tool directly (Claude handles PDFs natively). `.docx` → call `extract_text` MCP tool with the file path (Claude cannot read binary DOCX files directly).

**Action C — Setup output:**
- Extract company name and job title from JD
- Create output folder: `applications/{CompanyName} - {JobTitle}/`
- Save JD as `job_description.txt`

---

## PHASE 2: BACKGROUND BASE SCORING + IMMEDIATE RESUME WRITING

**Launch 2 background Bash agents AND start writing immediately — do NOT wait for base scores.**

Base scores are only needed for the final comparison report.

**Background Agent A — Combined Base Score (ATS + HR):**
```
Use Task tool (subagent_type: "Bash", run_in_background: true, name: "base-scorer"):
python ats_scorer.py --score "{base_template_path}" "applications/{folder}/job_description.txt" --json && python hr_scorer.py --score "{base_template_path}" "applications/{folder}/job_description.txt" --json
```

**MAIN AGENT — Generate the tailored resume immediately (see RESUME WRITING RULES below).**

Save as `resume.md` in the output folder.

**CRITICAL .md FORMATTING RULE:** Do NOT use `**` (markdown bold asterisks) anywhere in resume.md files. Write metrics and text as plain text (e.g., "11,300+ ICU stays" not "**11,300+ ICU stays**"). The DOCX generator handles bold formatting automatically — asterisks in .md files cause display issues.

---

## PHASE 3: PARALLEL TAILORED SCORING (launch both simultaneously)

Once `resume.md` is saved, launch **2 agents in a single parallel tool call**:

**Background Agent C — Combined Tailored Score (ATS + HR):**
```
Use Task tool (subagent_type: "Bash", run_in_background: true, name: "tailored-scorer"):
python ats_scorer.py --score "applications/{folder}/resume.md" "applications/{folder}/job_description.txt" --json && python hr_scorer.py --score "applications/{folder}/resume.md" "applications/{folder}/job_description.txt" --json
```

---

## PHASE 3.5: ERROR RECOVERY CHECK

Before reading scores, verify background agents completed. If agents failed or timed out (60s), fall back to direct scoring:
```bash
python ats_scorer.py --score "applications/{folder}/resume.md" "applications/{folder}/job_description.txt" --json
python hr_scorer.py --score "applications/{folder}/resume.md" "applications/{folder}/job_description.txt" --json
```
Parse the JSON output directly instead of waiting for state.json.

---

## PHASE 4: SCORE CHECK + ITERATION (max 2 rounds)

1. **Collect scores** from agents C and D
2. **Evaluate:**

```
IF ATS < 75%:
    → Add keywords to Core Competencies (primary method)
    → Naturally reframe 1-2 bullet points with JD language
    → Re-score: `python ats_scorer.py --score "applications/{folder}/resume.md" "applications/{folder}/job_description.txt" --json`

IF ATS ≥ 75% AND HR < 70%:
    → Improve bullet impact (metrics, action verbs)
    → Remove awkward keyword insertions
    → Re-score via CLI (1 background Bash agent)

IF ATS ≥ 75% AND HR ≥ 70%:
    → PASS — proceed to finalization
```

3. **Max 2 iteration rounds.** Each round = 2 parallel scoring agents.

---

## PHASE 5: PARALLEL FINALIZATION (launch both simultaneously)

Once scores pass, launch **2 agents in a single parallel tool call**:

**Background Agent E — Resume DOCX (from markdown):**
```
Use Task tool (subagent_type: "Bash", run_in_background: true, name: "resume-docx-creator"):
cd "." && python -c "from docx_generator import create_resume_from_md; create_resume_from_md('applications/{folder}/resume.md', 'applications/{folder}/{Name}_Resume_{Company}.docx'); print('Resume DOCX created successfully')"
```

**Background Agent F — Update Tracker:**
```
Use Task tool (subagent_type: "Bash", run_in_background: true, name: "tracker-updater"):
cd "." && python -c "
from tracker_utils import add_application
add_application(
    company='{Company}',
    job_title='{Job Title}',
    resume_file='{Name}_Resume_{Company}.docx',
    cover_letter_file='',
    jd_file='job_description.txt',
    ats_score={final_ats},
    hr_score={final_hr},
    application_date=None,
    status='Applied'
)
print('Tracker updated successfully')
"
```

---

## PHASE 6: CLEANUP + REPORT

1. **Collect all results** (verify DOCX + tracker)
2. **Collect base scores** from Phase 2 agent (for comparison)
3. **Delete `resume.md`** (AFTER DOCX agent confirms success — .md file is needed as input for DOCX creation)
4. **Display final report:**

```
================================================================================
                    RESUME TAILOR - FINAL REPORT (v3.0 Swarm)
================================================================================

COMPANY: {Company Name}
POSITION: {Job Title}
DOMAIN DETECTED: {clinical_research/pharma_biotech/technology/etc.}
BASE TEMPLATE: {source application folder or "Master Resume"}

--------------------------------------------------------------------------------
                         SCORING SUMMARY
--------------------------------------------------------------------------------

                    |  BASE RESUME  |  TAILORED RESUME  |  IMPROVEMENT
--------------------------------------------------------------------------------
ATS SCORE           |    {X}%       |      {Y}%         |    +{Z}%
HR SCORE            |    {X}%       |      {Y}%         |    +{Z}%
--------------------------------------------------------------------------------

ATS RATING: {Excellent/Good/Fair}
HR RECOMMENDATION: {STRONG INTERVIEW/INTERVIEW/MAYBE/PASS}

--------------------------------------------------------------------------------
                         AUTHENTICITY CHECK
--------------------------------------------------------------------------------

  [✓] Job titles preserved exactly from master resume
  [✓] Publications unchanged
  [✓] No keyword stuffing (each keyword 1-2x max)
  [✓] Bullets read naturally to human reviewer

GENERATED: {Name}_Resume_{Company}.docx
FOLDER: applications/{Company} - {JobTitle}/

================================================================================
SWARM AGENTS USED: {count} | ITERATIONS: {count}
================================================================================
```

5. **Offer** web reports:
```bash
python ats_scorer.py --web --base "{base_template}" --tailored "applications/{folder}/resume.md" --jd "applications/{folder}/job_description.txt"
python hr_scorer.py --score "applications/{folder}/{Name}_Resume_{Company}.docx" "applications/{folder}/job_description.txt" --web
```

---

## RESUME WRITING RULES (Applied during Phase 2)

**Read `.claude/commands/lib/scoring-rules.md` for the full scoring engine tables, section-by-section optimization, resume structure template, and writing coach Rules 1-14.**

Key rules:
- Modify: Summary, Core Competencies, bullet points (reframe with JD language)
- NEVER modify: Job titles, company names, dates, education, publications, certifications, memberships
- Each keyword: 1-2 times MAX. Core Competencies = primary keyword location
- ATS Phrase Match = 25% (highest weight). Insert exact JD phrases verbatim in bullets
- 50%+ bullets must have quantified metrics. 70%+ verbs at L3+ level
- No ** bold in .md files (DOCX handles formatting)
- ATS format: No columns/tables/graphics. ALL-CAPS headers. "TITLE | COMPANY | Location" format
- Bullet distribution: Current role 4-6, recent 3-4, older 2-3, very old 1-2

---

## ETHICAL REQUIREMENTS (NON-NEGOTIABLE)

- **NEVER CHANGE JOB TITLES** — Match master resume exactly (copy verbatim, including all qualifiers already in the title)
- **NEVER OMIT JOB EXPERIENCES** — All roles from the master resume must be included. Older or less-relevant roles get fewer bullets (min 1), but zero roles may be dropped.
- **NEVER CHANGE PUBLICATIONS** — Titles/citations stay as-is
- **Never invent experience** — Only reframe existing content
