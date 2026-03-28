"""
AI Resume Tuner — MCP Server (Local-Only)

Score and analyze resumes against job descriptions using dual ATS + HR scoring.
Runs entirely locally — no API keys, no subscriptions, no cloud dependencies.

Tools:
    score_resume   — Full ATS + HR analysis in one call (recommended)
    score_ats      — ATS keyword/semantic scoring only
    score_hr       — HR recruiter simulation only
    explain_score  — Actionable improvement suggestions
    discover_jobs  — Search jobs (Indeed/LinkedIn/ZipRecruiter/Glassdoor/Remotive)
    extract_text   — Read PDF/DOCX/MD/TXT files

Usage:
    fastmcp run mcp_scorer.py
"""

import os
import sys
import types
from pathlib import Path

# Load .env from project root
_env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
if os.path.isfile(_env_path):
    with open(_env_path, "r", encoding="utf-8") as _ef:
        for _line in _ef:
            _line = _line.strip()
            if _line and not _line.startswith("#") and "=" in _line:
                _k, _, _v = _line.partition("=")
                os.environ[_k.strip()] = _v.strip()

# Ensure project root is on sys.path
PROJECT_ROOT = str(Path(__file__).parent)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from fastmcp import FastMCP  # noqa: E402

mcp = FastMCP(
    "AI Resume Tuner",
    instructions=(
        "Resume optimization toolkit. Score resumes against job descriptions "
        "using ATS keyword matching and HR recruiter simulation. "
        "Supports PDF, DOCX, Markdown, and plain text. Runs fully locally."
    ),
)


# ─── Lazy-load local scorers (SBERT takes ~5s on first call) ──────────────

_scorers_loaded = False
ats_scorer: types.ModuleType = None  # type: ignore[assignment]
hr_scorer: types.ModuleType = None  # type: ignore[assignment]


def _ensure_scorers() -> None:
    global _scorers_loaded, ats_scorer, hr_scorer
    if not _scorers_loaded:
        import ats_scorer as _ats
        import hr_scorer as _hr
        ats_scorer = _ats
        hr_scorer = _hr
        _scorers_loaded = True


# ─── Tools ────────────────────────────────────────────────────────────────


@mcp.tool()
def score_resume(resume_text: str, jd_text: str) -> dict:
    """Score a resume against a job description using both ATS and HR analysis.

    This is the recommended tool for full resume evaluation. It runs:
    1. ATS scoring — keyword matching, semantic similarity, phrase matching,
       industry term recognition, and format risk assessment.
    2. HR scoring — recruiter simulation evaluating experience fit, skills match,
       career trajectory, impact signals, and competitive edge.

    Args:
        resume_text: Full text of the resume.
        jd_text: Full text of the job description.

    Returns:
        Combined results with ats_score (0-100), hr_score (0-100),
        matched/missing keywords, HR recommendation, and detailed breakdowns.
    """
    _ensure_scorers()

    ats_result = ats_scorer.calculate_ats_score(resume_text, jd_text)
    rating, likelihood, _color = ats_scorer.get_likelihood_rating(ats_result["total_score"])
    ats_result["rating"] = rating
    ats_result["likelihood"] = likelihood

    try:
        hr_result = hr_scorer.calculate_hr_score_from_text(resume_text, jd_text)
        hr_dict = hr_scorer.result_to_dict(hr_result)
    except Exception as e:
        hr_dict = {"overall_score": 0, "error": str(e)}

    ats_score = round(ats_result.get("total_score", 0), 1)
    hr_score = round(hr_dict.get("overall_score", 0), 1)

    return {
        "ats": ats_result,
        "hr": hr_dict,
        "summary": {
            "ats_score": ats_score,
            "hr_score": hr_score,
            "ats_rating": ats_result.get("rating", "Unknown"),
            "hr_recommendation": hr_dict.get("recommendation", "Unknown"),
            "assessment": _overall_assessment(ats_score, hr_score),
        },
    }


