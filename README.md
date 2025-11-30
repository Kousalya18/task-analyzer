Smart Task Analyzer – Full Stack Assignment (Django + JavaScript)

This project is a Smart Task Analyzer that helps users organize tasks based on priority, deadlines, importance, and dependencies.
It provides intelligent scoring and sorting modes to help users decide which task to work on first.

This is the submission for the Singularium Internship Assignment 2025.

📌 Features
🔹 1. Intelligent Task Scoring

Each task is scored using:

Importance (1–10 scale)

Deadline urgency

Estimated hours

Dependencies

Sorting mode selected

🔹 2. Four Sorting Modes
Mode	Behavior
smart	Balanced: importance, urgency, hours
fastest	Smallest estimated hours first
impact	Highest importance first
deadline	Urgent tasks first
🔹 3. Full REST API

Backend built using Django + DRF:

Method	Endpoint	Description
POST	/api/tasks/analyze/	Returns sorted tasks with score + reasons
POST	/api/tasks/suggest/	Suggests next best tasks
🔹 4. Simple Frontend UI

Built using:

HTML

CSS

JavaScript (Fetch API)

The frontend allows:
✔ Add tasks manually
✔ Paste JSON array of tasks
✔ Select sorting mode
✔ View results with scores & explanations

🗂 Project Structure
task-analyzer/
│
├── backend/            # Django REST API
│   ├── backend/        # Project settings
│   ├── tasks/          # App containing APIs
│   └── manage.py
│
├── frontend/           # HTML, CSS, JS frontend
│   ├── index.html
│   ├── script.js
│   └── styles.css
│
├── venv/               # Python virtual environment
│
└── README.md

🚀 How to Run the Project
1️⃣ Activate the Virtual Environment
cd task-analyzer
venv\Scripts\activate

2️⃣ Start the Backend Server
cd backend
python manage.py runserver


Backend runs at:

http://127.0.0.1:8000/

3️⃣ Open the Frontend

Go to:

task-analyzer/frontend/index.html


Double-click to open it in browser.

💡 API Usage Example (POST /analyze)

Request Body:

[
  {
    "id": "t1",
    "title": "Fix login bug",
    "importance": 8,
    "estimated_hours": 3,
    "due_date": "2025-12-05",
    "dependencies": []
  }
]


Response Example:

{
  "tasks": [
    {
      "id": "t1",
      "title": "Fix login bug",
      "score": 38.1,
      "reasons": ["High importance"]
    }
  ]
}

🧰 Tech Stack
Backend

Python

Django

Django REST Framework

python-dateutil

django-cors-headers

Frontend

HTML

JavaScript

CSS

🎯 Status: Completed

This project meets all requirements and is ready for submission.