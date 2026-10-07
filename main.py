"""
Student Performance Analytics System
Full-fledged interactive dashboard
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from functions import (
    calculate_total_and_average,
    apply_grades,
    determine_pass_fail,
    add_rank,
    get_highest_lowest_average,
    subject_wise_analysis,
    get_top_performers,
    get_bottom_performers,
    get_department_summary,
    get_grade_distribution,
    get_pass_fail_counts,
    get_attendance_stats,
    get_at_risk_students,
    generate_insights,
)

# ------------------------------------------------------------------
# Page config
# ------------------------------------------------------------------
st.set_page_config(
    page_title="Student Performance Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ------------------------------------------------------------------
# CSS
# ------------------------------------------------------------------
st.markdown("""
<style>
.block-container { padding-top: 1.5rem; padding-bottom: 2rem; }

div[data-testid="stMetric"] {
    background: linear-gradient(145deg, #1e293b, #0f172a);
    border: 1px solid #334155;
    border-radius: 14px;
    padding: 18px 14px 14px 18px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.35);
}
div[data-testid="stMetric"] label {
    color: #94a3b8 !important;
    font-size: 0.78rem !important;
    font-weight: 600 !important;
    text-transform: uppercase;
    letter-spacing: 0.4px;
}
div[data-testid="stMetric"] [data-testid="stMetricValue"] {
    color: #f8fafc !important;
    font-size: 1.65rem !important;
    font-weight: 700 !important;
}
div[data-testid="stMetric"] [data-testid="stMetricDelta"] {
    font-size: 0.8rem !important;
}

h1 {
    text-align: center !important;
    font-weight: 800 !important;
    letter-spacing: -0.6px;
    margin-bottom: 0.15rem !important;
}
.subtitle {
    text-align: center;
    color: #94a3b8;
    font-size: 0.95rem;
    margin-bottom: 1.8rem;
}

div[data-testid="stDataFrame"] {
    border-radius: 12px;
    border: 1px solid #334155;
    overflow: hidden;
}

.summary-card {
    background: linear-gradient(145deg, #1e293b, #0f172a);
    border: 1px solid #334155;
    border-radius: 14px;
    padding: 1.25rem 1.5rem;
    margin-top: 0.5rem;
    line-height: 1.7;
}
.summary-card h3 {
    margin-top: 0;
    margin-bottom: 0.75rem;
}

footer { visibility: hidden; }
#MainMenu { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------
# Plotly theme helper
# ------------------------------------------------------------------
CHART_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#e2e8f0", size=13),
    margin=dict(l=40, r=20, t=40, b=40),
    xaxis=dict(gridcolor="#334155", zeroline=False),
    yaxis=dict(gridcolor="#334155", zeroline=False),
)

COLOR_SEQUENCE = ["#6366f1", "#22d3ee", "#a78bfa", "#34d399", "#fbbf24", "#f87171", "#fb7185"]


def style_fig(fig, height=320):
    fig.update_layout(**CHART_LAYOUT, height=height)
    return fig


# ------------------------------------------------------------------
# Sidebar
# ------------------------------------------------------------------
st.sidebar.markdown("## ⚙️ Controls")
st.sidebar.markdown("---")

uploaded_file = st.sidebar.file_uploader(
    "📁 Upload CSV (optional)",
    type=["csv"],
    help="Columns: Student_ID, Name, Department, subject marks…, Attendance",
)

st.sidebar.markdown("### 🎯 Pass Criteria")
pass_mark = st.sidebar.slider("Minimum Average to Pass", 40, 70, 50, 5)
min_attendance = st.sidebar.slider("Minimum Attendance %", 60, 90, 75, 5)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📌 How to use")
st.sidebar.markdown("""
1. Data loads from **students.csv** by default  
2. Upload your own CSV if needed  
3. Adjust pass criteria with the sliders  
4. Explore the analysis tabs  
""")

