# ResumeForgerAI — Release Notes

---

## v5.3.0 — Full Improvement Plan Execution (2026-03-27)

All remaining items from the v5.2.0 evaluation plan have been implemented. Every known issue from v5.2.0 is resolved.

### New Features

- **Embedded/Agriculture domain** (T2-3)
  - Created `data/keywords_embedded.json` — 279 keywords across 18 categories (RTOS, firmware, CAN/J1939/ISOBUS, GNSS/RTK, precision ag, autonomous systems, etc.)
  - Added `embedded` to domain detection in `ats_scorer.py` (DOMAIN_PATTERNS, DOMAIN_PROTOTYPES, _DOMAIN_KEYWORD_FILES)
  - Kevin's embedded SW engineer resumes now correctly detect as "embedded" domain (38.6 confidence vs 26.5 for generic "technology")

- **Domain-aware alternative titles** (T2-3)
  - Rewrote `_suggest_alternative_titles()` in `job_fit_scorer.py`
  - No longer hardcoded for healthcare — now suggests embedded/technology titles (Embedded Software Engineer, Firmware Engineer, Controls Engineer, etc.) when domain matches
  - Added experience type detection for `embedded_software`, `software_engineering`, `controls_automation`, `systems_engineering`

- **Score history tracking** (T3-4)
  - New `score_history.py` module with `log_score()`, `get_history()`, `format_progression()`, `hash_resume()`
  - Per-folder and global history in `score_history.json` files
  - CLI: `python score_history.py --show <folder>` for progression tables
  - Enables A/B testing of rule changes

- **MCP health check tool** (T3-5)
  - New `health_check()` MCP tool in `mcp_scorer.py`
  - Checks: SBERT model, NLTK, scorer imports, 8 domain keyword files, config.json validity, required directories
  - Returns structured JSON with "ok" or "degraded" status

### Testing

- **Unit test suite** (T2-4) — 39 tests across 7 files, all passing
  - `test_ats_scorer.py` — 9 tests: return shape, weight sums, score ranges, domain detection, keyword analysis
  - `test_hr_scorer.py` — 5 tests: return types, score ranges, quality comparison, recommendation values
  - `test_docx_generator.py` — 3 tests: resume DOCX, cover letter DOCX, KeyError fix verification
  - `test_mcp_tools.py` — 3 tests: combined scoring, explain_score gaps, text extraction
  - `test_orchestration_state.py` — 13 tests: init/update/phase/error/cleanup + health check + safe_wait
  - `test_score_history.py` — 6 tests: hashing, logging, retrieval, progression formatting

### Error Recovery

- **Phase 3.5 error recovery** (T2-5)
  - Added `check_phase_health()` to `orchestration_state.py` — non-blocking diagnostic for background agent status
  - Added `safe_wait_for_keys()` — returns `(state, error)` tuple instead of raising on timeout
  - `/resume` and `/tailor-resume` now include Phase 3.5: if background agents fail, falls back to direct scoring

### Architecture

- **Scoring package structure** (T3-1)
  - Created `scoring/` package with `scoring/ats/` and `scoring/hr/` sub-packages
  - `__init__.py` files re-export full public API for organized imports
  - Backward compatible: both `import ats_scorer` and `from scoring.ats import ...` work

- **Orchestrator separation** (T3-2)
  - `/resume` is now a pure orchestrator (v6.0) — zero inline writing rules
  - Writing delegated to shared `lib/scoring-rules.md` (single source of truth)
  - Prevents rule drift between `/resume`, `/tailor-resume`, and `/writing-coach`

- **Legacy CLI deprecated** (T3-3)
  - `resume_builder.py` marked deprecated (superseded by slash commands)
  - `.env.example` and `README.md` updated to clarify API key is legacy-only
  - No files import from `resume_builder.py` — safe to remove in future

### v5.2.0 Known Issues — All Resolved

