"""
HR Scoring Engine — organized package interface.

This package re-exports the public API from the monolithic hr_scorer module.
Import from here for organized access, or from hr_scorer directly for backward
compatibility.

Usage:
    from scoring.hr import calculate_hr_score_from_text, result_to_dict
    from scoring.hr import parse_resume, parse_job_description

Future: individual scoring components will be split into sub-modules
(parsing.py, skill_scoring.py, job_fit.py, etc.) and re-exported from here.
"""

import sys
import os

# Ensure project root is importable
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from hr_scorer import (
    # Data structures
    JobEntry,
    EducationEntry,
    CandidateProfile,
    JobRequirements,
    ScoreBreakdown,
    HRScoreResult,

    # Main scoring functions
    calculate_hr_score,
    calculate_hr_score_from_text,
    result_to_dict,

    # Parsing
    parse_resume,
    parse_job_description,
    parse_date,
    extract_years_from_text,
    determine_seniority_level,

    # Scoring components
    score_experience_trapezoidal,
    score_skills_contextual,
    score_impact_density,
    score_f_pattern_compliance,
    score_job_fit,
    score_competitive,
    calculate_penalties,

    # Utilities
    extract_text_from_file,
    generate_interview_questions,
)

__all__ = [
    'JobEntry',
    'EducationEntry',
    'CandidateProfile',
    'JobRequirements',
    'ScoreBreakdown',
    'HRScoreResult',
    'calculate_hr_score',
    'calculate_hr_score_from_text',
    'result_to_dict',
    'parse_resume',
    'parse_job_description',
    'parse_date',
    'extract_years_from_text',
    'determine_seniority_level',
    'score_experience_trapezoidal',
    'score_skills_contextual',
    'score_impact_density',
    'score_f_pattern_compliance',
    'score_job_fit',
    'score_competitive',
    'calculate_penalties',
    'extract_text_from_file',
    'generate_interview_questions',
]