# ------------------------------------------------------------------
# Load data
# ------------------------------------------------------------------
@st.cache_data(show_spinner="Loading data…")
def load_data(file):
    if file is not None:
        return pd.read_csv(file)
    return pd.read_csv("students.csv")


try:
    df_raw = load_data(uploaded_file)
except Exception as e:
    st.error(f"Could not load data: {e}")
    st.stop()

required = {"Student_ID", "Name", "Department", "Attendance"}
missing = required - set(df_raw.columns)
if missing:
    st.error(f"Missing required columns: {', '.join(missing)}")
    st.stop()

all_cols = list(df_raw.columns)
dept_idx = all_cols.index("Department")
att_idx = all_cols.index("Attendance")
subject_cols = all_cols[dept_idx + 1 : att_idx]

if not subject_cols:
    st.error("No subject mark columns found between Department and Attendance.")
    st.stop()

# ------------------------------------------------------------------
# Process pipeline
# ------------------------------------------------------------------
df = calculate_total_and_average(df_raw, subject_cols)
df = apply_grades(df)
df = determine_pass_fail(df, pass_mark=pass_mark, min_attendance=min_attendance)
df = add_rank(df)

# ------------------------------------------------------------------
# Header
# ------------------------------------------------------------------
st.title("📊 Student Performance Analytics System")
st.markdown('<p class="subtitle">Full Interactive Dashboard</p>', unsafe_allow_html=True)

# ------------------------------------------------------------------
# Top metrics
# ------------------------------------------------------------------
highest, lowest, overall_avg = get_highest_lowest_average(df)
pass_fail = get_pass_fail_counts(df)
total_students = len(df)
passed = int(pass_fail.get("Pass", 0))
failed = int(pass_fail.get("Fail", 0))
pass_rate = round((passed / total_students) * 100, 1) if total_students else 0
att_stats = get_attendance_stats(df)

m1, m2, m3, m4, m5 = st.columns(5)
m1.metric("Total Students", total_students)
m2.metric("Class Average", f"{overall_avg}%")
m3.metric("Highest Average", f"{highest}%")
m4.metric("Lowest Average", f"{lowest}%")
m5.metric("Pass Rate", f"{pass_rate}%", delta=f"{passed} Pass · {failed} Fail")

# ------------------------------------------------------------------
# Auto Insights
# ------------------------------------------------------------------
with st.expander("💡 Auto Insights — click to expand", expanded=True):
    for line in generate_insights(df, subject_cols):
        st.markdown(f"- {line}")

# ------------------------------------------------------------------
# Student Search
# ------------------------------------------------------------------
st.markdown("### 🔎 Search Student")
_search_labels = [f"{r.Student_ID} — {r.Name} ({r.Department})" for r in df.itertuples()]
_label_to_idx = {label: i for i, label in enumerate(_search_labels)}

selected_label = st.selectbox(
    "Type to filter, then click a student",
    options=_search_labels,
    index=None,
    placeholder="Type a name or ID…",
    key="global_search_select",
)

if selected_label is not None:
    s = df.iloc[_label_to_idx[selected_label]]
    header_msg = f"👤 **{s['Name']}**  ·  `{s['Student_ID']}`  ·  Rank **#{s['Rank']}**  ·  **{s['Status']}**"
    if s["Status"] == "Pass":
        st.success(header_msg)
    else:
        st.error(header_msg)

    d1, d2, d3, d4, d5 = st.columns(5)
    d1.metric("Department", s["Department"])
    d2.metric("Total Marks", int(s["Total"]))
    d3.metric("Average", f"{s['Average']}%")
    d4.metric("Grade", s["Grade"])
    d5.metric("Attendance", f"{int(s['Attendance'])}%")

    subj_data = {col: int(s[col]) for col in subject_cols}
    st.markdown("**Subject Marks**")
    st.dataframe(pd.DataFrame([subj_data]), use_container_width=True, hide_index=True)

    # Print-friendly summary card
    st.markdown("#### 🖨️ Printable Summary Card")
    subjects_html = " · ".join([f"<b>{c}</b>: {int(s[c])}" for c in subject_cols])
    card_border = "#22c55e" if s["Status"] == "Pass" else "#ef4444"
    st.markdown(
        f"""
        <div class="summary-card" style="border-left: 4px solid {card_border};">
            <h3>{s['Name']} &nbsp;|&nbsp; {s['Student_ID']} &nbsp;|&nbsp; Rank #{s['Rank']}</h3>
            <b>Department:</b> {s['Department']}<br>
            <b>Total:</b> {int(s['Total'])} &nbsp;·&nbsp; <b>Average:</b> {s['Average']}% &nbsp;·&nbsp;
            <b>Grade:</b> {s['Grade']} &nbsp;·&nbsp; <b>Status:</b> {s['Status']}<br>
            <b>Attendance:</b> {int(s['Attendance'])}%<br>
            <b>Subjects:</b> {subjects_html}
        </div>
        """,
        unsafe_allow_html=True,
    )