| Issue | Resolution |
|-------|-----------|
| Pharma/clinical alt titles for embedded engineers | Fixed — domain-aware title suggestions |
| No embedded/agriculture domain | Fixed — `embedded` domain with 279 keywords |
| `resume_builder.py` anthropic contradiction | Fixed — deprecated with docs updated |
| No unit tests | Fixed — 39 tests passing |
| No error recovery in 6-phase workflow | Fixed — Phase 3.5 with fallback |
| Monolithic scorer files | Improved — `scoring/` package for organized access |

---

## v5.2.0 — Tool Evaluation & Quality Pass (2026-03-27)

Comprehensive tool evaluation against the master resume, with bug fixes and architectural improvements based on findings.

### Evaluation Results

Ran the master resume (KEVIN_MASTER_RESUME.md) against a well-matched Embedded Software Engineer JD:
- **ATS Score**: 54.8% (Fair) — expected for untailored resume
- **HR Score**: 66.2% (MAYBE) — flagged long bullets, 16-month avg tenure
- **Job Fit Score**: 74.7 (MODERATE FIT) — no knockout disqualifiers

### Tool Ratings

| Dimension | Rating | Notes |
|---|---|---|
| Ease of Use | 6/10 | Good docs, but setup gaps and silent failures |
| LLM-Friendliness | 4/10 | 702-line mega-prompt is the main liability |
| `/job-fit` | 8/10 | Best feature — short, focused, genuinely useful |
| `/resume` | 5/10 | Comprehensive but fragile multi-agent orchestration |
| `explain_score` MCP | 2/10 | Was returning only 10 keywords + generic string |

### Bug Fixes

- **Fixed: Scoring weight inconsistency across all docs**
  - `CLAUDE.md` and `resume.md` referenced stale v2.0 weights (Keyword 22%, Phrase 13%)
  - Actual code uses v2.5 weights (Phrase Match **25%**, Keyword Match 20%)
  - Claude was making wrong iteration decisions during resume optimization
  - Updated all weight references in `CLAUDE.md`, `resume.md` iteration trees, scoring cheat sheet, and section-specific targets

- **Fixed: `explain_score` MCP tool massively under-delivering**
  - Before: returned `missing_keywords[:10]` + generic suggestion string
  - After: returns full component gap analysis (sorted by weight), HR concerns/strengths, section-specific suggestions, format/readability warnings, and domain detection
  - File: `mcp_scorer.py`

- **Fixed: `create_cover_letter_from_md()` KeyError bug**
  - `docx_generator.py:568` — `recipient_info['company']` used direct dict access
  - Fixed to `recipient_info.get('company')` with guard clause
  - Removed workaround comment from `resume.md` Global Constraints

### Architectural Improvements

- **Split `resume.md` from 707 to 451 lines (36% reduction)**
  - Extracted scoring engine tables, JD deconstruction protocol, section-by-section optimization, resume structure template, bullet distribution, writing coach Rules 1-14, and scoring cheat sheet
  - New shared reference file: `.claude/commands/lib/scoring-rules.md` (255 lines)
  - `resume.md` now references the shared file instead of inlining 260 lines of rules

- **Deduplicated writing rules across commands**
  - `tailor-resume.md` reduced from 299 to 218 lines
  - Writing rules, resume structure, and verb bank replaced with reference to shared `lib/scoring-rules.md`
  - Prevents drift between `/resume`, `/tailor-resume`, and `/writing-coach`

- **Created `batch_jds/` directory**
  - Required by `/batch-resume` but did not exist
  - Added `.gitkeep` for git tracking

- **Enhanced `/setup` command**
  - Added directory creation step (applications/, batch_jds/)
  - Added end-to-end smoke test (imports + minimal ATS/HR scoring)
  - Added `/job-fit` and `/batch-resume` to the success message command list

### Known Issues Identified

- Job Fit Scorer suggests pharma/clinical alternative titles (Medical Monitor, Drug Safety Physician) for embedded software engineers — alternative title generator appears hardcoded for healthcare domain
- No "embedded/agriculture" domain in scorer — Kevin's actual domain defaults to "technology"
- `resume_builder.py` requires `import anthropic` but README says "no API keys needed"
- No unit tests for core scoring engines
- No error recovery in the 6-phase `/resume` workflow
- `ats_scorer.py` (119KB) and `hr_scorer.py` (131KB) are monolithic single files
