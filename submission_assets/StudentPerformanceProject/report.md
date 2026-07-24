<div align="center">

# AI-Powered Student Performance Prediction &
# Learning Recommendation System

### Project Report

**Course:** Data Structures & Algorithms with Python
**Submission Type:** Mini Project
**Language / Tools:** Python 3, Matplotlib, NumPy
**Dataset:** UCI Machine Learning Repository — Student Performance Data Set

</div>

<!-- pagebreak -->

## Table of Contents

1. Introduction
2. Objectives
3. Dataset
4. System Architecture
5. Data Structures Used and Justification
6. Algorithms Used, Complexity, and Justification
7. Application Workflow
8. Visualizations
9. Error Handling & Robustness
10. Results
11. Future Enhancements
12. Conclusion
13. References

<!-- pagebreak -->

## 1. Introduction

Academic institutions generate large volumes of student performance data
every term, yet manually reviewing this data to identify struggling
students is slow and inconsistent. This project implements a command-line
application that applies core Data Structures & Algorithms concepts to
solve this real-world problem: organizing student records efficiently,
searching and sorting them using manually implemented algorithms, and
producing a transparent, rule-based performance prediction with an
actionable recommendation for every student.

## 2. Objectives

1. Demonstrate practical use of Lists and Dictionaries for organizing
   real academic data.
