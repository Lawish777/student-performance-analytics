# Student Performance Analytics System

**Python Project Assignment – EWB Courses | Python with AI**

| Item | Details |
|------|---------|
| **Project Title** | Student Performance Analytics System |
| **Technology** | Python, NumPy, Pandas, Streamlit |
| **Concepts Covered** | Variables, Data Types, Loops, Functions, NumPy, Pandas, Data Analysis |
| **Submission Deadline** | 15 October 2026 |

---

## 1. Project Title & Student Details

**Student Performance Analytics System**  
  Lawish Kumar
---

## 2. Objective

The goal of this project is to build a complete Python-based system that:

- Reads student academic data from a CSV file
- Processes marks and attendance using **NumPy** and **Pandas**
- Calculates totals, averages, grades and pass/fail status
- Performs subject-wise and department-wise analysis
- Identifies top performers and overall class statistics
- Presents all results through a clean, interactive web dashboard

This solves the practical problem of manually analysing student performance and makes the insights immediately visible to teachers or administrators.

---

## 3. Technologies Used

| Technology | Purpose |
|------------|---------|
| **Python 3** | Core programming language |
| **Pandas** | Loading CSV, DataFrame operations, grouping, filtering |
| **NumPy** | Numerical calculations (sum, mean, max, min, std) |
| **Streamlit** | Interactive web UI / dashboard |
| **CSV** | Data storage format |

---

## 4. Dataset Description

File: `students.csv`

| Column | Description |
|--------|-------------|
| Student_ID | Unique identifier (S001, S002 …) |
| Name | Student full name |
| Department | Computer Science / Electronics / Mechanical / Civil |
| Maths, Physics, Chemistry, English | Subject marks (out of 100) |
| Attendance | Attendance percentage |

- **Number of records**: 20 realistic student records  
- Marks range from roughly 45 to 95  
- Attendance ranges from 60 % to 97 %

---

## 5. Implementation

### Step 1 – Prepare the Dataset
A CSV file (`students.csv`) containing 20 student records was created with realistic values.

### Step 2 – Read the Data
```python
df = pd.read_csv("students.csv")
```
Pandas is used to load the data and inspect columns, shape and basic info.

### Step 3 – Process the Data
All processing is done through reusable functions defined in `functions.py`:

| Function | What it does |
|----------|--------------|
| `calculate_total_and_average()` | Uses **NumPy** `np.sum` and `np.mean` to compute Total & Average |
| `assign_grade()` | Applies a clear grading rule (A+ to F) |
| `apply_grades()` | Loops over every student and assigns the grade |
| `determine_pass_fail()` | Pass if Average ≥ pass mark **and** Attendance ≥ 75 % |
| `get_highest_lowest_average()` | Uses NumPy max / min / mean |
| `subject_wise_analysis()` | Per-subject highest, lowest, average and standard deviation |
| `get_top_performers()` | Returns top-N students by average |
| `get_department_summary()` | Group-by department statistics |
| `get_grade_distribution()` | Count of each grade |
| `get_pass_fail_counts()` | Pass vs Fail counts |

### Step 4 – Perform Analysis
The dashboard answers the practical questions required by the assignment:

- Which student has the highest average?
- Which subject has the best average?
- How many students passed?
- What is the overall class average?
- Department-wise performance comparison

### Step 5 – Final Output
Results are presented in six interactive tabs:

1. **Student Records** – Full table with colour-coded grades and status  
2. **Top Performers** – Ranked list + gold medalist highlight  
3. **Subject Analysis** – Metrics + bar chart for every subject  
4. **Department Summary** – Aggregated statistics per department  
5. **Grade Distribution** – Visual breakdown of grades and pass/fail  
6. **Detailed Insights** – Filterable view by department and status  

Users can also upload their own CSV and adjust the pass criteria with sidebar sliders.

---

## 6. Key Features

- ✅ CSV dataset with 20 student records  
- ✅ Pandas DataFrame for data organisation  
- ✅ NumPy used for all major numerical calculations  
- ✅ Reusable functions for every calculation  
- ✅ Loops used for grade assignment and pass/fail logic  
- ✅ Total marks and average for each student  
- ✅ Clear grading rule (A+ / A / B / C / D / F)  
- ✅ Pass/Fail based on average **and** attendance  
- ✅ Highest, lowest and class average  
- ✅ Subject-wise performance analysis  
- ✅ Top-performing students list  
- ✅ Department-wise summary  
- ✅ Interactive Streamlit dashboard with filters and download  

---

## 7. How to Run the Project

### Prerequisites
```bash
pip install -r requirements.txt
```

### Launch the Dashboard
```bash
streamlit run main.py
```

The browser will open automatically at `http://localhost:8501`.

### Optional – Use Your Own Data
Upload a CSV with the same column structure via the sidebar file uploader.

---

## 8. Project Structure

```
student-performance-analytics/
├── main.py              # Streamlit application (entry point)
├── functions.py         # All reusable calculation functions
├── students.csv         # Sample dataset (20 records)
├── requirements.txt     # Python dependencies
└── README.md            # This documentation
```

---

## 9. Challenges & Learning

**Challenges faced**
- Deciding a fair pass/fail rule that combines marks and attendance
- Keeping all numerical work in NumPy while still using Pandas DataFrames
- Designing a clean UI that does not hide the underlying analysis

**What was learned**
- Practical use of NumPy vectorised operations (`np.sum`, `np.mean`, `np.max` …)
- Building modular code with pure functions
- Creating interactive data dashboards with Streamlit
- Importance of clear documentation and a reproducible project structure

---

## 10. GitHub Repository

After pushing the project, replace the line below with your actual repository URL:

```
https://github.com/<your-username>/student-performance-analytics
```

---

## Final Submission Checklist

- [x] Project completed and tested  
- [x] Student dataset included (`students.csv`)  
- [x] NumPy and Pandas used appropriately  
- [x] Functions and loops used where required  
- [x] GitHub repository created (to be done by student)  
- [x] Complete project pushed to GitHub (to be done by student)  
- [x] README.md added  
- [x] Documentation completed with Objectives, Implementation and Final Outcome  

**DEADLINE: 15 OCTOBER 2026**