st.divider()

# ------------------------------------------------------------------
# Colour helpers
# ------------------------------------------------------------------
def colour_status(val):
    if val == "Pass":
        return "background-color:#14532d;color:#bbf7d0;font-weight:600"
    return "background-color:#7f1d1d;color:#fecaca;font-weight:600"

def colour_grade(val):
    return {
        "A+": "background-color:#14532d;color:#bbf7d0;font-weight:600",
        "A":  "background-color:#166534;color:#dcfce7;font-weight:600",
        "B":  "background-color:#713f12;color:#fef08a;font-weight:600",
        "C":  "background-color:#9a3412;color:#fdba74;font-weight:600",
        "D":  "background-color:#9a3412;color:#fed7aa;font-weight:600",
        "F":  "background-color:#7f1d1d;color:#fca5a5;font-weight:600",
    }.get(val, "")

# ------------------------------------------------------------------
# Tabs
# ------------------------------------------------------------------
tabs = st.tabs([
    "📋 All Records",
    "🏆 Top Performers",
    "📉 Needs Attention",
    "📚 Subjects",
    "🏢 Departments",
    "📈 Grades & Distribution",
    "⚖️ Compare Students",
    "🔍 Custom Filter",
])

# ========== TAB 0 : All Records ==========
with tabs[0]:
    st.subheader("Complete Student Performance Table")
    st.caption("Includes class Rank · totals and averages via NumPy.")

    display_cols = [
        "Rank", "Student_ID", "Name", "Department",
        *subject_cols, "Attendance", "Total", "Average", "Grade", "Status",
    ]

    styled = (
        df.sort_values("Rank")[display_cols]
        .style.map(colour_status, subset=["Status"])
        .map(colour_grade, subset=["Grade"])
        .format({"Average": "{:.2f}", "Total": "{:.0f}"})
    )
    st.dataframe(styled, use_container_width=True, height=460, hide_index=True)

    st.download_button(
        "⬇️ Download CSV",
        df.sort_values("Rank")[display_cols].to_csv(index=False).encode("utf-8"),
        "student_performance_processed.csv",
        "text/csv",
    )

# ========== TAB 1 : Top Performers ==========
with tabs[1]:
    st.subheader("🏆 Top Performing Students")
    n_top = st.slider("Show top", 3, 10, 5, key="top_n")
    top_df = get_top_performers(df, n=n_top)

    st.dataframe(
        top_df.style
        .format({"Average": "{:.2f}", "Total": "{:.0f}"})
        .map(colour_grade, subset=["Grade"])
        .map(colour_status, subset=["Status"]),
        use_container_width=True,
        hide_index=True,
    )

    if not top_df.empty:
        gold = top_df.iloc[0]
        st.success(
            f"🥇 **Gold Medalist — {gold['Name']}** ({gold['Student_ID']})  \n"
            f"Rank **#{gold['Rank']}** · **{gold['Department']}** · "
            f"Average **{gold['Average']}%** · Grade **{gold['Grade']}**"
        )

