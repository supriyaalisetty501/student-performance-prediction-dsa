"""
preprocessing/data_cleaner.py
==============================
Transforms the raw UCI "Student Performance" dataset (student-mat.csv)
into a cleaned, analysis-ready CSV.
"""

import csv
from pathlib import Path

import config
from utils.logger import get_logger

logger = get_logger(__name__)

_STUDYTIME_CODE_TO_HOURS = {
    "1": 1.5,
    "2": 3.5,
    "3": 7.5,
    "4": 11.0,
}


class DataCleaningError(Exception):
    """Raised when dataset cleaning fails."""


def _convert_studytime_code(code: str) -> float:
    """Convert UCI studytime code (1-4) into representative study hours."""
    code = str(code).strip()

    if code not in _STUDYTIME_CODE_TO_HOURS:
        raise DataCleaningError(f"Invalid studytime code: {code}")

    return _STUDYTIME_CODE_TO_HOURS[code]


def _calculate_attendance_percentage(absences: int) -> float:
    """Convert absences into attendance percentage."""
    attended = config.ASSUMED_TOTAL_CLASS_SESSIONS - absences
    percentage = (attended / config.ASSUMED_TOTAL_CLASS_SESSIONS) * 100
    return round(max(0.0, min(100.0, percentage)), 2)


def clean_dataset(
    raw_path: Path = config.RAW_DATASET_PATH,
    processed_path: Path = config.PROCESSED_DATASET_PATH,
) -> int:

    if not raw_path.exists():
        raise DataCleaningError(
            f"Dataset not found:\n{raw_path}\n\n"
            "Download student-mat.csv from the UCI repository."
        )

    required_columns = {
        "school",
        "sex",
        "age",
        "studytime",
        "absences",
        "G1",
        "G2",
        "G3",
    }

    cleaned_rows = []

    logger.info("Reading dataset: %s", raw_path)

    with open(raw_path, "r", encoding="utf-8", newline="") as raw_file:

        reader = csv.DictReader(
            raw_file,
            delimiter=config.RAW_CSV_DELIMITER,
        )

        if reader.fieldnames is None:
            raise DataCleaningError("CSV file is empty.")

        reader.fieldnames = [field.strip() for field in reader.fieldnames]

        missing = required_columns - set(reader.fieldnames)

        if missing:
            raise DataCleaningError(
                f"Missing required columns: {sorted(missing)}"
            )

        for row_number, row in enumerate(reader, start=2):

            # Skip completely empty rows
            if not row:
                logger.warning("Skipping empty row %d", row_number)
                continue

            # Skip malformed rows
            if any(value is None for value in row.values()):
                logger.warning("Skipping malformed row %d", row_number)
                continue

            try:

                absences = int(row["absences"].strip())

                cleaned_row = {
                    "student_id": row_number - 1,
                    "school": row["school"].strip(),
                    "sex": row["sex"].strip(),
                    "age": int(row["age"].strip()),
                    "study_hours": _convert_studytime_code(
                        row["studytime"]
                    ),
                    "absences": absences,
                    "attendance_percentage": _calculate_attendance_percentage(
                        absences
                    ),
                    "grade_1": float(row["G1"].strip()),
                    "grade_2": float(row["G2"].strip()),
                    "final_grade": float(row["G3"].strip()),
                }

                cleaned_rows.append(cleaned_row)

            except (
                ValueError,
                TypeError,
                KeyError,
                AttributeError,
                DataCleaningError,
            ) as err:

                logger.warning(
                    "Skipping row %d because of invalid data: %s",
                    row_number,
                    err,
                )

                continue

    if not cleaned_rows:
        raise DataCleaningError(
            "No valid records were found in the dataset."
        )

    processed_path.parent.mkdir(parents=True, exist_ok=True)

    with open(
        processed_path,
        "w",
        encoding="utf-8",
        newline="",
    ) as processed_file:

        writer = csv.DictWriter(
            processed_file,
            fieldnames=cleaned_rows[0].keys(),
        )

        writer.writeheader()
        writer.writerows(cleaned_rows)

    logger.info(
        "Cleaning completed successfully. %d rows written.",
        len(cleaned_rows),
    )

    return len(cleaned_rows)