"""
algorithms/sorting.py
======================
Manual implementation of the Merge Sort algorithm, operating on the
project's primary List[Student] data structure.
"""

from typing import Callable, TypeVar

from models import Student
from utils.logger import get_logger

logger = get_logger(__name__)

T = TypeVar("T")


# ============================================================
# DSA CONCEPT: Manual Merge Sort Implementation
# Time Complexity: O(n log n) best/average/worst
# Space Complexity: O(n)
# ============================================================
def merge_sort(items: list[T], key: Callable[[T], float], descending: bool = False) -> list[T]:
    """Sort a list using the manual Merge Sort algorithm."""
    if len(items) <= 1:
        return list(items)

    middle_index = len(items) // 2
    left_half = merge_sort(items[:middle_index], key, descending)
    right_half = merge_sort(items[middle_index:], key, descending)

    return _merge(left_half, right_half, key, descending)


def _merge(left: list[T], right: list[T], key: Callable[[T], float], descending: bool) -> list[T]:
    """Merge two already-sorted lists into a single sorted list."""
    merged: list[T] = []
    left_index = 0
    right_index = 0

    while left_index < len(left) and right_index < len(right):
        left_key = key(left[left_index])
        right_key = key(right[right_index])

        take_left = (left_key <= right_key) if not descending else (left_key >= right_key)

        if take_left:
            merged.append(left[left_index])
            left_index += 1
        else:
            merged.append(right[right_index])
            right_index += 1

    merged.extend(left[left_index:])
    merged.extend(right[right_index:])

    return merged


def sort_students_by_field(students: list[Student], field_name: str,
                            descending: bool = False) -> list[Student]:
    """Convenience wrapper that sorts Student objects by a named field."""
    key_extractors: dict[str, Callable[[Student], float]] = {
        "final_grade": lambda s: s.final_grade,
        "attendance_percentage": lambda s: s.attendance_percentage,
        "study_hours": lambda s: s.study_hours,
        "age": lambda s: s.age,
    }

    if field_name not in key_extractors:
        raise ValueError(
            f"Unsupported sort field '{field_name}'. "
            f"Supported fields: {list(key_extractors.keys())}"
        )

    logger.info(
        "Sorting %d students by '%s' (%s) using manual Merge Sort.",
        len(students), field_name, "descending" if descending else "ascending"
    )

    return merge_sort(students, key_extractors[field_name], descending)
