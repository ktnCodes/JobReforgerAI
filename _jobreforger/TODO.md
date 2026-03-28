# ResumeForgerAI — Improvement TODO

Tracks improvements from the v5.2.0 evaluation (2026-03-27).
See [RELEASE_NOTES.md](RELEASE_NOTES.md) for completed work.

---

## Quick Wins (1-2 hours each)

- [x] **QW-1**: Fix scoring weight inconsistency across all docs (v2.0 → v2.5)
- [x] **QW-2**: Fix `explain_score` MCP tool (was returning only 10 keywords)
- [x] **QW-3**: Fix `create_cover_letter_from_md()` KeyError bug in `docx_generator.py`
- [x] **QW-4**: Create `batch_jds/` directory + `.gitkeep`
- [x] **QW-5**: Add smoke test and directory creation to `/setup`

---

## Medium Effort (half-day each)

- [x] **T2-1**: Split `resume.md` from 707 → 451 lines (extracted scoring rules to `lib/scoring-rules.md`)
- [x] **T2-2**: Deduplicate writing rules (`tailor-resume.md` now references shared `lib/scoring-rules.md`)
- [x] **T2-3**: Add "embedded/agriculture" domain to scoring engines
  - Created `data/keywords_embedded.json` (279 keywords across 18 categories)
  - Added domain detection in `ats_scorer.py` (DOMAIN_PATTERNS, DOMAIN_PROTOTYPES, _DOMAIN_KEYWORD_FILES)
  - Fixed `_suggest_alternative_titles()` in `job_fit_scorer.py` to be domain-aware (no longer healthcare-only)
- [x] **T2-4**: Add unit tests for core scoring engines
  - Created `tests/` with 39 tests across 7 files: conftest, test_ats_scorer, test_hr_scorer, test_docx_generator, test_mcp_tools, test_orchestration_state, test_score_history
  - All 39 tests passing
- [x] **T2-5**: Add error recovery to 6-phase `/resume` workflow
  - Added `check_phase_health()` and `safe_wait_for_keys()` to `orchestration_state.py`
  - Added Phase 3.5 error recovery to `resume.md` and `tailor-resume.md`
  - Background agent failures now fall back to direct scoring

---

## Larger Refactors (1-2 days each)

- [x] **T3-1**: Modularize `ats_scorer.py` and `hr_scorer.py`
  - Created `scoring/` package with `scoring/ats/` and `scoring/hr/` sub-packages
  - Package `__init__.py` files re-export full public API for organized imports
  - Backward compatible: `import ats_scorer` and `from scoring.ats import ...` both work
- [x] **T3-2**: Separate orchestration from writing in `/resume`
  - `/resume` is now a pure orchestrator (v6.0) — delegates writing to `lib/scoring-rules.md`
  - Writing rules reference is explicit: "read scoring-rules.md" instead of inline rules
  - Zero writing rules remain in `/resume` — prevents drift with `/tailor-resume`
- [x] **T3-3**: Resolve `resume_builder.py` / anthropic dependency
  - Confirmed `resume_builder.py` is legacy (no imports from it anywhere)
  - Added deprecation notice to `resume_builder.py`
  - Updated `.env.example` and `README.md` to clarify API key is legacy-only
- [x] **T3-4**: Add score history and comparison
  - Created `score_history.py` with `log_score()`, `get_history()`, `format_progression()`
  - Per-folder and global history tracking with resume hashes
  - CLI: `python score_history.py --show <folder>`
- [x] **T3-5**: Add MCP health check tool
  - Added `health_check()` MCP tool to `mcp_scorer.py`
  - Checks: SBERT status, NLTK, scorer imports, domain keywords, config validity, directories
  - Returns structured JSON with "ok" or "degraded" status

---

## All Known Issues — Status

| Issue | Status |
|-------|--------|
| Job Fit Scorer suggests pharma/clinical titles for embedded engineers | **Fixed** — `_suggest_alternative_titles()` now domain-aware |
| No "embedded/agriculture" domain in scorer | **Fixed** — new `embedded` domain with 279 keywords |
| `resume_builder.py` requires `import anthropic` but README says "no API keys" | **Fixed** — deprecated with clear docs |
| No unit tests for core scoring engines | **Fixed** — 39 tests passing |
| `ats_scorer.py` and `hr_scorer.py` are monolithic | **Improved** — `scoring/` package created for organized access |

---

## Plan Complete

All items from the v5.2.0 improvement plan have been implemented.
