"""
visualization/charts.py
=========================
Generates all required Matplotlib visualizations from the in-memory
student dataset and saves each one as a PNG file into config.CHARTS_DIR.
"""

from collections import Counter
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

import config
from models import Student
from utils.logger import get_logger

logger = get_logger(__name__)


def _ensure_charts_directory_exists() -> None:
    """Create the charts/ output directory if it does not already exist."""
    Path(config.CHARTS_DIR).mkdir(parents=True, exist_ok=True)


def plot_performance_distribution(students: list[Student]) -> Path:
    """Generate a bar chart showing the count of students in each performance category."""
    category_order = [
        config.CATEGORY_EXCELLENT, config.CATEGORY_GOOD, config.CATEGORY_AVERAGE,
        config.CATEGORY_NEEDS_IMPROVEMENT, config.CATEGORY_AT_RISK,
    ]

    counts = Counter(s.performance_category for s in students if s.performance_category)
    if not counts:
        raise ValueError("No students have a predicted performance_category yet.")

    values = [counts.get(category, 0) for category in category_order]

    _ensure_charts_directory_exists()
    fig, ax = plt.subplots(figsize=(9, 6))
    bars = ax.bar(category_order, values, color=["#2E7D32", "#66BB6A", "#FBC02D", "#F57C00", "#C62828"])

    ax.set_title("Student Performance Distribution", fontsize=14, fontweight="bold")
    ax.set_xlabel("Performance Category")
    ax.set_ylabel("Number of Students")
    ax.grid(axis="y", linestyle="--", alpha=0.6)

    for bar, value in zip(bars, values):
        ax.annotate(str(value), xy=(bar.get_x() + bar.get_width() / 2, bar.get_height()),
                    xytext=(0, 3), textcoords="offset points", ha="center", fontsize=10)

    output_path = config.CHARTS_DIR / "performance_distribution.png"
    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)

    logger.info("Saved performance distribution chart to %s", output_path)
    return output_path


def plot_attendance_analysis(students: list[Student]) -> Path:
    """Generate a histogram of student attendance percentages."""
    attendance_values = [s.attendance_percentage for s in students]

    _ensure_charts_directory_exists()
    fig, ax = plt.subplots(figsize=(9, 6))
    ax.hist(attendance_values, bins=15, color="#1E88E5", edgecolor="black", alpha=0.85)

    ax.set_title("Attendance Analysis", fontsize=14, fontweight="bold")
    ax.set_xlabel("Attendance Percentage (%)")
    ax.set_ylabel("Number of Students")
    ax.grid(axis="y", linestyle="--", alpha=0.6)

    output_path = config.CHARTS_DIR / "attendance_analysis.png"
    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)

    logger.info("Saved attendance analysis chart to %s", output_path)
    return output_path


def plot_marks_distribution(students: list[Student]) -> Path:
    """Generate a histogram of student final grades (marks)."""
    grades = [s.final_grade for s in students]

    _ensure_charts_directory_exists()
    fig, ax = plt.subplots(figsize=(9, 6))
    ax.hist(grades, bins=range(0, 22, 2), color="#8E24AA", edgecolor="black", alpha=0.85)

    ax.set_title("Marks Distribution (Final Grade, 0-20 scale)", fontsize=14, fontweight="bold")
    ax.set_xlabel("Final Grade")
    ax.set_ylabel("Number of Students")
    ax.grid(axis="y", linestyle="--", alpha=0.6)

    output_path = config.CHARTS_DIR / "marks_distribution.png"
    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)

    logger.info("Saved marks distribution chart to %s", output_path)
    return output_path


def plot_study_hours_analysis(students: list[Student]) -> Path:
    """Generate a histogram of weekly student study hours."""
    study_hours = [s.study_hours for s in students]

    _ensure_charts_directory_exists()
    fig, ax = plt.subplots(figsize=(9, 6))
    ax.hist(study_hours, bins=10, color="#FB8C00", edgecolor="black", alpha=0.85)

    ax.set_title("Study Hours Analysis (Weekly)", fontsize=14, fontweight="bold")
    ax.set_xlabel("Study Hours per Week")
    ax.set_ylabel("Number of Students")
    ax.grid(axis="y", linestyle="--", alpha=0.6)

    output_path = config.CHARTS_DIR / "study_hours_analysis.png"
    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)

    logger.info("Saved study hours analysis chart to %s", output_path)
    return output_path


def plot_correlation_heatmap(students: list[Student]) -> Path:
    """Generate a correlation matrix heatmap across study hours, attendance, and final grade."""
    feature_names = ["Study Hours", "Attendance %", "Final Grade"]
    data_matrix = np.array([
        [s.study_hours for s in students],
        [s.attendance_percentage for s in students],
        [s.final_grade for s in students],
    ])

    correlation_matrix = np.corrcoef(data_matrix)

    _ensure_charts_directory_exists()
    fig, ax = plt.subplots(figsize=(7, 6))
    im = ax.imshow(correlation_matrix, cmap="coolwarm", vmin=-1, vmax=1)

    ax.set_xticks(range(len(feature_names)))
    ax.set_yticks(range(len(feature_names)))
    ax.set_xticklabels(feature_names, rotation=45, ha="right")
    ax.set_yticklabels(feature_names)
    ax.set_title("Correlation Matrix: Study Habits vs Performance", fontsize=13, fontweight="bold")

    for i in range(len(feature_names)):
        for j in range(len(feature_names)):
            ax.text(j, i, f"{correlation_matrix[i, j]:.2f}",
                    ha="center", va="center", color="black", fontsize=11)

    fig.colorbar(im, ax=ax, label="Correlation Coefficient")

    output_path = config.CHARTS_DIR / "correlation_heatmap.png"
    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)

    logger.info("Saved correlation heatmap chart to %s", output_path)
    return output_path


def generate_all_charts(students: list[Student]) -> list[Path]:
    """Generate all five required visualizations in one call."""
    generated_paths = [
        plot_performance_distribution(students),
        plot_attendance_analysis(students),
        plot_marks_distribution(students),
        plot_study_hours_analysis(students),
        plot_correlation_heatmap(students),
    ]

    logger.info("Generated all %d charts successfully.", len(generated_paths))
    return generated_paths