# ========== TAB 2 : Needs Attention ==========
with tabs[2]:
    st.subheader("📉 Students Who Need Attention")
    risk_avg = st.slider("Flag if Average below", 40, 70, 60, 5, key="risk_avg")
    at_risk = get_at_risk_students(df, avg_threshold=risk_avg, att_threshold=min_attendance)

    if at_risk.empty:
        st.success("🎉 No students currently flagged as at-risk.")
    else:
        st.warning(f"**{len(at_risk)}** student(s) need attention")
        st.dataframe(
            at_risk.style.format({"Average": "{:.2f}"})
            .map(colour_grade, subset=["Grade"])
            .map(colour_status, subset=["Status"]),
            use_container_width=True,
            hide_index=True,
        )

    st.markdown("#### Bottom Performers")
    bottom = get_bottom_performers(df, n=5)
    st.dataframe(
        bottom.style.format({"Average": "{:.2f}", "Total": "{:.0f}"})
        .map(colour_grade, subset=["Grade"])
        .map(colour_status, subset=["Status"]),
        use_container_width=True,
        hide_index=True,
    )

# ========== TAB 3 : Subjects ==========
with tabs[3]:
    st.subheader("📚 Subject-wise Performance")
    analysis = subject_wise_analysis(df, subject_cols)

    subj_cols_ui = st.columns(len(subject_cols))
    for i, subj in enumerate(subject_cols):
        with subj_cols_ui[i]:
            st.metric(
                label=subj,
                value=f"{analysis[subj]['Average']}%",
                delta=f"H {analysis[subj]['Highest']} · L {analysis[subj]['Lowest']}",
                delta_color="off",
            )

    chart_df = pd.DataFrame({
        "Subject": list(analysis.keys()),
        "Average": [v["Average"] for v in analysis.values()],
    })
    fig = px.bar(
        chart_df, x="Subject", y="Average", color="Subject",
        color_discrete_sequence=COLOR_SEQUENCE,
        text="Average", title="Average Marks by Subject",
    )
    fig.update_traces(textposition="outside", marker_line_width=0)
    st.plotly_chart(style_fig(fig, 360), use_container_width=True)

    stats = pd.DataFrame(analysis).T
    stats.index.name = "Subject"
    st.dataframe(stats.style.format("{:.2f}"), use_container_width=True, hide_index=False)

    best_subj = max(analysis, key=lambda s: analysis[s]["Average"])
    worst_subj = min(analysis, key=lambda s: analysis[s]["Average"])
    c1, c2 = st.columns(2)
    c1.success(f"✅ **Strongest:** {best_subj} ({analysis[best_subj]['Average']}%)")
    c2.error(f"⚠️ **Weakest:** {worst_subj} ({analysis[worst_subj]['Average']}%)")

# ========== TAB 4 : Departments ==========
with tabs[4]:
    st.subheader("🏢 Department-wise Summary")
    dept = get_department_summary(df)
    st.dataframe(
        dept.style.format({
            "Avg_Marks": "{:.2f}", "Avg_Attendance": "{:.2f}",
            "Highest": "{:.2f}", "Lowest": "{:.2f}", "Pass_Rate_%": "{:.1f}",
        }),
        use_container_width=True,
        hide_index=True,
    )

    left, right = st.columns(2)
    with left:
        fig1 = px.bar(
            dept, x="Department", y="Avg_Marks", color="Department",
            color_discrete_sequence=COLOR_SEQUENCE, text="Avg_Marks",
            title="Average Marks by Department",
        )
        fig1.update_traces(textposition="outside", marker_line_width=0)
        st.plotly_chart(style_fig(fig1), use_container_width=True)
    with right:
        fig2 = px.bar(
            dept, x="Department", y="Pass_Rate_%", color="Department",
            color_discrete_sequence=COLOR_SEQUENCE, text="Pass_Rate_%",
            title="Pass Rate (%) by Department",
        )
        fig2.update_traces(textposition="outside", marker_line_width=0)
        st.plotly_chart(style_fig(fig2), use_container_width=True)

