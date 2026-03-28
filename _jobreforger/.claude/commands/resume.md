# Resume Builder — Orchestrator v6.0 (Swarm)

Orchestrate a full application package (resume + cover letter) using parallel agent execution. This command is a **pure orchestrator** — it delegates resume writing to `/tailor-resume` logic and cover letter to `/cover-letter` logic.

## Job Description
$ARGUMENTS

## Instructions

You are a parallel-agent orchestrator managing the full resume + cover letter workflow. You will:
1. Run a job fit pre-check (knockout detection)
2. Delegate resume writing using the scoring-aware rules from `lib/scoring-rules.md`
3. Generate a cover letter in parallel with scoring
4. Score, iterate, finalize DOCX files, and report results
5. Use error recovery if background agents fail

---

## GLOBAL CONSTRAINTS (read first, enforce always)

- NEVER change job titles, company names, dates, education, publications, certifications, or memberships
- NEVER add parenthetical qualifiers to job titles — titles must match the master resume exactly, with no additions or removals.
- NEVER omit any job experience entry — every role in the master resume must appear in the tailored resume. Reduce bullet count for older/less-relevant roles (minimum 1 bullet each), but NEVER drop an entire role.
- NEVER use `**bold**` markdown in `.md` files — the DOCX generator handles bold automatically
- NEVER exceed 2 appearances of any single keyword across the entire resume
- Publications & Education: Keep EXACTLY as in master resume — zero modifications
- Cover letter DOCX: Use `create_ats_cover_letter()` directly or `create_cover_letter_from_md()` — both work correctly
- Score targets: ATS 75-85%, HR 70%+. If JD contains staffing/benefits boilerplate, ATS ceiling is ~69-73% — accept once all domain weights are maxed. Max 2 iterations against a boilerplate ceiling.

---

## PHASE 0.5: JOB FIT PRE-CHECK (mandatory gate)

Before investing time in tailoring, run the Job Fit Scorer to check for knockout disqualifiers:

```python
from job_fit_scorer import calculate_job_fit, format_report
result = calculate_job_fit(resume_text, jd_text)
```

**Decision gate:**
- **STRONG FIT (75+)**: Proceed to Phase 1.
- **MODERATE FIT (55-74)**: Proceed — show the user fixable gaps and note them for Phase 2 writing.
- **WEAK FIT (35-54)**: PAUSE. Show the user the report and ask: "This job is a weak fit (score: X). [Show knockouts/gaps]. Continue anyway?"
- **NO-GO (<35 or hard knockouts)**: STOP. Show the full report with knockouts and alternative job titles. Do NOT proceed to Phase 1. Tell the user: "This job has disqualifying requirements: [list knockouts]. Better-fit roles for your profile: [alternatives]."

Display the fit score, any knockouts, and key dimensions before proceeding.

---

## PHASE 1: PARALLEL RESEARCH + JD DECONSTRUCTION (launch all simultaneously)

Execute these 3 actions in a single parallel tool call (no agents needed — use Read, Glob, and Write tools simultaneously):

Action A — Find best matching resume:
- Use `Glob` to find all `applications/**/*Resume*.docx` files
- From the folder names (format: `{Company} - {JobTitle}`), identify the most semantically similar role to the new JD (same domain, similar responsibilities, overlapping keywords)
- If a match is found (PREFERRED): Read the `.docx` using Python via Bash: `python -c "from docx import Document; [print(p.text) for p in Document('path').paragraphs]"`
- If no match found: Fall back to the master resume (read `config.json` for `master_resume_path`, or glob for `*MASTER*RESUME*.md`, `*MASTER*RESUME*.docx`, `*MASTER*RESUME*.pdf`)