2. Implement Linear Search and Merge Sort manually (no reliance on
   Python's built-in `sort()` or search shortcuts).
3. Build a rule-based (non-ML, no paid API) prediction engine.
4. Generate personalized learning recommendations per prediction category.
5. Visualize class-wide trends using Matplotlib.
6. Apply professional software engineering practices: modular
   architecture, logging, type hints, docstrings, and defensive error
   handling.

<!-- pagebreak -->

## 3. Dataset

The project uses the **UCI Machine Learning Repository "Student
Performance Data Set"** (Cortez & Silva, 2008), specifically the
Mathematics course file `student-mat.csv` (395 records, 33 raw columns).
This is a real, publicly available, citable academic dataset — not
synthetic data.

Key fields used: `school`, `sex`, `age`, `studytime` (coded 1-4),
`absences`, `G1`, `G2`, `G3` (grades on a 0-20 scale).

The raw file is never modified. A dedicated preprocessing module
(`preprocessing/data_cleaner.py`) reads the raw CSV and writes a derived,
cleaned CSV into `data/processed/`, deriving:
- `study_hours` from the coded `studytime` scale,
- `attendance_percentage` from the raw `absences` count,
- a sequential `student_id` (absent in the raw file).

<!-- pagebreak -->

## 4. System Architecture

The project follows a layered, modular architecture:

```
Presentation Layer    -> app.py (CLI menu, input handling)
Domain Layer          -> models.py (Student dataclass)
Business Logic Layer  -> algorithms/ (searching, sorting, prediction)
Data Access Layer     -> utils/data_loader.py, preprocessing/data_cleaner.py
Cross-Cutting Layer   -> utils/logger.py, utils/validators.py, config.py
Presentation Output   -> visualization/charts.py
```

This separation means each layer can be modified, tested, or replaced
independently — for example, swapping the CLI for a web interface would
only require changes in the Presentation Layer, since all business logic
lives in `algorithms/`.

## 5. Data Structures Used and Justification

| Data Structure | Location | Justification |
|---|---|---|
| `List[Student]` | `utils/data_loader.py` | Ordered, indexable collection — a hard requirement for both Linear Search (sequential scan) and Merge Sort (index-based divide step). |
| `Dict[int, Student]` | `utils/data_loader.py` | O(1) average-case direct lookup by `student_id`, built alongside the list to illustrate the classic array-vs-hash-map access trade-off. |
| `Dict[str, str]` / `Dict[str, int]` | `algorithms/prediction.py`, `config.py` | Category-to-recommendation and category-to-threshold mappings, avoiding long conditional chains and centralizing configurable policy. |

<!-- pagebreak -->

## 6. Algorithms Used, Complexity, and Justification

### 6.1 Linear Search
- **Implementation:** `algorithms/searching.py`, functions
  `linear_search_by_id()` and `linear_search_by_predicate()`.
- **Explanation:** Iterates through the list index by index, comparing
  each element against the target condition, until a match is found or
  the list is exhausted.
- **Time Complexity:** O(1) best case, O(n) average and worst case.
- **Space Complexity:** O(1).
- **Why selected:** The dataset cannot be assumed sorted on every
  possible search key a user might query (ID, school code, etc.).
  Binary Search requires a sorted array on the specific search key;
  Linear Search has no such precondition, making it the correct
  general-purpose choice for this use case.

### 6.2 Merge Sort
- **Implementation:** `algorithms/sorting.py`, functions `merge_sort()`
  and `_merge()`.
- **Explanation:** A divide-and-conquer algorithm that recursively splits
  the list in half until sublists of size 0 or 1 remain (trivially
  sorted), then merges sorted sublists back together in linear time.
- **Time Complexity:** O(n log n) in all cases (best, average, worst).
- **Space Complexity:** O(n) — auxiliary lists are allocated during
  merging; not an in-place sort.
- **Why selected over Quick Sort:** Merge Sort guarantees O(n log n)
  regardless of input order, whereas Quick Sort can degrade to O(n²) on
  already-sorted or adversarially ordered input without careful pivot
  selection. Merge Sort is also stable, which preserves original record
  order among students who share an identical grade — a desirable
  property for reproducible academic reporting.

### 6.3 Rule-Based Prediction
- **Implementation:** `algorithms/prediction.py`,
  `predict_performance_category()`.
- **Explanation:** Applies ordered threshold comparisons against a
  student's final grade (configurable via `config.GRADE_THRESHOLDS`) to
  assign one of five categories.
- **Why rule-based (not ML):** Fully transparent and explainable —
  every classification can be traced back to a specific numeric
  threshold, which matters when the output affects real students,
  parents, and instructors.

<!-- pagebreak -->

## 7. Application Workflow

1. **Load Dataset** — validates raw file existence, triggers
   preprocessing if the processed file is missing/stale, loads records
   into a `List[Student]` and builds a `Dict[int, Student]` index.
2. **Display Student Records** — paginated display using the in-memory
   list.
3. **Search Student Information** — manual Linear Search by ID or by
   predicate (e.g., school code).
4. **Sort Student Records** — manual Merge Sort by grade, attendance,
   study hours, or age, ascending or descending.
5. **Predict Student Performance** — accepts new hypothetical student
   details and returns an instant rule-based prediction.
6. **Generate Learning Recommendations** — batch prediction +
   recommendation generation across the entire loaded dataset.
7. **Display Visualizations** — generates and saves five Matplotlib
   charts into `charts/`.
8. **Exit** — terminates the session.

## 8. Visualizations

| Chart | File | Insight Provided |
|---|---|---|
| Student Performance Distribution | `performance_distribution.png` | Count of students per predicted category |
| Attendance Analysis | `attendance_analysis.png` | Spread of attendance percentages across the class |
| Marks Distribution | `marks_distribution.png` | Spread of final grades (0-20 scale) |
| Study Hours Analysis | `study_hours_analysis.png` | Spread of weekly study hours |
| Correlation Matrix | `correlation_heatmap.png` | Relationship strength between study hours, attendance, and final grade |

*(See `screenshots/` for real sample renders of each chart.)*

<!-- pagebreak -->

## 9. Error Handling & Robustness

- Custom exceptions (`DataCleaningError`, `DataLoadError`) distinguish
  data-layer failures from generic runtime errors.
- Malformed individual CSV rows are skipped with a logged warning rather
  than aborting the entire load — the system degrades gracefully on
  partially corrupt real-world data.
- All user input in the CLI passes through `utils/validators.py` before
  being used, rejecting non-numeric, out-of-range, or empty input with a
  clear message rather than crashing.
- A top-level exception boundary in `app.py`'s main loop prevents any
  single unexpected error from terminating the entire interactive
  session.

## 10. Results

Testing against a representative sample confirmed:
- Correct List and Dict construction from processed CSV data.
- Linear Search correctly retrieves exact ID matches and predicate-based
  multi-matches.
- Merge Sort output was verified programmatically to match Python's own
  `sorted()` ordering (used only as an external correctness check, never
  as the production sorting mechanism).
- Rule-based prediction correctly classified all five category
  boundaries.
- All five chart types generated successfully with correct titles, axis
  labels, and gridlines, saved to `charts/`.
- The full CLI application was run end-to-end covering all 8 menu
  options with zero crashes, and separately stress-tested with invalid
  input (out-of-range grades, non-numeric IDs, unknown school codes),
  all of which were handled gracefully.

<!-- pagebreak -->

## 11. Future Enhancements

- Add Binary Search as a secondary, opt-in fast path once data is
  pre-sorted, with an explicit runtime comparison against Linear Search.
- Add Quick Sort as an alternative sort strategy for empirical
  average-case comparison against Merge Sort.
- Introduce persistent storage (SQLite) instead of recomputing
  predictions each session.
- Extend the CLI into a web-based dashboard.
- Add automated unit tests covering edge cases (empty dataset, single
  record, all-identical grades, extreme absences).

## 12. Conclusion

This project demonstrates that fundamental data structures and manually
implemented algorithms — rather than relying on built-in shortcuts — can
power a genuinely useful, explainable educational tool. The modular,
professionally structured codebase also serves as a foundation that could
be extended toward a real institutional deployment with minimal
architectural rework.

## 13. References

- P. Cortez and A. Silva. *Using Data Mining to Predict Secondary School
  Student Performance.* In A. Brito and J. Teixeira Eds., Proceedings of
  5th FUBUTEC Conference, pp. 5-12, Porto, Portugal, 2008.
- UCI Machine Learning Repository: Student Performance Data Set.
- Cormen, Leiserson, Rivest, Stein. *Introduction to Algorithms* (Merge
  Sort and Linear Search complexity analysis reference).
