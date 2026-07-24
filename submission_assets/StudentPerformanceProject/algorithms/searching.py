"""
algorithms/searching.py
========================
Manual implementation of the Linear Search algorithm, operating on the
project's primary List[Student] data structure.
"""

from typing import Callable, Optional

from models import Student
from utils.logger import get_logger

logger = get_logger(__name__)


# ============================================================
# DSA CONCEPT: Manual Linear Search Implementation
# Time Complexity: Best O(1), Average/Worst O(n)
# Space Complexity: O(1)
# ============================================================
def linear_search_by_id(students: list[Student], target_id: int) -> Optional[Student]:
    """Search for a student by exact student_id using manual Linear Search."""
    comparisons = 0
    for index in range(len(students)):
        comparisons += 1
        if students[index].student_id == target_id:
            logger.info(
                "Linear search found student_id=%d after %d comparison(s).",
                target_id, comparisons
            )
            return students[index]

    logger.info(
        "Linear search completed %d comparison(s); student_id=%d not found.",
        comparisons, target_id
    )
    return None


def linear_search_by_predicate(students: list[Student],
                                predicate: Callable[[Student], bool]) -> list[Student]:
    """Search for ALL students matching a custom predicate function via manual scan."""
    matches: list[Student] = []
    comparisons = 0

    for index in range(len(students)):
        comparisons += 1
        if predicate(students[index]):
            matches.append(students[index])

    logger.info(
        "Linear search by predicate completed %d comparison(s); %d match(es) found.",
        comparisons, len(matches)
    )
    return matches