Action B — Read master resume:
- Read the master resume (path from `config.json` → `master_resume_path`) for canonical job titles, dates, company names, education, certifications, publications, and memberships (these NEVER change)
- **Format-aware reading:** `.md`/`.txt` → use `Read` tool directly. `.pdf` → use `Read` tool directly (Claude handles PDFs natively). `.docx` → call `extract_text` MCP tool with the file path (Claude cannot read binary DOCX files directly).

Action C — Setup output + initialize orchestration state:
- Extract company name and job title from JD
- Create output folder: `applications/{CompanyName} - {JobTitle}/`
- Save JD as `job_description.txt` in the output folder
- Initialize shared state via Bash:
```
cd "." && python -c "
from orchestration_state import init_state
init_state('applications/{folder}', '{Company}', '{JobTitle}', 'applications/{folder}/job_description.txt', '{base_template}')
print('State initialized')
"
```

THEN — Before writing anything, complete the JD Deconstruction (see STEP 1 in Scoring-Aware Writing Rules below). This takes 30 seconds and prevents generic, under-optimized drafts.

---

## PHASE 2: BACKGROUND BASE SCORING + IMMEDIATE RESUME WRITING

Launch background Bash agents AND start writing immediately — do NOT wait for base scores.

Base scores are only needed for the final comparison report, NOT for writing the resume.

Background Agent A — Combined Base Score (ATS + HR) → writes to state.json:
```
Use Task tool (subagent_type: "Bash", run_in_background: true, name: "base-scorer"):
cd "." && python ats_scorer.py --score "{base_template_path}" "applications/{folder}/job_description.txt" --json && python hr_scorer.py --score "{base_template_path}" "applications/{folder}/job_description.txt" --json
```

MAIN AGENT — Generate the tailored resume by following the `/tailor-resume` writing protocol:
- Read `.claude/commands/lib/scoring-rules.md` for JD deconstruction, section-by-section optimization, resume structure template, and writing coach Rules 1-14
- Apply Phase 0.5 job-fit results (fixable gaps become writing priorities)
- Follow the ETHICAL REQUIREMENTS section below (non-negotiable)

Save as `resume.md` in the output folder when done, then update state:
```
cd "." && python -c "
from orchestration_state import update_state, set_phase
update_state('applications/{folder}', 'tailored_resume_path', 'applications/{folder}/resume.md')
set_phase('applications/{folder}', 'writing')
print('State updated: resume path + phase=writing')
"
```

CRITICAL .md FORMATTING RULE: Do NOT use `**` (markdown bold asterisks) anywhere in resume.md or cover_letter.md files. Write metrics and text as plain text (e.g., "11,300+ ICU stays" not "**11,300+ ICU stays**"). The DOCX generator handles bold formatting automatically.

---

## PHASE 3: PARALLEL SCORING + COVER LETTER (launch all simultaneously)

Once `resume.md` is saved, launch 3 agents in a single parallel tool call:

Background Agent C — Combined Tailored Score (ATS + HR):
```
Use Task tool (subagent_type: "Bash", run_in_background: true, name: "tailored-scorer"):
cd "." && python ats_scorer.py --score "applications/{folder}/resume.md" "applications/{folder}/job_description.txt" --json && python hr_scorer.py --score "applications/{folder}/resume.md" "applications/{folder}/job_description.txt" --json
```

