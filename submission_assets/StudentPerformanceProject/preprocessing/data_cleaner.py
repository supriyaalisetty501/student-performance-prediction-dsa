"""
preprocessing/data_cleaner.py
==============================
Transforms the raw UCI "Student Performance" dataset (student-mat.csv)
into a cleaned, analysis-ready CSV, WITHOUT ever modifying the original
raw file.
"""

import csv
from pathlib import Path

import config
from utils.logger import get_logger

logger = get_logger(__name__)

_STUDYTIME_CODE_TO_HOURS: dict[str, float] = {
    "1": 1.5,
    "2": 3.5,
    "3": 7.5,
    "4": 11.0,
}


class DataCleaningError(Exception):
    """Raised when the raw dataset cannot be cleaned due to a structural problem."""


def _convert_studytime_code(code: str) -> float:
    """Convert a raw studytime code ("1"-"4") into representative weekly study hours."""
    try:
        return _STUDYTIME_CODE_TO_HOURS[code.strip()]
    except KeyError as exc:
        raise DataCleaningError(
            f"Unexpected studytime code encountered: {code!r}"
        ) from exc


def _calculate_attendance_percentage(absences: int) -> float:
    """Derive an attendance percentage from a raw absence count."""
    attended_sessions = config.ASSUMED_TOTAL_CLASS_SESSIONS - absences
    percentage = (attended_sessions / config.ASSUMED_TOTAL_CLASS_SESSIONS) * 100
    return max(0.0, min(100.0, round(percentage, 2)))


def clean_dataset(raw_path: Path = config.RAW_DATASET_PATH,
                   processed_path: Path = config.PROCESSED_DATASET_PATH) -> int:
    """
    Read the raw UCI dataset, clean/derive fields, and write the result
    to the processed dataset path.
    """
    if not raw_path.exists():
        raise DataCleaningError(
            f"Raw dataset not found at '{raw_path}'. Please download "
            "student-mat.csv from the UCI Machine Learning Repository "
            "(or the equivalent Kaggle mirror) and place it at this path. "
            "See README.md for exact download instructions."
        )

    required_columns = {"age", "sex", "school", "studytime", "absences", "G1", "G2", "G3"}

    cleaned_rows: list[dict] = []

    logger.info("Starting dataset cleaning from raw file: %s", raw_path)

    with open(raw_path, mode="r", encoding="utf-8", newline="") as raw_file:
        reader = csv.DictReader(raw_file, delimiter=config.RAW_CSV_DELIMITER)

        if reader.fieldnames is None:
            raise DataCleaningError("Raw dataset appears to be empty (no header row found).")

        missing_columns = required_columns - set(reader.fieldnames)
        if missing_columns:
            raise DataCleaningError(
                f"Raw dataset is missing required columns: {sorted(missing_columns)}. "
                "Confirm the file is the correct UCI student-mat.csv dataset."
            )

        for row_number, row in enumerate(reader, start=1):
            try:
                absences = int(row["absences"])
                cleaned_rows.append(
                    {
                        "student_id": row_number,
                        "school": row["school"].strip(),
                        "sex": row["sex"].strip(),
                        "age": int(row["age"]),
                        "study_hours": _convert_studytime_code(row["studytime"]),
                        "absences": absences,
                        "attendance_percentage": _calculate_attendance_percentage(absences),
                        "grade_1": float(row["G1"]),
                        "grade_2": float(row["G2"]),
                        "final_grade": float(row["G3"]),
                    }
                )
            except (ValueError, DataCleaningError) as row_error:
                logger.warning("Skipping malformed row %d: %s", row_number, row_error)
                continue

    if not cleaned_rows:
        raise DataCleaningError("No valid rows could be cleaned from the raw dataset.")

    processed_path.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = list(cleaned_rows[0].keys())
    with open(processed_path, mode="w", encoding="utf-8", newline="") as processed_file:
        writer = csv.DictWriter(processed_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(cleaned_rows)

    logger.info(
        "Dataset cleaning complete. %d records written to %s",
        len(cleaned_rows), processed_path
    )

    return len(cleaned_rows)