@mcp.tool()
def score_ats(resume_text: str, jd_text: str) -> dict:
    """Score a resume using ATS (Applicant Tracking System) analysis only.

    Evaluates how well a resume matches a job description through eight
    weighted components: keyword match (20%), phrase match (25%),
    industry terms (15%), semantic similarity (10%), BM25 relevance (10%),
    job title match (10%), graph centrality (5%), skill recency (5%).

    Args:
        resume_text: Full text of the resume.
        jd_text: Full text of the job description.

    Returns:
        Score (0-100) with matched/missing keywords, domain detection,
        readability analysis, format risk flags, and component breakdowns.
    """
    _ensure_scorers()
    result = ats_scorer.calculate_ats_score(resume_text, jd_text)
    rating, likelihood, _color = ats_scorer.get_likelihood_rating(result["total_score"])
    result["rating"] = rating
    result["likelihood"] = likelihood
    return result


@mcp.tool()
def score_hr(resume_text: str, jd_text: str) -> dict:
    """Score a resume using HR recruiter simulation.

    Evaluates the resume as a human hiring manager would, analyzing:
    experience fit (30%), skills match (20%), career trajectory (20%),
    impact signals (20%), and competitive edge (10%). Includes F-pattern
    visual scoring, job-hopping detection, and interview question generation.

    Args:
        resume_text: Full text of the resume.
        jd_text: Full text of the job description.

    Returns:
        Score (0-100) with recommendation (INTERVIEW/MAYBE/PASS),
        factor breakdown, strengths, concerns, and interview questions.
    """
    _ensure_scorers()
    hr_result = hr_scorer.calculate_hr_score_from_text(resume_text, jd_text)
    return hr_scorer.result_to_dict(hr_result)


@mcp.tool()
def explain_score(resume_text: str, jd_text: str) -> dict:
    """Get actionable improvement suggestions for a resume.

    Analyzes the resume against the job description using both ATS and HR
    scoring, then returns prioritized suggestions: per-component gap analysis,
    section-by-section improvement tips, quick wins, and format warnings.

    Args:
        resume_text: Full text of the resume.
        jd_text: Full text of the job description.

    Returns:
        Current ATS/HR scores, component breakdown, prioritized gaps ranked
        by weight, section-specific suggestions, and format/readability warnings.
    """
    _ensure_scorers()

    ats_result = ats_scorer.calculate_ats_score(resume_text, jd_text)
    ats_score = round(ats_result.get("total_score", 0), 1)

    try:
        hr_result = hr_scorer.calculate_hr_score_from_text(resume_text, jd_text)
        hr_dict = hr_scorer.result_to_dict(hr_result)
        hr_score = round(hr_dict.get("overall_score", 0), 1)
    except Exception:
        hr_dict = {}
        hr_score = 0

    # Component-level gap analysis (sorted by weight, highest first)
    components = [
        ("Phrase Match", 25, ats_result.get("phrase_score", 0),
         ats_result.get("missing_phrases", []),
         "Insert exact JD multi-word phrases into bullet points verbatim"),
        ("Keyword Match", 20, ats_result.get("keyword_score", 0),
         ats_result.get("missing_keywords", []),
         "Add missing keywords to Core Competencies section"),
        ("Industry Terms", 15, ats_result.get("weighted_score", 0),
         ats_result.get("missing_weighted", []),
         "Add domain-specific terms expected for this industry"),
        ("Semantic Similarity", 10, ats_result.get("semantic_score", 0),
         [], "Rewrite Summary using JD vocabulary instead of paraphrasing"),
        ("BM25 Relevance", 10, ats_result.get("bm25_score", 0),
         [], "Ensure key terms appear at least twice across the resume"),
        ("Job Title Match", 10,
         ats_result.get("job_title_match", {}).get("score", 0), [],
         "Include the exact JD title in your Professional Summary"),
        ("Graph Centrality", 5,
         ats_result.get("skill_graph", {}).get("score", 0), [],
         "Add related/adjacent skills to trigger inferred skill bonuses"),
        ("Skill Recency", 5,
         ats_result.get("skill_recency", {}).get("score", 0), [],
         "Ensure recent skills appear in your most recent role bullets"),
    ]

    gaps = []
    for name, weight, score, missing, fix in components:
        if score < 80:
            gaps.append({
                "component": name,
                "weight": f"{weight}%",
                "current_score": round(score, 1),
                "missing_items": missing[:5] if missing else [],
                "fix": fix,
            })

    # Section-specific suggestions
    section_tips = []
    if ats_result.get("semantic_score", 0) < 60:
        section_tips.append({
            "section": "Professional Summary",
            "tip": "Rewrite using JD vocabulary. Mirror exact phrasing from the job description.",
        })
    if ats_result.get("keyword_score", 0) < 70:
        section_tips.append({
            "section": "Core Competencies",
            "tip": f"Add missing keywords: {', '.join(ats_result.get('missing_keywords', [])[:7])}",
        })
    if ats_result.get("phrase_score", 0) < 70:
        section_tips.append({
            "section": "Experience Bullets",
            "tip": f"Insert exact JD phrases: {', '.join(ats_result.get('missing_phrases', [])[:5])}",
        })

    # Format and readability warnings
    warnings = []
    readability = ats_result.get("readability", {})
    details = readability.get("details", {})
    if details.get("dale_chall_score", 0) > 9.0:
        warnings.append(f"Readability too complex (Dale-Chall: {details.get('dale_chall_score', 'N/A')}). Target grade 7-8.")
    if ats_result.get("stuffing_analysis", {}).get("is_stuffed", False):
        warnings.append("Keyword stuffing detected. Reduce keyword repetition.")
    format_risk = ats_result.get("format_risk", {})
    if format_risk.get("risk_score", 0) > 50:
        warnings.append(f"High format risk ({format_risk.get('risk_score')}%). Avoid tables, text boxes, headers/footers.")

    # HR concerns
    hr_concerns = hr_dict.get("concerns", [])
    hr_strengths = hr_dict.get("strengths", [])

    return {
        "scores": {
            "ats_score": ats_score,
            "hr_score": hr_score,
            "assessment": _overall_assessment(ats_score, hr_score),
        },
        "gaps_by_priority": gaps,
        "section_suggestions": section_tips,
        "format_warnings": warnings,
        "hr_concerns": hr_concerns[:5],
        "hr_strengths": hr_strengths[:5],
        "domain_detected": ats_result.get("domain", {}).get("detected", "unknown"),
    }


