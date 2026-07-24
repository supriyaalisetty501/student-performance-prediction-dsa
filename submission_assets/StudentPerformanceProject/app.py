"""
app.py
======
Main command-line application entry point for the AI-Powered Student
Performance Prediction & Learning Recommendation System.
"""

import sys

import config
from models import Student
from algorithms.searching import linear_search_by_id, linear_search_by_predicate
from algorithms.sorting import sort_students_by_field
from algorithms.prediction import predict_and_recommend, predict_for_all
from utils.data_loader import load_students, DataLoadError
from utils.logger import get_logger
from utils.validators import (
    validate_menu_choice,
    validate_positive_float,
    validate_positive_int,
)
from visualization.charts import generate_all_charts

logger = get_logger(__name__)

MENU_TEXT = """
==================================================================
 {app_name}
==================================================================
 1. Load Dataset
 2. Display Student Records
 3. Search Student Information
 4. Sort Student Records
 5. Predict Student Performance
 6. Generate Learning Recommendations
 7. Display Visualizations
 8. Exit
==================================================================
""".format(app_name=config.APP_NAME)

_VALID_MENU_CHOICES = {str(n) for n in range(1, 9)}


class ApplicationState:
    """Holds the application's in-memory state for the duration of a CLI session."""

    def __init__(self) -> None:
        self.students: list[Student] = []
        self.student_index: dict[int, Student] = {}
        self.dataset_loaded: bool = False


def handle_load_dataset(state: ApplicationState) -> None:
    """Menu option 1: Load (and auto-preprocess if needed) the dataset."""
    try:
        state.students, state.student_index = load_students()
        state.dataset_loaded = True
        print(f"\n✅ Dataset loaded successfully: {len(state.students)} student records.")
    except DataLoadError as exc:
        print(f"\n❌ Failed to load dataset: {exc}")
        logger.error("Dataset load failure: %s", exc)


def _require_dataset_loaded(state: ApplicationState) -> bool:
    """Guard clause used by every menu option that needs data in memory."""
    if not state.dataset_loaded:
        print("\n⚠️  Please load the dataset first (Menu Option 1).")
        return False
    return True


def handle_display_records(state: ApplicationState) -> None:
    """Menu option 2: Display all student records (paginated)."""
    if not _require_dataset_loaded(state):
        return

    page_size = 10
    total = len(state.students)

    for start in range(0, total, page_size):
        chunk = state.students[start:start + page_size]
        print(f"\n--- Records {start + 1}-{min(start + page_size, total)} of {total} ---")
        for student in chunk:
            print(student.display_summary())

        if start + page_size < total:
            proceed = input("\nPress Enter to see more, or type 'q' to stop: ").strip().lower()
            if proceed == "q":
                break


def handle_search(state: ApplicationState) -> None:
    """Menu option 3: Search for a student by ID or by school code."""
    if not _require_dataset_loaded(state):
        return

    print("\nSearch by: [1] Student ID   [2] School Code")
    sub_choice = input("Enter choice: ").strip()

    if sub_choice == "1":
        raw_id = input("Enter Student ID: ")
        student_id = validate_positive_int(raw_id, "Student ID", minimum=1)
        if student_id is None:
            print("\n❌ Invalid Student ID entered.")
            return

        result = linear_search_by_id(state.students, student_id)
        if result:
            print(f"\n✅ Found:\n{result.display_summary()}")
        else:
            print(f"\n⚠️  No student found with ID {student_id}.")

    elif sub_choice == "2":
        school_code = input("Enter School Code (e.g., GP or MS): ").strip().upper()
        results = linear_search_by_predicate(state.students, lambda s: s.school.upper() == school_code)
        if results:
            print(f"\n✅ Found {len(results)} student(s) in school '{school_code}':")
            for student in results:
                print(student.display_summary())
        else:
            print(f"\n⚠️  No students found for school code '{school_code}'.")
    else:
        print("\n❌ Invalid sub-choice.")


def handle_sort(state: ApplicationState) -> None:
    """Menu option 4: Sort student records by a chosen field."""
    if not _require_dataset_loaded(state):
        return

    print("\nSort by: [1] Final Grade  [2] Attendance %  [3] Study Hours  [4] Age")
    field_map = {
        "1": "final_grade",
        "2": "attendance_percentage",
        "3": "study_hours",
        "4": "age",
    }
    sub_choice = input("Enter choice: ").strip()
    field_name = field_map.get(sub_choice)

    if field_name is None:
        print("\n❌ Invalid sub-choice.")
        return

    order_choice = input("Order: [1] Ascending  [2] Descending: ").strip()
    descending = order_choice == "2"

    sorted_students = sort_students_by_field(state.students, field_name, descending)
    state.students = sorted_students

    print(f"\n✅ Sorted {len(sorted_students)} records by '{field_name}' "
          f"({'descending' if descending else 'ascending'}).")
    for student in sorted_students[:10]:
        print(student.display_summary())
    if len(sorted_students) > 10:
        print(f"... and {len(sorted_students) - 10} more.")


