# AI-Powered Student Performance Prediction & Learning Recommendation System

A production-style Python application demonstrating core Data Structures &
Algorithms (Lists, Dictionaries, Linear Search, Merge Sort) applied to a
real educational dataset, with rule-based performance prediction,
personalized learning recommendations, and Matplotlib visualizations.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Complete-brightgreen)

---

## 1. Project Overview

This system loads real student academic data, organizes it using
fundamental data structures, allows searching and sorting through manually
implemented algorithms, predicts each student's performance category using
transparent rule-based logic, generates personalized learning
recommendations, and visualizes key trends — all through a clean,
menu-driven command-line interface.

The project is built to professional software engineering standards:
modular architecture, type hints, docstrings, logging, and defensive error
handling throughout — while keeping every required DSA concept clearly
visible and separated for evaluation.

## 2. Problem Statement

Educational institutions collect large amounts of student data (grades,
attendance, study habits) but often lack simple tools to quickly identify
which students need intervention. This project addresses that gap with a
lightweight, explainable, rule-based system that:

- Organizes student records efficiently in memory.
- Allows fast search and sorting of records.
- Classifies each student into a performance category.
- Recommends a concrete, actionable next step per category.
- Visualizes class-wide trends for a teacher/administrator.

## 3. Dataset Information

- **Name:** Student Performance Data Set
- **Source:** UCI Machine Learning Repository (Cortez & Silva, 2008),
  also mirrored on Kaggle as part of the "Student Alcohol Consumption"
  dataset collection.
- **File used:** `student-mat.csv` (Mathematics course subset, 395 records)
- **Delimiter:** semicolon (`;`) — not comma.

### How to obtain the dataset
1. Go to the UCI Machine Learning Repository and search for
   **"Student Performance Data Set"**, or search Kaggle for
   **"Student Alcohol Consumption"** (same source file).
2. Download `student-mat.csv`.
3. Place it at:
   ```
   StudentPerformanceProject/data/raw/student-mat.csv
   ```
4. Run the application — Menu Option 1 ("Load Dataset") will automatically
   detect the raw file, clean/preprocess it, and load it into memory. The
   original raw file is **never modified**; cleaned output is written
   separately to `data/processed/`.

### Key raw columns used
| Column | Meaning |
|---|---|
| `school`, `sex`, `age` | Demographics |
| `studytime` | Coded weekly study time (1-4 scale) |
| `absences` | Number of classes missed |
| `G1`, `G2`, `G3` | Period 1, Period 2, and Final grade (0-20 scale) |

### Derived fields (created during preprocessing, raw file untouched)
| Field | Derivation |
|---|---|
| `study_hours` | `studytime` code converted to representative real hours |
| `attendance_percentage` | Derived from `absences` vs. an assumed term length |
| `student_id` | Sequentially assigned (raw dataset has no native ID) |

## 4. Data Structures Used

| Structure | Where Used | Why |
|---|---|---|
| **List[Student]** | `utils/data_loader.py`, all algorithm modules | Primary ordered collection required for indexable, sequential access — a prerequisite for both Linear Search and Merge Sort. |
| **Dict[int, Student]** | `utils/data_loader.py` (`student_index`) | Secondary fast-lookup structure keyed by `student_id`, offering O(1) average-case access — contrasted against the O(n) manual Linear Search to illustrate the classic list-vs-dict trade-off. |
| **Dict[str, str]** | `algorithms/prediction.py` (`_RECOMMENDATIONS`), `config.py` (`GRADE_THRESHOLDS`) | Category-to-text and category-to-threshold mappings — a natural dictionary use case avoiding long if/elif chains. |

## 5. Algorithms Used

### Linear Search — `algorithms/searching.py`
- **Purpose:** Locate a student by ID or by an arbitrary predicate (e.g., school code).
- **Why chosen:** The dataset is not guaranteed sorted on every possible search key, so Binary Search's precondition (sorted input) cannot be assumed for general search. Linear Search makes no such assumption.
- **Time Complexity:** Best O(1), Average O(n), Worst O(n)
- **Space Complexity:** O(1)

### Merge Sort — `algorithms/sorting.py`
- **Purpose:** Sort student records by final grade, attendance, study hours, or age.
- **Why chosen over Quick Sort:** Guaranteed O(n log n) worst-case performance (Quick Sort can degrade to O(n²) on adversarial/sorted input), and Merge Sort is **stable** — ties retain original order, which matters for reproducible academic record ordering.
- **Time Complexity:** Best/Average/Worst all O(n log n)
- **Space Complexity:** O(n) — not in-place; uses temporary lists during merging.

### Rule-Based Prediction — `algorithms/prediction.py`
- **Purpose:** Classify a numeric final grade into one of five performance categories using ordered threshold comparisons (no ML model, no paid API).
- **Categories:** Excellent, Good, Average, Needs Improvement, At Risk.
- **Why rule-based:** Fully transparent and explainable to students/parents/instructors — an important property in an educational context.

## 6. Application Workflow