@mcp.tool()
def discover_jobs(
    job_title: str,
    resume_text: str = "",
    location: str = "",
    remote_only: bool = False,
    max_results: int = 10,
) -> dict:
    """Search for jobs and score them against your resume.

    Searches Indeed, LinkedIn, ZipRecruiter, Glassdoor (via JobSpy) and
    Remotive — no API keys required. Scores each result with lightweight
    pre-screening then full ATS + HR scoring on top finalists.

    Args:
        job_title: Target job title to search for (e.g., "Data Scientist").
        resume_text: Full text of your resume (optional — improves scoring).
        location: Geographic location filter (e.g., "New York", "Remote").
        remote_only: If True, focuses on remote-only results.
        max_results: Number of top-scored jobs to return (1-20, default 10).

    Returns:
        Ranked list of jobs with ATS scores, HR scores, salary data, and apply URLs.
    """
    _ensure_scorers()
    import job_discovery as _jd
    return _jd.discover_jobs(
        resume_text=resume_text,
        job_title=job_title,
        location=location,
        remote_only=remote_only,
        max_results=max_results,
    )


@mcp.tool()
def extract_text(file_path: str) -> dict:
    """Extract text from a resume file (PDF, DOCX, Markdown, or TXT).

    Use this to read resume files that Claude can't open directly,
    such as .docx and .pdf files.

    Args:
        file_path: Path to the file (.pdf, .docx, .md, .txt).

    Returns:
        Extracted text content, detected format, and character count.
    """
    p = Path(file_path)
    if not p.exists():
        return {"error": f"File not found: {file_path}"}

    ext = p.suffix.lower()
    text = ""

    try:
        if ext == ".pdf":
            import pdfplumber
            with pdfplumber.open(str(p)) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        elif ext == ".docx":
            from docx import Document
            doc = Document(str(p))
            text = "\n".join(para.text for para in doc.paragraphs)
        elif ext in (".md", ".txt"):
            with open(str(p), "r", encoding="utf-8") as f:
                text = f.read()
        else:
            return {"error": f"Unsupported format: {ext}. Use .pdf, .docx, .md, or .txt"}
    except ImportError:
        pkg = "pdfplumber" if ext == ".pdf" else "python-docx"
        return {"error": f"Missing dependency for {ext} files. Run: pip install {pkg}"}
    except Exception as e:
        return {"error": f"Failed to read {p.name}: {e}"}

    if not text.strip():
        return {"error": f"No text extracted from {p.name}. The file may be empty or image-based."}

    return {
        "text": text.strip(),
        "format": ext,
        "char_count": len(text.strip()),
    }


