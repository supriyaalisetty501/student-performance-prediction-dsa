# Screenshots Guide

This folder contains two kinds of images for your submission:

1. **Chart screenshots (included, real, ready to use)** — actual PNG
   output produced by running `visualization/charts.py` against a small
   representative sample of student records. These are genuine program
   output, not mockups.
2. **CLI screenshots (you capture these yourself)** — terminal
   interactions are specific to your machine/terminal theme, so capture
   these yourself after running `python3 app.py` with the real dataset in
   place. Instructions and exact screens to capture are listed below.

---

## Part A — Chart Screenshots (included in this folder)

| # | Filename | Caption |
|---|---|---|
| 1 | `performance_distribution.png` | **Figure 1 — Student Performance Distribution.** Bar chart showing the count of students in each of the five predicted performance categories (Excellent, Good, Average, Needs Improvement, At Risk), generated from Menu Option 7. |
| 2 | `attendance_analysis.png` | **Figure 2 — Attendance Analysis.** Histogram of student attendance percentages, derived from the raw `absences` column during preprocessing. |
| 3 | `marks_distribution.png` | **Figure 3 — Marks Distribution.** Histogram of final grades (`G3`, 0–20 scale) across the loaded student population. |
| 4 | `study_hours_analysis.png` | **Figure 4 — Study Hours Analysis.** Histogram of weekly study hours, converted from the raw dataset's coded `studytime` scale (1–4). |
| 5 | `correlation_heatmap.png` | **Figure 5 — Correlation Matrix.** Heatmap showing the correlation coefficients between study hours, attendance percentage, and final grade, computed with `numpy.corrcoef`. |

> **Note:** These five charts were generated from a small representative
> sample used for testing during development. When you run the
> application against the full 395-record UCI dataset, re-run Menu Option
> 7 and replace these five files with your own output — the code and
> chart formatting will be identical, only the data volume changes.

---

## Part B — CLI Screenshots (capture these yourself)

After placing the real `student-mat.csv` in `data/raw/` and running
`python3 app.py`, capture your terminal window at each of these points
and save them into this folder using the suggested filenames:

| # | Suggested filename | What to capture | Caption |
|---|---|---|---|
| 6 | `06_main_menu.png` | The initial 8-option menu right after starting `app.py` | **Figure 6 — Main Menu.** The application's entry-point menu showing all 8 required options. |
| 7 | `07_load_dataset.png` | After selecting Option 1, showing the "✅ Dataset loaded successfully: 395 student records" message | **Figure 7 — Dataset Loaded.** Confirmation that the raw CSV was auto-preprocessed and loaded into memory as a List and Dictionary. |
| 8 | `08_display_records.png` | Option 2 output, showing a page of student summaries | **Figure 8 — Display Student Records.** Paginated view of loaded student records. |
| 9 | `09_search_result.png` | Option 3, searching by Student ID, showing a found result | **Figure 9 — Search Result (Linear Search).** A student record retrieved by manual Linear Search on Student ID. |
| 10 | `10_sorted_records.png` | Option 4, sorted by Final Grade descending | **Figure 10 — Sorted Records (Merge Sort).** Top student records after sorting the full dataset by final grade using the manual Merge Sort implementation. |
| 11 | `11_prediction_output.png` | Option 5, entering a new student's details and viewing the prediction | **Figure 11 — Rule-Based Prediction.** A hypothetical student's academic details classified into a performance category with an accompanying recommendation. |
| 12 | `12_batch_recommendations.png` | Option 6 output, showing the batch prediction summary | **Figure 12 — Batch Recommendations.** Performance categories and recommendations generated for the entire loaded dataset. |
| 13 | `13_charts_generated.png` | Option 7 output, showing the "✅ Generated 5 charts" confirmation | **Figure 13 — Visualizations Generated.** Confirmation that all five chart files were created in `charts/`. |

### How to capture
- **Windows:** `Win + Shift + S`, select the terminal window region.
- **macOS:** `Cmd + Shift + 4`, then drag over the terminal window.
- **Linux:** Use your desktop's screenshot tool (e.g., `gnome-screenshot`,
  `flameshot`) or `PrintScreen`.

Save each capture as a `.png` into this `screenshots/` folder using the
suggested filenames above so they match the report and README references.
