"""
Student Performance Analytics System - Helper Functions
All reusable calculations and data processing.
Uses NumPy for numerical operations and Pandas for data handling.
"""

import numpy as np
import pandas as pd


# ------------------------------------------------------------------
# Core calculations
# ------------------------------------------------------------------
def calculate_total_and_average(df, subject_cols):
    """Calculate total marks and average for each student using NumPy."""
    marks_array = df[subject_cols].to_numpy(dtype=float)
    totals = np.sum(marks_array, axis=1)
    averages = np.mean(marks_array, axis=1)
    result = df.copy()
    result["Total"] = totals
    result["Average"] = np.round(averages, 2)
    return result


def assign_grade(average):
    """
    Assign grade based on average marks.
        >= 90 → A+ | >= 80 → A | >= 70 → B
        >= 60 → C  | >= 50 → D | < 50 → F
    """
    if average >= 90:
        return "A+"
    elif average >= 80:
        return "A"
    elif average >= 70:
        return "B"
    elif average >= 60:
        return "C"
    elif average >= 50:
        return "D"
    else:
        return "F"


def apply_grades(df):
    """Apply grade assignment to every student using a loop."""
    grades = []
    for avg in df["Average"]:
        grades.append(assign_grade(avg))
    result = df.copy()
    result["Grade"] = grades
    return result


def determine_pass_fail(df, pass_mark=50, min_attendance=75):
    """Pass if Average >= pass_mark AND Attendance >= min_attendance."""
    status = []
    for avg, att in zip(df["Average"], df["Attendance"]):
        if avg >= pass_mark and att >= min_attendance:
            status.append("Pass")
        else:
            status.append("Fail")
    result = df.copy()
    result["Status"] = status
    return result


def add_rank(df):
    """Add class Rank column (1 = highest average). Ties get same rank style via dense."""
    result = df.copy()
    result["Rank"] = result["Average"].rank(method="min", ascending=False).astype(int)
    return result


# ------------------------------------------------------------------
# Aggregations & insights
# ------------------------------------------------------------------
def get_highest_lowest_average(df):
    """Return highest, lowest and overall average using NumPy."""
    averages = df["Average"].to_numpy()
    highest = float(np.max(averages))
    lowest = float(np.min(averages))
    overall_avg = float(np.round(np.mean(averages), 2))
    return highest, lowest, overall_avg


def subject_wise_analysis(df, subject_cols):
    """Per-subject Highest, Lowest, Average, Std Dev using NumPy."""
    analysis = {}
    for subject in subject_cols:
        marks = df[subject].to_numpy(dtype=float)
        analysis[subject] = {
            "Highest": float(np.max(marks)),
            "Lowest": float(np.min(marks)),
            "Average": float(np.round(np.mean(marks), 2)),
            "Std Dev": float(np.round(np.std(marks), 2)),
        }
    return analysis


def get_top_performers(df, n=5):
    """Top N students by Average."""
    cols = ["Rank", "Student_ID", "Name", "Department", "Total", "Average", "Grade", "Attendance", "Status"]
    cols = [c for c in cols if c in df.columns]
    return df.nlargest(n, "Average")[cols].reset_index(drop=True)


def get_bottom_performers(df, n=5):
    """Bottom N students by Average."""
    cols = ["Rank", "Student_ID", "Name", "Department", "Total", "Average", "Grade", "Attendance", "Status"]
    cols = [c for c in cols if c in df.columns]
    return df.nsmallest(n, "Average")[cols].reset_index(drop=True)


def get_department_summary(df):
    """Department-wise performance summary."""
    summary = (
        df.groupby("Department")
        .agg(
            Students=("Student_ID", "count"),
            Avg_Marks=("Average", "mean"),
            Pass_Count=("Status", lambda x: (x == "Pass").sum()),
            Avg_Attendance=("Attendance", "mean"),
            Highest=("Average", "max"),
            Lowest=("Average", "min"),
        )
        .reset_index()
    )
    summary["Avg_Marks"] = summary["Avg_Marks"].round(2)
    summary["Avg_Attendance"] = summary["Avg_Attendance"].round(2)
    summary["Highest"] = summary["Highest"].round(2)
    summary["Lowest"] = summary["Lowest"].round(2)
    summary["Pass_Rate_%"] = (
        (summary["Pass_Count"] / summary["Students"]) * 100
    ).round(1)
    return summary.sort_values("Avg_Marks", ascending=False).reset_index(drop=True)


