"""
config.py
=========
Central configuration module for the Student Performance Prediction System.

Design rationale
-----------------
This module follows the "single source of truth" principle. All file paths,
grade thresholds, column mappings, and application-wide constants live here.
No other module should hardcode a path or a magic number -- they import
from this file instead.

Why this matters for a real deployment:
    If this system were deployed at an actual institution, grading scales,
    file locations, or logging behaviour could change per-institution.
    Centralizing configuration means such changes require editing ONE file,
    not hunting through the entire codebase.

This module contains no DSA logic -- it is pure configuration.
"""

from pathlib import Path

# --------------------------------------------------------------------------
# BASE DIRECTORY SETUP
# --------------------------------------------------------------------------
BASE_DIR: Path = Path(__file__).resolve().parent

# --------------------------------------------------------------------------
# DATA PATHS
# --------------------------------------------------------------------------
DATA_DIR: Path = BASE_DIR / "data"
RAW_DATA_DIR: Path = DATA_DIR / "raw"
PROCESSED_DATA_DIR: Path = DATA_DIR / "processed"

RAW_DATASET_PATH: Path = RAW_DATA_DIR / "student-mat.csv"
PROCESSED_DATASET_PATH: Path = PROCESSED_DATA_DIR / "student_performance_processed.csv"

RAW_CSV_DELIMITER: str = ";"

# --------------------------------------------------------------------------
# LOGGING CONFIGURATION
# --------------------------------------------------------------------------
LOGS_DIR: Path = BASE_DIR / "logs"
LOG_FILE_PATH: Path = LOGS_DIR / "app.log"
LOG_LEVEL: str = "INFO"
LOG_FORMAT: str = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"

# --------------------------------------------------------------------------
# VISUALIZATION OUTPUT
# --------------------------------------------------------------------------
CHARTS_DIR: Path = BASE_DIR / "charts"

# --------------------------------------------------------------------------
# GRADE / PERFORMANCE PREDICTION THRESHOLDS
# --------------------------------------------------------------------------
GRADE_THRESHOLDS: dict[str, int] = {
    "EXCELLENT": 16,
    "GOOD": 13,
    "AVERAGE": 10,
    "NEEDS_IMPROVEMENT": 7,
}

CATEGORY_EXCELLENT: str = "Excellent"
CATEGORY_GOOD: str = "Good"
CATEGORY_AVERAGE: str = "Average"
CATEGORY_NEEDS_IMPROVEMENT: str = "Needs Improvement"
CATEGORY_AT_RISK: str = "At Risk"

# --------------------------------------------------------------------------
# ATTENDANCE DERIVATION
# --------------------------------------------------------------------------
ASSUMED_TOTAL_CLASS_SESSIONS: int = 100

# --------------------------------------------------------------------------
# APPLICATION METADATA
# --------------------------------------------------------------------------
APP_NAME: str = "AI-Powered Student Performance Prediction & Learning Recommendation System"
APP_VERSION: str = "1.0.0"
