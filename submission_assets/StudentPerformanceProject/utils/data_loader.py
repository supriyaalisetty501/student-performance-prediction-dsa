"""
utils/data_loader.py
=====================
Loads student records from the processed CSV file into the in-memory
data structures used throughout the application.

============================================================
DSA CONCEPT: List and Dictionary construction
============================================================
    student_list : List[Student]   -> primary ordered collection.
    student_index : Dict[int, Student] -> secondary fast-lookup index.
============================================================
"""

import csv
from pathlib import Path
from typing import Tuple

import config
from models import Student
from preprocessing.data_cleaner import clean_dataset, DataCleaningError
from utils.logger import get_logger

logger = get_logger(__name__)


class DataLoadError(Exception):
    """Raised when student records cannot be loaded into memory."""


def _row_to_student(row: dict) -> Student:
    """Convert a single processed CSV row (dict of strings) into a typed Student instance."""
    return Student(
        student_id=int(row["student_id"]),
        school=row["school"],
        sex=row["sex"],
        age=int(row["age"]),
        study_hours=float(row["study_hours"]),
        absences=int(row["absences"]),
        attendance_percentage=float(row["attendance_percentage"]),
        grade_1=float(row["grade_1"]),
        grade_2=float(row["grade_2"]),
        final_grade=float(row["final_grade"]),
    )


def load_students(processed_path: Path = config.PROCESSED_DATASET_PATH,
                   raw_path: Path = config.RAW_DATASET_PATH,
                   auto_preprocess: bool = True) -> Tuple[list[Student], dict[int, Student]]:
    """
    Load all student records into memory as both a List and a Dict.
    """
    if not processed_path.exists():
        if not auto_preprocess:
            raise DataLoadError(
                f"Processed dataset not found at '{processed_path}' and "
                "auto_preprocess is disabled."
            )
        logger.info("Processed dataset not found. Triggering preprocessing pipeline...")
        try:
            clean_dataset(raw_path=raw_path, processed_path=processed_path)
        except DataCleaningError as exc:
            raise DataLoadError(f"Automatic preprocessing failed: {exc}") from exc

    student_list: list[Student] = []
    student_index: dict[int, Student] = {}

    try:
        with open(processed_path, mode="r", encoding="utf-8", newline="") as file:
            reader = csv.DictReader(file)
            for row_number, row in enumerate(reader, start=1):
                try:
                    student = _row_to_student(row)
                except (ValueError, KeyError) as row_error:
                    logger.warning(
                        "Skipping unparseable processed row %d: %s", row_number, row_error
                    )
                    continue

                student_list.append(student)
                student_index[student.student_id] = student

    except FileNotFoundError as exc:
        raise DataLoadError(f"Processed dataset disappeared before it could be read: {exc}") from exc
    except OSError as exc:
        raise DataLoadError(f"OS error while reading processed dataset: {exc}") from exc

    if not student_list:
        raise DataLoadError("Processed dataset contained no valid student records.")

    logger.info(
        "Loaded %d student records into memory (List + Dict index).", len(student_list)
    )

    return student_list, student_index
