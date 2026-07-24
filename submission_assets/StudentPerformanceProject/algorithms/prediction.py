"""
algorithms/prediction.py
=========================
Rule-based student performance prediction and personalized learning
recommendation engine. No external ML models or paid AI APIs are used.
"""

import config
from models import Student
from utils.logger import get_logger

logger = get_logger(__name__)


_RECOMMENDATIONS: dict[str, str] = {
    config.CATEGORY_EXCELLENT: (
        "Excellent performance! Recommend advanced projects, peer mentoring "
        "opportunities, and enrichment material to maintain engagement."
    ),
    config.CATEGORY_GOOD: (
        "Solid performance. Recommend regular coding/practice exercises and "
        "gradually introducing more challenging material."
    ),
    config.CATEGORY_AVERAGE: (
        "Room for improvement. Recommend increasing structured study hours "
        "and targeted revision of weaker topics."
    ),
    config.CATEGORY_NEEDS_IMPROVEMENT: (
        "Performance is below expectations. Recommend a daily revision plan "
        "and closer tracking of attendance and assignment completion."
    ),
    config.CATEGORY_AT_RISK: (
        "Student is at risk of falling significantly behind. Recommend "
        "immediate one-on-one mentoring, parental/guardian notification, "
        "and an intensive extra-practice schedule."
    ),
}


def predict_performance_category(final_grade: float) -> str:
    """Classify a student's final grade into a performance category using rule-based logic."""
    if not (0.0 <= final_grade <= 20.0):
        raise ValueError(f"final_grade must be between 0 and 20; got {final_grade}")

    if final_grade >= config.GRADE_THRESHOLDS["EXCELLENT"]:
        category = config.CATEGORY_EXCELLENT
    elif final_grade >= config.GRADE_THRESHOLDS["GOOD"]:
        category = config.CATEGORY_GOOD
    elif final_grade >= config.GRADE_THRESHOLDS["AVERAGE"]:
        category = config.CATEGORY_AVERAGE
    elif final_grade >= config.GRADE_THRESHOLDS["NEEDS_IMPROVEMENT"]:
        category = config.CATEGORY_NEEDS_IMPROVEMENT
    else:
        category = config.CATEGORY_AT_RISK

    return category


def get_recommendation(category: str) -> str:
    """Retrieve the personalized learning recommendation text for a given category."""
    if category not in _RECOMMENDATIONS:
        raise KeyError(f"Unrecognized performance category: {category!r}")
    return _RECOMMENDATIONS[category]


def predict_and_recommend(student: Student) -> Student:
    """Predict a student's performance category and attach the recommendation."""
    category = predict_performance_category(student.final_grade)
    recommendation = get_recommendation(category)

    student.performance_category = category
    student.recommendation = recommendation

    logger.info(
        "Predicted category '%s' for student_id=%d (final_grade=%.1f).",
        category, student.student_id, student.final_grade
    )

    return student


def predict_for_all(students: list[Student]) -> list[Student]:
    """Apply prediction and recommendation generation to an entire list of students."""
    for student in students:
        predict_and_recommend(student)

    logger.info("Prediction complete for all %d students.", len(students))
    return students