# ========== TAB 5 : Grades & Distribution ==========
with tabs[5]:
    st.subheader("📈 Grades & Average Distribution")

    grade_dist = get_grade_distribution(df)
    gtable = grade_dist.reset_index()
    gtable.columns = ["Grade", "Count"]

    left, right = st.columns(2)
    with left:
        fig_g = px.bar(
            gtable, x="Grade", y="Count", color="Grade",
            color_discrete_sequence=COLOR_SEQUENCE, text="Count",
            title="Students per Grade",
        )
        fig_g.update_traces(textposition="outside", marker_line_width=0)
        st.plotly_chart(style_fig(fig_g), use_container_width=True)
    with right:
        pf = pass_fail.reset_index()
        pf.columns = ["Status", "Count"]
        fig_pf = px.pie(
            pf, names="Status", values="Count",
            color="Status",
            color_discrete_map={"Pass": "#22c55e", "Fail": "#ef4444"},
            title="Pass / Fail Split",
            hole=0.45,
        )
        fig_pf.update_layout(**CHART_LAYOUT, height=320)
        st.plotly_chart(fig_pf, use_container_width=True)

    st.markdown("#### Distribution of Student Averages")
    fig_hist = px.histogram(
        df, x="Average", nbins=10,
        color_discrete_sequence=["#6366f1"],
        title="How averages are spread across the class",
    )
    fig_hist.update_traces(marker_line_width=1, marker_line_color="#0f172a")
    st.plotly_chart(style_fig(fig_hist, 340), use_container_width=True)

    st.markdown("#### Attendance Overview")
    a1, a2, a3, a4 = st.columns(4)
    a1.metric("Avg Attendance", f"{att_stats['Average']}%")
    a2.metric("Highest", f"{att_stats['Highest']}%")
    a3.metric("Lowest", f"{att_stats['Lowest']}%")
    a4.metric("Below 75%", att_stats["Below_75"])