Background Agent E — Cover Letter:
```
Use Task tool (subagent_type: "general-purpose", run_in_background: true, name: "cover-letter-writer"):
Prompt: "Generate a one-page cover letter (350-400 words) for {Name} applying to {Job Title} at {Company}.

JD: [paste full JD text]

Resume bullets to reference: [paste the key achievements from the tailored resume]

Structure (4 paragraphs):
P1 — Hook (50-60 words): Lead with a specific metric achievement + direct connection to what this role needs. Name the role and company. Lead with a number.
P2 — Proof Point 1 (80-100 words): STAR story for strongest JD-relevant experience. Use at least 1 exact JD noun phrase. Include a metric.
P3 — Proof Point 2 (80-100 words): STAR story for secondary JD requirement. Include a metric with magnitude ($M or multiplier preferred).
P4 — Close (50-60 words): Forward-looking statement tied to company mission or pipeline + call to action. Confident, not pleading. No 'I would welcome the opportunity.'

Tone: Senior professional writing to peers, not a job-seeker writing to gatekeepers. Confident, specific, evidence-based.
- Do NOT use ** markdown bold — write metrics as plain text
- At least 2 exact JD phrases used across the letter
- At least 2 quantified metrics included
- No sentence exceeds 25 words
- Total word count 350-400
- Save the cover letter text to: applications/{folder}/cover_letter.md

Contact info:
Name: {user_name from config.json}
Address: {user_city, user_state from config.json}
Phone: {user_phone from config.json}
Email: {user_email from config.json}"
```

---

## PHASE 3.5: ERROR RECOVERY CHECK

Before reading scores, verify that background agents completed successfully:

```python
from orchestration_state import check_phase_health, safe_wait_for_keys

# Check if scoring agents finished
health = check_phase_health(
    'applications/{folder}',
    expected_keys=['tailored_scores'],
    phase_name='scoring_tailored'
)

if not health['healthy']:
    # Try waiting up to 60s for slow agents
    state, err = safe_wait_for_keys(
        'applications/{folder}',
        ['tailored_scores'],
        timeout=60
    )
    if err:
        # Agents failed — fall back to direct (non-background) scoring
        print(f"Background agents failed: {err}")
        print("Falling back to direct scoring...")
```

**If background scoring agents failed or timed out**, fall back to direct scoring:
```bash
python ats_scorer.py --score "applications/{folder}/resume.md" "applications/{folder}/job_description.txt" --json
python hr_scorer.py --score "applications/{folder}/resume.md" "applications/{folder}/job_description.txt" --json
```
Parse the JSON output directly instead of reading from state.json.

**If the cover letter agent failed**, generate the cover letter directly in the main conversation (not as a background agent). The resume scoring and iteration should not be blocked by cover letter generation.

---

## PHASE 4: PRECISION DIAGNOSIS + ITERATION (max 3 rounds)

1. Collect all three scores from state.json (single read replaces polling multiple agent outputs):
```
cd "." && python -c "
from orchestration_state import read_state
import json
state = read_state('applications/{folder}')
ts = state.get('tailored_scores', {})
# Combined (blended) scores — these are the primary decision scores
combined_ats = ts.get('combined_ats', ts.get('ats', {}).get('total', 'pending'))
combined_hr = ts.get('combined_hr', ts.get('hr', {}).get('total', 'pending'))
print(f'=== COMBINED (70% rules + 30% LLM) ===')
print(f'ATS: {combined_ats}%')
print(f'HR:  {combined_hr}%')
# Individual scorer breakdown
rules_ats = ts.get('rules_ats', {})
rules_hr = ts.get('rules_hr', {})
llm = ts.get('llm', {})
print(f'--- Rules-based ---')
print(f'ATS (rules): {rules_ats.get(\"total_score\", \"?\")}%')
print(f'HR  (rules): {rules_hr.get(\"overall_score\", \"?\")}%')
print(f'--- LLM (Claude) ---')
print(f'ATS (LLM): {llm.get(\"ats_score\", \"?\")}%')
print(f'HR  (LLM): {llm.get(\"hr_score\", \"?\")}%')
if llm.get('explanation'):
    print(f'LLM says: {llm[\"explanation\"]}')
blend = ts.get('blend_details', {})
print(f'Blend method: {blend.get(\"method\", \"unknown\")}')
if state.get('errors'):
    print(f'Errors: {json.dumps(state[\"errors\"], indent=2)}')
"
```
Use the COMBINED scores for iteration decisions (they incorporate LLM semantic understanding).
2. Diagnose BEFORE editing — follow the decision trees in Step 3 of Scoring-Aware Writing Rules below. Fix the highest-weighted gap first.