# ─── Helpers ──────────────────────────────────────────────────────────────


@mcp.tool()
def health_check() -> dict:
    """Check the health of the scoring engine. Returns server version,
    SBERT model status, available tools, config validity, and domain list."""
    import time

    status = {
        "server": "AI Resume Tuner",
        "version": "5.2.0",
        "status": "ok",
        "checks": {},
    }

    # Check SBERT
    try:
        _ensure_scorers()
        sbert_ok = getattr(ats_scorer, "SBERT_AVAILABLE", False)
        if sbert_ok:
            start = time.time()
            model = ats_scorer.get_sbert_model()
            load_time = round(time.time() - start, 2)
            status["checks"]["sbert"] = {
                "available": True,
                "model": "all-MiniLM-L6-v2",
                "load_time_seconds": load_time,
            }
        else:
            status["checks"]["sbert"] = {"available": False, "reason": "sentence-transformers not installed"}
    except Exception as e:
        status["checks"]["sbert"] = {"available": False, "error": str(e)}

    # Check NLTK
    try:
        import nltk
        status["checks"]["nltk"] = {"available": True, "version": nltk.__version__}
    except ImportError:
        status["checks"]["nltk"] = {"available": False}

    # Check scorers
    try:
        _ensure_scorers()
        status["checks"]["ats_scorer"] = {"loaded": True}
        status["checks"]["hr_scorer"] = {"loaded": True}
    except Exception as e:
        status["checks"]["scorers"] = {"loaded": False, "error": str(e)}

    # Check domain keywords
    try:
        domains = list(ats_scorer._DOMAIN_KEYWORD_FILES.keys())
        status["checks"]["domains"] = {"available": domains, "count": len(domains)}
    except Exception:
        status["checks"]["domains"] = {"available": [], "count": 0}

    # Check config.json
    config_path = os.path.join(PROJECT_ROOT, "config.json")
    if os.path.isfile(config_path):
        try:
            import json
            with open(config_path, "r") as f:
                config = json.load(f)
            master = config.get("master_resume_path", "")
            master_exists = os.path.isfile(os.path.join(PROJECT_ROOT, master))
            status["checks"]["config"] = {
                "valid": True,
                "master_resume": master,
                "master_resume_exists": master_exists,
            }
        except Exception as e:
            status["checks"]["config"] = {"valid": False, "error": str(e)}
    else:
        status["checks"]["config"] = {"valid": False, "reason": "config.json not found"}

    # Check required directories
    dirs = {"applications": False, "batch_jds": False, "data": False}
    for d in dirs:
        dirs[d] = os.path.isdir(os.path.join(PROJECT_ROOT, d))
    status["checks"]["directories"] = dirs

    # Available MCP tools
    status["tools"] = [
        "score_resume", "score_ats", "score_hr",
        "explain_score", "discover_jobs", "extract_text",
        "health_check",
    ]

    # Overall status
    all_ok = (
        status["checks"].get("sbert", {}).get("available", False)
        and status["checks"].get("ats_scorer", {}).get("loaded", False)
        and status["checks"].get("hr_scorer", {}).get("loaded", False)
        and status["checks"].get("config", {}).get("valid", False)
    )
    status["status"] = "ok" if all_ok else "degraded"

    return status


def _overall_assessment(ats_score: float, hr_score: float) -> str:
    if ats_score >= 75 and hr_score >= 70:
        return "STRONG: Passes both ATS and HR evaluation. Ready to submit."
    elif ats_score >= 75 and hr_score < 70:
        return "ATS READY, HR WEAK: Will pass ATS filters but may not impress recruiters. Strengthen impact signals."
    elif ats_score < 75 and hr_score >= 70:
        return "HR STRONG, ATS WEAK: Reads well to humans but may be filtered by ATS. Add more JD keywords."
    elif ats_score >= 60 and hr_score >= 55:
        return "COMPETITIVE: Decent match with room for improvement on both ATS keywords and HR appeal."
    else:
        return "NEEDS WORK: Significant gaps in keyword matching and recruiter appeal. Major revision recommended."


if __name__ == "__main__":
    mcp.run()