def get_grade_distribution(df):
    """Ordered grade counts."""
    order = ["A+", "A", "B", "C", "D", "F"]
    counts = df["Grade"].value_counts()
    return counts.reindex([g for g in order if g in counts.index])


def get_pass_fail_counts(df):
    """Pass / Fail counts."""
    return df["Status"].value_counts()


def get_attendance_stats(df):
    """Attendance statistics using NumPy."""
    att = df["Attendance"].to_numpy(dtype=float)
    return {
        "Average": float(np.round(np.mean(att), 2)),
        "Highest": float(np.max(att)),
        "Lowest": float(np.min(att)),
        "Below_75": int(np.sum(att < 75)),
    }


def get_at_risk_students(df, avg_threshold=60, att_threshold=75):
    """Students with low average or low attendance."""
    mask = (df["Average"] < avg_threshold) | (df["Attendance"] < att_threshold)
    cols = ["Rank", "Student_ID", "Name", "Department", "Average", "Attendance", "Grade", "Status"]
    cols = [c for c in cols if c in df.columns]
    return df.loc[mask, cols].sort_values("Average").reset_index(drop=True)


def generate_insights(df, subject_cols):
    """
    Auto-generate plain-English insights from the data.
    Returns a list of insight strings.
    """
    insights = []
    total = len(df)
    highest, lowest, overall = get_highest_lowest_average(df)
    pf = get_pass_fail_counts(df)
    passed = int(pf.get("Pass", 0))
    failed = int(pf.get("Fail", 0))
    pass_rate = round((passed / total) * 100, 1) if total else 0

    # Top student
    top = df.loc[df["Average"].idxmax()]
    insights.append(
        f"🥇 Top student is **{top['Name']}** ({top['Student_ID']}) with **{top['Average']}%** average ({top['Grade']})."
    )

    # Class average
    insights.append(f"📊 Class average is **{overall}%** across **{total}** students.")

    # Pass rate
    insights.append(
        f"{'✅' if pass_rate >= 75 else '⚠️'} Pass rate is **{pass_rate}%** ({passed} passed, {failed} failed)."
    )

    # Best / worst subject
    analysis = subject_wise_analysis(df, subject_cols)
    best_subj = max(analysis, key=lambda s: analysis[s]["Average"])
    worst_subj = min(analysis, key=lambda s: analysis[s]["Average"])
    insights.append(
        f"📚 Strongest subject: **{best_subj}** ({analysis[best_subj]['Average']}%). "
        f"Weakest: **{worst_subj}** ({analysis[worst_subj]['Average']}%)."
    )

    # Best department
    dept = get_department_summary(df)
    if not dept.empty:
        best_dept = dept.iloc[0]
        insights.append(
            f"🏢 Best department: **{best_dept['Department']}** "
            f"(avg {best_dept['Avg_Marks']}%, pass rate {best_dept['Pass_Rate_%']}%)."
        )

    # Attendance
    att = get_attendance_stats(df)
    if att["Below_75"] > 0:
        insights.append(
            f"📅 **{att['Below_75']}** student(s) have attendance below 75% (class avg attendance: {att['Average']}%)."
        )
    else:
        insights.append(f"📅 All students have attendance ≥ 75% (class avg: {att['Average']}%).")

    # At risk
    risk = get_at_risk_students(df, avg_threshold=60, att_threshold=75)
    if len(risk) > 0:
        insights.append(f"🔻 **{len(risk)}** student(s) may need extra attention (low average or attendance).")
    else:
        insights.append("🌟 No students currently flagged as at-risk.")

    return insights