IF ATS < 75%:
```
1. Phrase Match (25%) — Are exact 2-4 word JD phrases appearing verbatim?
   FIX: Insert 1-2 exact JD phrases into bullets naturally
2. Keyword Match (20%) — Are all high-frequency JD nouns in Core Competencies?
   FIX: Add missing JD keywords to Core Competencies
3. Weighted Industry Terms (15%) — Are all domain-critical keywords present?
   FIX: Add missing domain terms to Core Competencies
4. Semantic Similarity (10%) — Is Summary using JD vocabulary or paraphrased vocabulary?
   FIX: Rewrite Summary sentences 2-3 to mirror JD phrasing exactly
5. BM25 (10%) — Are key terms appearing at least twice but not more than twice?
   FIX: Add one natural repetition of under-represented terms
6. Job Title Match (10%) — Does the resume header/summary contain the JD title?
   FIX: Include exact or close JD title in Professional Summary
STOP if boilerplate ceiling applies (~69-73%). Max 2 iteration cycles.
```

IF ATS >= 75% AND HR < 70%:
```
1. Job Fit (25%) — Are domain-defining terms in first 100 words?
   FIX: Rewrite Summary sentence 1 to lead with domain identity
2. Skills Match (20%) — Are skills IN ACTION (verb + skill + metric) or just listed?
   FIX: Reframe 2-3 listed skills as action bullets (2x weight multiplier)
3. Experience Fit (20%) — Does Summary explicitly state years of experience?
   FIX: Ensure Summary mentions years matching JD minimum +/- 3 yrs
4. Impact Signals (15%) — Do 50%+ of bullets contain metrics?
   FIX: Add metrics to bare bullets. Move highest-magnitude metric to bullet 1.
5. Competitive Edge (10%) — Are prestige signals (top companies/universities) appearing early?
   FIX: Name-drop in Summary sentence 1 or 3
```

IF ATS >= 75% AND HR >= 70%:
   PASS — proceed to finalization

Re-score after each iteration:
```bash
python ats_scorer.py --score "applications/{folder}/resume.md" "applications/{folder}/job_description.txt" --json
python hr_scorer.py --score "applications/{folder}/resume.md" "applications/{folder}/job_description.txt" --json
```

Iteration protocol:
| Iteration | Focus | Stop Condition |
|-----------|-------|----------------|
| 1 | Fix top 2 gaps from diagnosis | Re-score |
| 2 | Fix remaining gaps if still below target | Re-score |
| 3 | Micro-adjustments only (single word/phrase swaps) | Accept if within 3 pts of target |
| MAX | Do not exceed 3 iterations | Diminishing returns / risk of over-optimization |

Anti-patterns to avoid during iteration:
- Stuffing keywords that don't match real experience
- Inflating metrics beyond defensible truth
- Breaking readability grade above 12 with complex rewrites
- Removing metrics to make room for keywords (metrics are 15% of HR)
- Editing Publications or Education sections

---

## PHASE 5: PARALLEL FINALIZATION (launch all 3 simultaneously)

Once scores pass AND cover letter is ready, set phase to finalizing and launch 3 agents in a single parallel tool call:
```
cd "." && python -c "from orchestration_state import set_phase; set_phase('applications/{folder}', 'finalizing')"
```

Background Agent F — Resume DOCX (from markdown) → updates state.json:
```
Use Task tool (subagent_type: "Bash", run_in_background: true, name: "resume-docx-creator"):
cd "." && python -c "
from docx_generator import create_resume_from_md
from orchestration_state import update_state, log_error
try:
    create_resume_from_md('applications/{folder}/resume.md', 'applications/{folder}/{Name}_Resume_{Company}.docx')
    update_state('applications/{folder}', 'docx_resume_path', 'applications/{folder}/{Name}_Resume_{Company}.docx')
    print('Resume DOCX created successfully')
except Exception as e:
    log_error('applications/{folder}', 'finalizing', f'Resume DOCX failed: {e}')
    print(f'Error: {e}')
"
```

