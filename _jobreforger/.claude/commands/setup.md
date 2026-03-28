# Resume Builder — One-Time Setup

Run this command once after installing the plugin to enable the advanced ATS/HR scoring engine.

## Input
$ARGUMENTS

## Instructions

You are helping the user set up the Resume Builder plugin's scoring engine. This is a one-time setup that installs Python dependencies needed for the MCP-based ATS and HR scorers.

### Step 1: Check Python

Run `python --version` (or `python3 --version` on Mac/Linux).

- If Python 3.10+ is installed, proceed to Step 2.
- If Python is NOT installed, tell the user:

```
The scoring engine requires Python 3.10 or later.

Download it from: https://www.python.org/downloads/

During installation:
- CHECK "Add Python to PATH" (Windows)
- Mac/Linux: Use your package manager (brew install python3)

After installing Python, run /resume-builder:setup again.
```

Stop here if Python is not installed.

### Step 2: Install Dependencies

Run this command to install all required packages:

```bash
pip install -r requirements.txt
```

If `pip` is not found, try `pip3 install -r requirements.txt` or `python -m pip install -r requirements.txt`.

The requirements file is located in the plugin directory. Use `${CLAUDE_PLUGIN_ROOT}/requirements.txt` if needed.

Wait for it to complete. This may take 1-3 minutes (sentence-transformers downloads a ~80MB model).

### Step 3: Set Up Configuration

Check if the user has a `config.json` in their project. If not, create one from `config.example.json`:

1. Read `config.example.json` from the plugin directory
2. Ask the user for their details:
   - Full name
   - Credentials (e.g., M.D., MBA, CPA — or leave blank)
   - Email
   - Phone
   - LinkedIn URL
   - Path to their master resume file (supported formats: .docx, .pdf, .md, or .txt)
3. Create `config.json` with their answers

### Step 4: Create Required Directories

Ensure the following directories exist (create if missing):

```bash
mkdir -p applications
mkdir -p batch_jds
```

- `applications/` — Output folder for tailored resumes and cover letters
- `batch_jds/` — Place `.txt` JD files here for `/batch-resume` processing (naming: `{Company} - {Job Title}.txt`)

### Step 5: Verify and Smoke Test

Run a quick test to verify everything works:

```bash
python -c "
import ats_scorer, hr_scorer, job_fit_scorer
print('All scorers imported OK')

# Smoke test: score a minimal resume against a minimal JD
score = ats_scorer.calculate_ats_score('Software Engineer with 3 years Python experience', 'Looking for a Software Engineer with Python')
print(f'ATS smoke test: {score[\"total_score\"]:.1f}%')

hr = hr_scorer.calculate_hr_score_from_text('Software Engineer with 3 years Python experience', 'Looking for a Software Engineer with Python')
hr_dict = hr_scorer.result_to_dict(hr)
print(f'HR smoke test: {hr_dict[\"overall_score\"]:.1f}%')

print('Scoring engine ready!')
"
```

If successful, tell the user:

```
Setup complete! You can now use:

  /resume [paste job description]         — Full resume + cover letter package
  /tailor-resume [paste JD]               — Resume only
  /cover-letter [paste JD]               — Cover letter only
  /writing-coach [resume file]            — Improve resume writing quality
  /find-jobs [job title] [location]       — Discover & score matching jobs
  /job-fit [paste JD]                     — Quick GO/NO-GO fit check
  /batch-resume                           — Process multiple JDs from batch_jds/ folder

The ATS/HR scoring engine is now active and will automatically score your resumes.
```

If it fails, show the error and suggest fixes.
