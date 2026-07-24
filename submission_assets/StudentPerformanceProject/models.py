"""
models.py
=========
Defines the canonical, typed data structure representing a single student
record: the `Student` dataclass.

DSA note
--------
    List[Student]        -> primary ordered collection (used by Linear
                             Search and Merge Sort).
    Dict[int, Student]    -> secondary fast-lookup index keyed by student_id
                             (built in utils/data_loader.py).
"""

from dataclasses import dataclass, asdict


@dataclass
class Student:
    """
    Represents a single student's academic record.

    Attributes
    ----------
    student_id : int
    school : str
    sex : str
    age : int
    study_hours : float
    absences : int
    attendance_percentage : float
    grade_1 : float
    grade_2 : float
    final_grade : float
    performance_category : str
    recommendation : str
    """

    student_id: int
    school: str
    sex: str
    age: int
    study_hours: float
    absences: int
    attendance_percentage: float
    grade_1: float
    grade_2: float
    final_grade: float
    performance_category: str = ""
    recommendation: str = ""

    def to_dict(self) -> dict:
        """Convert this Student instance into a plain dictionary."""
        return asdict(self)

    def display_summary(self) -> str:
        """Build a short, human-readable one-line summary of this student."""
        category = self.performance_category if self.performance_category else "Not yet predicted"
        return (
            f"ID: {self.student_id} | School: {self.school} | Age: {self.age} | "
            f"Study Hours/wk: {self.study_hours:.1f} | Attendance: {self.attendance_percentage:.1f}% | "
            f"Final Grade: {self.final_grade:.1f}/20 | Category: {category}"
        )