Background Agent G — Cover Letter DOCX (ALWAYS use create_ats_cover_letter directly) → updates state.json:
```
Use Task tool (subagent_type: "Bash", run_in_background: true, name: "cover-letter-docx-creator"):
cd "." && python -c "
from docx_generator import create_ats_cover_letter
from orchestration_state import update_state, log_error
try:
    with open('applications/{folder}/cover_letter.md', 'r') as f:
        content = f.read()
    lines = [l.strip() for l in content.split('\n') if l.strip()]
    body_paragraphs = []
    skip_patterns = [config_name.split()[0], config_city, config_phone[:7], 'Dear', 'Sincerely', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December', 'January', 'Hiring Manager', 'Re:']
    for line in lines:
        if not any(p in line for p in skip_patterns) and len(line) > 50:
            body_paragraphs.append(line)
    create_ats_cover_letter(
        output_path='applications/{folder}/{Name}_Cover_Letter_{Company}.docx',
        name='{user_name from config.json}',
        contact_info={'city': '{city}', 'state': '{state}', 'phone': '{phone}', 'email': '{email}'},
        date='{date}',
        recipient_info={'name': 'Hiring Manager', 'company': '{Company}', 'title': ''},
        job_title='{Job Title}',
        paragraphs=body_paragraphs[:4],
        closing='Sincerely'
    )
    update_state('applications/{folder}', 'docx_cover_letter_path', 'applications/{folder}/{Name}_Cover_Letter_{Company}.docx')
    print('Cover Letter DOCX created successfully')
except Exception as e:
    log_error('applications/{folder}', 'finalizing', f'Cover Letter DOCX failed: {e}')
    print(f'Error: {e}')
"
```

Background Agent H — Update Tracker → updates state.json:
```
Use Task tool (subagent_type: "Bash", run_in_background: true, name: "tracker-updater"):
cd "." && python -c "
from tracker_utils import add_application
from orchestration_state import update_state, log_error
try:
    add_application(
        company='{Company}',
        job_title='{Job Title}',
        resume_file='{Name}_Resume_{Company}.docx',
        cover_letter_file='{Name}_Cover_Letter_{Company}.docx',
        jd_file='job_description.txt',
        ats_score={final_ats},
        hr_score={final_hr},
        application_date=None,
        status='Applied'
    )
    update_state('applications/{folder}', 'tracker_updated', True)
    print('Tracker updated successfully')
except Exception as e:
    log_error('applications/{folder}', 'finalizing', f'Tracker update failed: {e}')
    print(f'Error: {e}')
"
```

---

## PHASE 6: CLEANUP + REPORT

1. Read final state from state.json (single source of truth for all agent results):
```
cd "." && python -c "
from orchestration_state import read_state, set_phase, cleanup_state
import json
state = read_state('applications/{folder}')
set_phase('applications/{folder}', 'done')
print(json.dumps(state, indent=2))
# Check for any errors logged during the run
errors = state.get('errors', [])
if errors:
    print(f'\nWARNING: {len(errors)} error(s) during run:')
    for e in errors: print(f'  [{e[\"phase\"]}] {e[\"message\"]}')
"
```
2. Extract base_scores and tailored_scores from the state dict for the comparison report
3. Delete intermediate files: `resume.md`, `cover_letter.md`, and `state.json` (AFTER verifying DOCX paths exist in state)
```
cd "." && python -c "
from orchestration_state import cleanup_state
import os
for f in ['applications/{folder}/resume.md', 'applications/{folder}/cover_letter.md']:
    if os.path.exists(f): os.remove(f)
cleanup_state('applications/{folder}')
print('Cleanup complete')
"
```
4. Display final report:

```
================================================================================
          RESUME BUILDER - FINAL REPORT (v5.1 Triple-Scorer Swarm)
================================================================================

COMPANY: {Company Name}
POSITION: {Job Title}
DOMAIN DETECTED: {clinical_research/pharma_biotech/technology/etc.}
BASE TEMPLATE: {source application folder or "Master Resume"}

--------------------------------------------------------------------------------
                    COMBINED SCORES (70% Rules + 30% LLM)
--------------------------------------------------------------------------------

                    |  BASE RESUME  |  TAILORED RESUME  |  IMPROVEMENT
--------------------------------------------------------------------------------
COMBINED ATS        |    {X}%       |      {Y}%         |    +{Z}%
COMBINED HR         |    {X}%       |      {Y}%         |    +{Z}%
--------------------------------------------------------------------------------

--------------------------------------------------------------------------------
                    SCORER BREAKDOWN — TAILORED RESUME
--------------------------------------------------------------------------------

                    |  ATS (Rules)  |  HR (Rules)  |  ATS (LLM)  |  HR (LLM)
--------------------------------------------------------------------------------
SCORES              |    {X}%       |    {Y}%      |    {X}%     |    {Y}%
--------------------------------------------------------------------------------
  ATS Components:
  - Keywords        |    {X}%       |
  - Semantic        |    {X}%       |
  - Phrases         |    {X}%       |
  - BM25            |    {X}%       |

  HR Factors:
  - Experience      |               |    {Y}%      |
  - Skills          |               |    {Y}%      |
  - Impact          |               |    {Y}%      |
  - Job Fit         |               |    {Y}%      |
--------------------------------------------------------------------------------

  LLM INSIGHT: {llm_explanation from state.json}

--------------------------------------------------------------------------------
                         AUTHENTICITY CHECK
--------------------------------------------------------------------------------

  [x] Job titles preserved exactly from master resume
  [x] Publications unchanged
  [x] No keyword stuffing (each keyword appears 1-2x max)
  [x] Bullets read naturally to human reviewer

--------------------------------------------------------------------------------
                         GENERATED FILES
--------------------------------------------------------------------------------

  [x] {Name}_Resume_{Company}.docx
  [x] {Name}_Cover_Letter_{Company}.docx
  [x] job_description.txt

FOLDER: applications/{Company} - {JobTitle}/

================================================================================
SCORERS: 3 (ATS Rules + HR Rules + LLM Claude)
SWARM AGENTS USED: {count} | ITERATIONS: {count}
================================================================================
```

5. Offer to open web comparison reports:
```bash
python ats_scorer.py --web --base "{base_template}" --tailored "applications/{folder}/resume.md" --jd "applications/{folder}/job_description.txt"
python hr_scorer.py --score "applications/{folder}/{Name}_Resume_{Company}.docx" "applications/{folder}/job_description.txt" --web
```

---

## WRITING RULES REFERENCE (delegated to shared rules)

Resume writing is governed by `.claude/commands/lib/scoring-rules.md` (the single source of truth shared with `/tailor-resume` and `/writing-coach`). The orchestrator does NOT contain its own writing rules — this prevents drift.

Key score targets: ATS Phrase Match 25%, Keyword Match 20%, Job Title Match 10%. HR Job Fit 25%, Experience 20%, Skills 20%.

---

## ETHICAL REQUIREMENTS (NON-NEGOTIABLE)

- NEVER CHANGE JOB TITLES — Must match master resume exactly (copy verbatim, including all qualifiers already in the title)
- NEVER OMIT JOB EXPERIENCES — All roles from the master resume must be included. Older or less-relevant roles get fewer bullets (min 1), but zero roles may be dropped.
- NEVER CHANGE PUBLICATIONS — Titles and citations stay as-is
- Never invent experience — Only reframe existing content
- Keywords go in: Core Competencies (primary), Summary (3-5 terms), select bullets
- Keywords do NOT go in: Titles, company names, education, publications, certifications, memberships
