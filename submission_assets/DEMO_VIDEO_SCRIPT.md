# Demo Video Script
## AI-Powered Student Performance Prediction & Learning Recommendation System

**Target length:** 6–7 minutes (fits the 5–8 minute requirement with buffer)
**Format:** Screen recording of terminal + generated charts, narrated voiceover.

---

### [0:00 – 0:40] Introduction (40 sec)

> "Hi, I'm [Your Name], and this is my DSA with Python mini project: an
> AI-Powered Student Performance Prediction and Learning Recommendation
> System.
>
> The goal was to take a real educational dataset and apply core data
> structures and algorithms — specifically Lists, Dictionaries, a manually
> implemented Linear Search, and a manually implemented Merge Sort — to
> solve a genuine problem: quickly identifying which students need
> academic support.
>
> Everything you'll see uses real data from the UCI Machine Learning
> Repository, and every prediction is rule-based and fully explainable —
> no black-box AI, no paid APIs."

**On screen:** Title slide or project folder structure in an IDE.

---

### [0:40 – 1:30] Dataset & Architecture Overview (50 sec)

> "The dataset is the UCI 'Student Performance Data Set' — 395 real
> student records including grades, absences, and study habits. I never
> modify this raw file directly. Instead, a dedicated preprocessing
> module reads it, derives clean fields like attendance percentage and
> study hours, and writes the result to a separate processed file.
>
> The whole project follows a layered architecture: a presentation layer
> for the CLI, a domain layer for the Student data model, a business
> logic layer for the algorithms, and a data access layer for loading and
> cleaning. Every module has type hints, docstrings, and logging."

**On screen:** Quickly scroll through the folder structure — `data/raw`,
`preprocessing/`, `algorithms/`, `utils/`, `visualization/`, `app.py`.

---

### [1:30 – 2:15] Menu Walkthrough & Load Dataset (45 sec)

> "Let's run it. Here's the main menu — eight options exactly as required:
> load, display, search, sort, predict, recommend, visualize, and exit.
>
> Option 1 loads the dataset. Behind the scenes, it checks if a processed
> file already exists — if not, it automatically triggers preprocessing
> on the raw CSV. Here it is loading 395 real student records into two
> data structures simultaneously: a List, which preserves order for our
> algorithms, and a Dictionary, keyed by student ID, for instant lookups."

**On screen:** Run `python3 app.py`, select `1`, show the success message.

---

### [2:15 – 3:00] Display & Search — Linear Search (45 sec)

> "Option 2 displays records in pages of ten. Option 3 lets us search —
> I'll search by exact Student ID. This uses a Linear Search I implemented
> manually — no `in` operator, no `.index()`. It's a plain for-loop
> scanning index by index. That gives it O(n) time complexity in the
> worst case, but it makes no assumption that the data is sorted, which
> is important because our list isn't sorted on every field a user might
> search by."

**On screen:** Select `2`, show paginated output; select `3`, search by
ID, show the result.

---

### [3:00 – 3:50] Sort — Merge Sort (50 sec)

> "Option 4 sorts the records. I implemented Merge Sort from scratch —
> a classic divide-and-conquer algorithm. It recursively splits the list
> in half until each piece has zero or one elements, then merges sorted
> halves back together. I chose Merge Sort over Quick Sort because it
> guarantees O(n log n) performance in every case, and it's stable —
> students with the same grade keep their original order. Let's sort by
> final grade, descending."

**On screen:** Select `4`, choose "Final Grade", choose "Descending",
show the top sorted students.

---

### [3:50 – 4:50] Predict & Recommend (60 sec)

> "Option 5 lets me enter a brand-new, hypothetical student's grade,
> study hours, and attendance, and get an instant prediction. This uses
> rule-based thresholds — no machine learning model — so every
> classification is fully explainable. Let's try a low grade... and you
> can see it's classified as 'At Risk', with a concrete recommendation:
> immediate mentoring and an intensive practice schedule.
>
> Option 6 runs this same prediction logic across the entire loaded
> dataset at once, assigning a category and recommendation to every
> student."

**On screen:** Select `5`, enter a low grade (e.g., 6), show the At Risk
result. Then select `6`, show the batch summary.

---

### [4:50 – 6:00] Visualizations (70 sec)

> "Finally, Option 7 generates five Matplotlib charts and saves them to
> the charts folder: the performance distribution across all five
> categories, an attendance histogram, a marks distribution, a study
> hours histogram, and a correlation heatmap showing how study hours and
> attendance relate to final grades. You can see attendance and study
> hours are both strongly positively correlated with final grade — which
> matches educational intuition and validates the dataset."

**On screen:** Select `7`, then open and briefly show each of the 5 PNGs
in `charts/`.

---

### [6:00 – 6:40] Wrap-up (40 sec)

> "To summarize: this project uses a real UCI dataset, implements Linear
> Search and Merge Sort manually with documented time and space
> complexity, applies a transparent rule-based prediction engine, and
> visualizes the results — all wrapped in a clean, modular, professionally
> structured codebase with logging, type hints, and error handling
> throughout.
>
> The full source code, README, and project report are in the GitHub
> repository linked in the description. Thanks for watching!"

**On screen:** Show the GitHub repo page / README.

---

## Recording Checklist
- [ ] Terminal font size increased for readability
- [ ] Full run rehearsed once before recording (avoid live typos)
- [ ] Charts folder opened in an image viewer for the visualization segment
- [ ] Background noise minimized; consistent narration pace
- [ ] Final video trimmed to stay within 5–8 minutes
