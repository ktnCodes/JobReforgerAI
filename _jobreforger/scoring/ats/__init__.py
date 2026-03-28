"""
ATS Scoring Engine — organized package interface.

This package re-exports the public API from the monolithic ats_scorer module.
Import from here for organized access, or from ats_scorer directly for backward
compatibility.

Usage:
    from scoring.ats import calculate_ats_score, detect_domain
    from scoring.ats import extract_jd_keywords, check_job_title_match

Future: individual scoring components will be split into sub-modules
(semantic.py, bm25.py, domain.py, etc.) and re-exported from here.
"""

import sys
import os

# Ensure project root is importable
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from ats_scorer import (
    # Primary scoring function
    calculate_ats_score,
    score_resume,
    score_resume_text,
    get_likelihood_rating,

    # Domain detection
    detect_domain,
    load_domain_keywords,
    load_domain_phrases,
    get_domain_keywords_for_text,

    # Keyword/phrase extraction and matching
    extract_jd_keywords,
    extract_keywords,
    extract_phrases,
    check_job_title_match,
    calculate_keyword_match,
    calculate_phrase_match,

    # Semantic/embedding functions
    embed_with_cache,
    calculate_semantic_similarity,
    calculate_bm25_score,

    # NLP utilities
    lemmatize_word,
    lemmatize_text,
    expand_acronyms,
    is_valid_skill,

    # Format and quality assessment
    assess_format_risk,
    detect_keyword_stuffing,
    calculate_readability,
    detect_hidden_text,

    # Skill analysis
    calculate_skill_decay,
    extract_skills_with_recency,
    calculate_recency_adjusted_score,
    build_skill_graph,
    infer_skills_from_graph,
    calculate_graph_centrality_score,

    # Text extraction
    extract_text_from_file,

    # Module-level constants
    SBERT_AVAILABLE,
    SYNONYM_MAP,
)

# Optional imports that may not always be available
try:
    from ats_scorer import sbert_util
except ImportError:
    sbert_util = None

__all__ = [
    'calculate_ats_score',
    'score_resume',
    'score_resume_text',
    'get_likelihood_rating',
    'detect_domain',
    'load_domain_keywords',
    'load_domain_phrases',
    'get_domain_keywords_for_text',
    'extract_jd_keywords',
    'extract_keywords',
    'extract_phrases',
    'check_job_title_match',
    'calculate_keyword_match',
    'calculate_phrase_match',
    'embed_with_cache',
    'calculate_semantic_similarity',
    'calculate_bm25_score',
    'lemmatize_word',
    'lemmatize_text',
    'expand_acronyms',
    'is_valid_skill',
    'assess_format_risk',
    'detect_keyword_stuffing',
    'calculate_readability',
    'detect_hidden_text',
    'calculate_skill_decay',
    'extract_skills_with_recency',
    'calculate_recency_adjusted_score',
    'build_skill_graph',
    'infer_skills_from_graph',
    'calculate_graph_centrality_score',
    'extract_text_from_file',
    'SBERT_AVAILABLE',
    'SYNONYM_MAP',
    'sbert_util',
]
