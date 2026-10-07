# Project Documentation – Assessment Activity

## 1. Project Title
**Student Performance Analytics System**

- **Student Name:** ______________________________
- **Roll Number:** ______________________________
- **Batch / Course:** EWB Courses – Python with AI

---

## 2. Objective
This project was created to build a Python-based system that reads student academic data, processes it using NumPy and Pandas, and produces meaningful results such as marks summary, averages, grades, pass/fail statistics, subject-wise performance, and top performers.

It solves the problem of manually analysing student performance in spreadsheets by providing clear calculations, reusable functions, and an interactive dashboard for teachers or administrators.

---

## 3. Technologies Used
- **Python 3**
- **NumPy** – numerical calculations (sum, mean, max, min, standard deviation)
- **Pandas** – DataFrame loading, filtering, grouping, ranking
- **Streamlit** – interactive web dashboard
- **Plotly** – charts and visualisations
- **CSV** – dataset storage format

---

## 4. Dataset Description
**File:** `students.csv`

| Field | Description |
|-------|-------------|
| Student_ID | Unique student identifier |
| Name | Student full name |
| Department | Computer Science / Electronics / Mechanical / Civil |
| Maths, Physics, Chemistry, English | Subject marks (out of 100) |
| Attendance | Attendance percentage |

**Number of records:** 20 realistic student records

---

## 5. Implementation

### Step 1 – Prepare the Dataset
A CSV file (`students.csv`) was created with 20 student records including realistic marks and attendance values.

### Step 2 – Read the Data
Pandas is used to read the CSV file into a DataFrame. Columns, number of records, and basic structure are verified.

### Step 3 – Process the Data
Reusable functions in `functions.py` perform:
- Total and average calculation using **NumPy**
- Grade assignment using a loop and a clear grading rule
- Pass/Fail status using average and attendance conditions
- Class rank based on average marks

### Step 4 – Perform Analysis
The system answers practical questions such as:
- Which student has the highest average?
- Which subject has the best average?
- How many students passed?
- What is the overall class average?
- Which department performs best?
- Which students need attention?

### Step 5 – Final Output
Results are presented through:
- Summary metrics
- Auto-generated insights
- Student search
- Multiple analysis tabs (records, top performers, subjects, departments, grades, comparison, filters)
- Charts and downloadable processed CSV

---

## 6. Key Features
- Student dataset with ID, Name, Department, subject marks, and Attendance
- Pandas DataFrame for data organisation
- NumPy for numerical calculations
- Reusable functions for calculations and processing
- Loops for grade assignment and pass/fail logic
- Total marks and average marks for each student
- Grades based on a defined rule (A+ to F)
- Pass/Fail based on average and attendance
- Highest, lowest, and class average
- Subject-wise performance analysis
- Department-wise summary
- Top-performing students and rank
- At-risk / needs-attention list
- Student comparison
- Interactive dashboard with search and filters

---

## 7. Output / Screenshots (optional)
*(Add screenshots of the dashboard here after running the project: metrics, student table, subject charts, department summary, search result, etc.)*

---

## 8. Final Outcome
The project successfully:
- Loads and processes student data
- Calculates totals, averages, grades, ranks, and pass/fail status
- Produces subject-wise and department-wise analysis
- Identifies top performers and students who need attention
- Presents results clearly through an interactive dashboard

All required features from the assignment guidelines have been implemented using Python, NumPy, and Pandas concepts covered in the course.

---

## 9. Challenges & Learning

### Challenges faced
- Designing a fair pass/fail rule that uses both marks and attendance
- Keeping numerical work in NumPy while using Pandas DataFrames
- Organising analysis into a clear, readable interface

### What was learned
- Practical use of NumPy operations (`np.sum`, `np.mean`, `np.max`, `np.min`, `np.std`)
- Building modular code with reusable functions
- Using Pandas for filtering, grouping, and ranking
- Presenting data-analysis results in a structured way

---

## 10. GitHub Repository