# ========== TAB 6 : Compare Students ==========
with tabs[6]:
    st.subheader("⚖️ Compare Two Students")
    st.caption("Pick any two students to compare marks, average, grade and attendance side by side.")

    labels = [f"{r.Student_ID} — {r.Name}" for r in df.itertuples()]
    label_map = {f"{r.Student_ID} — {r.Name}": i for i, r in enumerate(df.itertuples())}

    c1, c2 = st.columns(2)
    with c1:
        pick_a = st.selectbox("Student A", labels, index=0, key="cmp_a")
    with c2:
        pick_b = st.selectbox("Student B", labels, index=min(1, len(labels) - 1), key="cmp_b")

    if pick_a and pick_b:
        sa = df.iloc[label_map[pick_a]]
        sb = df.iloc[label_map[pick_b]]

        left, right = st.columns(2)
        for col, s in ((left, sa), (right, sb)):
            with col:
                border = "#22c55e" if s["Status"] == "Pass" else "#ef4444"
                st.markdown(
                    f"""
                    <div class="summary-card" style="border-left: 4px solid {border};">
                        <h3>{s['Name']}</h3>
                        <b>ID:</b> {s['Student_ID']} &nbsp;·&nbsp; <b>Rank:</b> #{s['Rank']}<br>
                        <b>Department:</b> {s['Department']}<br>
                        <b>Total:</b> {int(s['Total'])} &nbsp;·&nbsp; <b>Average:</b> {s['Average']}%<br>
                        <b>Grade:</b> {s['Grade']} &nbsp;·&nbsp; <b>Status:</b> {s['Status']}<br>
                        <b>Attendance:</b> {int(s['Attendance'])}%
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        # Subject comparison chart
        cmp_data = []
        for subj in subject_cols:
            cmp_data.append({"Subject": subj, "Student": sa["Name"], "Marks": int(sa[subj])})
            cmp_data.append({"Subject": subj, "Student": sb["Name"], "Marks": int(sb[subj])})
        cmp_df = pd.DataFrame(cmp_data)

        fig_cmp = px.bar(
            cmp_df, x="Subject", y="Marks", color="Student",
            barmode="group",
            color_discrete_sequence=["#6366f1", "#22d3ee"],
            text="Marks",
            title="Subject-wise Comparison",
        )
        fig_cmp.update_traces(textposition="outside", marker_line_width=0)
        st.plotly_chart(style_fig(fig_cmp, 380), use_container_width=True)

        # Winner summary
        if sa["Average"] > sb["Average"]:
            st.info(f"📌 **{sa['Name']}** has the higher average ({sa['Average']}% vs {sb['Average']}%).")
        elif sb["Average"] > sa["Average"]:
            st.info(f"📌 **{sb['Name']}** has the higher average ({sb['Average']}% vs {sa['Average']}%).")
        else:
            st.info("📌 Both students have the same average.")

# ========== TAB 7 : Custom Filter ==========
with tabs[7]:
    st.subheader("🔍 Custom Filter & Search")

    f1, f2, f3 = st.columns(3)
    with f1:
        depts = ["All"] + sorted(df["Department"].unique().tolist())
        sel_dept = st.selectbox("Department", depts)
    with f2:
        sel_status = st.multiselect("Status", ["Pass", "Fail"], default=["Pass", "Fail"])
    with f3:
        sel_grade = st.multiselect(
            "Grade", ["A+", "A", "B", "C", "D", "F"],
            default=["A+", "A", "B", "C", "D", "F"],
        )

    if st.button("🔄 Reset filters"):
        st.rerun()

    st.markdown("#### 🔎 Search by Name / ID")
    filtered = df.copy()
    if sel_dept != "All":
        filtered = filtered[filtered["Department"] == sel_dept]
    filtered = filtered[filtered["Status"].isin(sel_status)]
    filtered = filtered[filtered["Grade"].isin(sel_grade)]

    tab_labels = [f"{r.Student_ID} — {r.Name} ({r.Department})" for r in filtered.itertuples()]
    tab_label_to_pos = {label: i for i, label in enumerate(tab_labels)}

    tab_choice = st.selectbox(
        "Type to filter, then click a student",
        options=tab_labels if tab_labels else ["No matches"],
        index=None,
        placeholder="Type a name or ID…",
        key="tab_search_select",
        disabled=not tab_labels,
    )

    if tab_choice is not None and tab_labels:
        chosen = filtered.iloc[tab_label_to_pos[tab_choice]]
        msg = (
            f"**{chosen['Name']}** ({chosen['Student_ID']}) · Rank #{chosen['Rank']} · "
            f"{chosen['Department']} · Avg **{chosen['Average']}%** · "
            f"Grade **{chosen['Grade']}** · **{chosen['Status']}**"
        )
        if chosen["Status"] == "Pass":
            st.success(msg)
        else:
            st.error(msg)

    st.markdown(f"**{len(filtered)}** student(s) match your filters")

    if len(filtered) > 0:
        st.dataframe(
            filtered[[
                "Rank", "Student_ID", "Name", "Department", "Total",
                "Average", "Grade", "Attendance", "Status",
            ]]
            .sort_values("Rank")
            .style.format({"Average": "{:.2f}"})
            .map(colour_grade, subset=["Grade"])
            .map(colour_status, subset=["Status"]),
            use_container_width=True,
            height=380,
            hide_index=True,
        )
        fh, fl, fa = get_highest_lowest_average(filtered)
        q1, q2, q3 = st.columns(3)
        q1.metric("Highest Avg (filtered)", f"{fh}%")
        q2.metric("Lowest Avg (filtered)", f"{fl}%")
        q3.metric("Group Average", f"{fa}%")
    else:
        st.info("No students match the current filters.")

# ------------------------------------------------------------------
st.divider()
st.caption("Student Performance Analytics System")