```
1. Load Dataset          -> auto-preprocesses raw CSV if needed, loads List + Dict
2. Display Records       -> paginated view of all loaded students
3. Search                -> Linear Search by ID or by school code
4. Sort                  -> Merge Sort by grade / attendance / study hours / age
5. Predict Performance   -> rule-based classification for a NEW hypothetical student
6. Generate Recommendations (batch) -> predicts + recommends for entire loaded dataset
7. Display Visualizations -> generates and saves 5 charts to charts/
8. Exit
```

## 7. Project Structure

```
StudentPerformanceProject/
│
├── data/
│   ├── raw/                # Place student-mat.csv here (never modified)
│   └── processed/          # Auto-generated cleaned CSV
│
├── preprocessing/
│   └── data_cleaner.py      # Raw -> processed transformation
│
├── algorithms/
│   ├── searching.py         # Manual Linear Search
│   ├── sorting.py           # Manual Merge Sort
│   └── prediction.py        # Rule-based prediction + recommendations
│
├── visualization/
│   └── charts.py             # 5 Matplotlib charts, saved to charts/
│
├── utils/
│   ├── data_loader.py        # Builds List[Student] + Dict[int, Student]
│   ├── logger.py             # Centralized logging
│   └── validators.py         # Input validation helpers
│
├── charts/                   # Generated chart PNGs (auto-created)
├── logs/                     # Runtime logs (auto-created)
│
├── config.py                 # Central configuration (paths, thresholds)
├── models.py                 # Student dataclass definition
├── app.py                    # CLI entry point
├── requirements.txt
├── README.md
├── report.md
└── .gitignore
```

## 8. Installation Guide

```bash
# 1. Clone or extract the project
git clone <your-repo-url>
cd StudentPerformanceProject

# 2. (Recommended) Create a virtual environment
python3 -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Download the dataset (see Section 3) and place it at:
#    data/raw/student-mat.csv

# 5. Run the application
python3 app.py
```

## 9. User Guide

- On first run, select **Option 1** to load the dataset. This will
  auto-detect and preprocess the raw CSV if it hasn't been cleaned yet.
- Use **Option 2** to browse records in pages of 10.
- Use **Option 3** to search by exact Student ID (Linear Search) or by
  school code (returns all matches).
- Use **Option 4** to sort the entire loaded dataset by a chosen numeric
  field, ascending or descending, using the manual Merge Sort.
- Use **Option 5** to enter a new, hypothetical student's grade, study
  hours, and attendance, and receive an instant rule-based prediction +
  recommendation (this does not modify the loaded dataset).
- Use **Option 6** to run predictions across the entire loaded dataset at
  once.
- Use **Option 7** to generate all five visualizations into `charts/`.
- Use **Option 8** to exit.

## 10. Sample Output

```
Enter your choice (1-8): 1

✅ Dataset loaded successfully: 395 student records.

Enter your choice (1-8): 3

Search by: [1] Student ID   [2] School Code
Enter choice: 1
Enter Student ID: 12

✅ Found:
ID: 12 | School: GP | Age: 16 | Study Hours/wk: 7.5 | Attendance: 94.0% | Final Grade: 14.0/20 | Category: Not yet predicted

Enter your choice (1-8): 5

--- Enter New Student Academic Details ---
Final Grade (0-20): 6
Weekly Study Hours: 2
Attendance Percentage (0-100): 65

📊 Predicted Performance Category: At Risk
💡 Recommendation: Student is at risk of falling significantly behind. Recommend
immediate one-on-one mentoring, parental/guardian notification, and an
intensive extra-practice schedule.
```

## 11. Screenshots

See `screenshots/README.md` for the full captioned list and capture
instructions. Sample chart outputs (real, code-generated) are included in
`screenshots/`.

## 12. Results

Running the full pipeline against the real dataset (395 records) produces:
- A complete List + Dict in-memory representation of all students.
- Verified O(n log n) Merge Sort ordering across all sortable fields.
- Verified Linear Search retrieval by ID and by predicate.
- Five saved chart images summarizing class-wide performance, attendance,
  marks, study habits, and feature correlations.
- A performance category and recommendation for every student.

## 13. Future Enhancements

- Add Binary Search as an alternative fast-path once records are
  pre-sorted by a given key (with a visible complexity comparison against
  Linear Search).
- Add Quick Sort as a second sorting option to compare average-case
  performance against Merge Sort empirically.
- Persist predictions back into a student database (SQLite) rather than
  recomputing them each session.
- Build a simple web dashboard (Flask/Streamlit) on top of the same
  algorithms module for non-CLI users.
- Extend the rule-based engine into a lightweight, locally-trained ML
  model (e.g., decision tree) while keeping the current rule-based system
  as an explainable fallback.
- Add unit tests (`tests/`) covering edge cases for each algorithm.

## 14. Attribution

Dataset: P. Cortez and A. Silva. "Using Data Mining to Predict Secondary
School Student Performance." In A. Brito and J. Teixeira Eds., Proceedings
of 5th FUBUTEC Conference, pp. 5-12, Porto, Portugal, 2008. Distributed via
the UCI Machine Learning Repository.

## 15. License

This project is submitted for academic coursework purposes. Feel free to
fork and extend it for your own learning.