def handle_predict_single(state: ApplicationState) -> None:
    """Menu option 5: Accept a new student's details and predict performance."""
    print("\n--- Enter New Student Academic Details ---")

    raw_grade = input("Final Grade (0-20): ")
    final_grade = validate_positive_float(raw_grade, "Final Grade", minimum=0.0, maximum=20.0)
    if final_grade is None:
        print("\n❌ Invalid grade entered. Must be a number between 0 and 20.")
        return

    raw_study_hours = input("Weekly Study Hours: ")
    study_hours = validate_positive_float(raw_study_hours, "Study Hours", minimum=0.0, maximum=100.0)
    if study_hours is None:
        print("\n❌ Invalid study hours entered.")
        return

    raw_attendance = input("Attendance Percentage (0-100): ")
    attendance = validate_positive_float(raw_attendance, "Attendance", minimum=0.0, maximum=100.0)
    if attendance is None:
        print("\n❌ Invalid attendance entered.")
        return

    temp_student = Student(
        student_id=-1,
        school="N/A",
        sex="N/A",
        age=0,
        study_hours=study_hours,
        absences=0,
        attendance_percentage=attendance,
        grade_1=final_grade,
        grade_2=final_grade,
        final_grade=final_grade,
    )

    predict_and_recommend(temp_student)

    print(f"\n📊 Predicted Performance Category: {temp_student.performance_category}")
    print(f"💡 Recommendation: {temp_student.recommendation}")


def handle_predict_all(state: ApplicationState) -> None:
    """Menu option 6: Generate predictions + recommendations for the whole dataset."""
    if not _require_dataset_loaded(state):
        return

    predict_for_all(state.students)
    print(f"\n✅ Predictions and recommendations generated for {len(state.students)} students.")

    print("\n--- Sample (first 5 students) ---")
    for student in state.students[:5]:
        print(f"\n{student.display_summary()}")
        print(f"  Recommendation: {student.recommendation}")


def handle_visualizations(state: ApplicationState) -> None:
    """Menu option 7: Generate and save all Matplotlib visualizations."""
    if not _require_dataset_loaded(state):
        return

    if not any(s.performance_category for s in state.students):
        print("\nℹ️  Running predictions first (required for performance distribution chart)...")
        predict_for_all(state.students)

    try:
        chart_paths = generate_all_charts(state.students)
        print(f"\n✅ Generated {len(chart_paths)} charts in '{config.CHARTS_DIR}':")
        for path in chart_paths:
            print(f"   - {path.name}")
    except (ValueError, OSError) as exc:
        print(f"\n❌ Failed to generate charts: {exc}")
        logger.error("Chart generation failure: %s", exc)


def run() -> None:
    """Main application loop: displays the menu and dispatches to handlers."""
    state = ApplicationState()
    handlers = {
        "1": handle_load_dataset,
        "2": handle_display_records,
        "3": handle_search,
        "4": handle_sort,
        "5": handle_predict_single,
        "6": handle_predict_all,
        "7": handle_visualizations,
    }

    logger.info("Application started.")
    print(MENU_TEXT)

    while True:
        raw_choice = input("Enter your choice (1-8): ")
        choice = validate_menu_choice(raw_choice, _VALID_MENU_CHOICES)

        if choice is None:
            print("\n❌ Invalid choice. Please enter a number between 1 and 8.")
            continue

        if choice == "8":
            print("\n👋 Exiting application. Goodbye!")
            logger.info("Application exited normally.")
            break

        try:
            handlers[choice](state)
        except Exception as exc:  # noqa: BLE001 -- top-level CLI safety net
            print(f"\n❌ An unexpected error occurred: {exc}")
            logger.exception("Unhandled exception in menu handler for choice '%s'.", choice)

        print(MENU_TEXT)


if __name__ == "__main__":
    try:
        run()
    except KeyboardInterrupt:
        print("\n\n👋 Application interrupted by user. Goodbye!")
        sys.exit(0)
