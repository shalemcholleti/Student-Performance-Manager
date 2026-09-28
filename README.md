# Student Performance Manager

A beginner-friendly command-line Student Performance Management System built with Python's standard library.

## Features

- Add, view, search, update, and delete student records
- Store records in `data/students.csv`
- Export records to `data/students.json`
- Calculate average, grade, status, strongest subject, and weakest subject
- Search by ID or case-insensitive name
- Filter by average and pass/fail status
- Sort by name, average, Python, SQL, or Math
- Display top 3, 5, or 10 students
- Validate input without crashing on invalid values
- Unit tests using `unittest`

No Pandas, NumPy, SQL, Flask, FastAPI, Streamlit, or AI APIs are used.

## Requirements

- Python 3.10 or newer

## Run the application

From this directory:

```bash
python3 -m src.main
```

The application creates the `data` directory and CSV file as needed. Select **Export Report** from the menu to write the JSON export.

## Run tests

```bash
python3 -m unittest discover -s tests -v
```

## Grade and status rules

| Average | Grade | Status |
|---:|:---:|:---|
| 90–100 | A+ | Excellent |
| 80–89.99 | A | Excellent |
| 70–79.99 | B | Good |
| 60–69.99 | C | Needs Improvement |
| 50–59.99 | D | Needs Improvement |
| Below 50 | F | Failed |

## Project structure

```text
student-performance-manager/
├── README.md
├── data/
│   ├── students.csv
│   └── students.json
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── student.py
│   ├── file_handler.py
│   └── utils.py
└── tests/
    └── test_student.py
```
