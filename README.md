# Classroom Task Tracker

A beginner-friendly task manager built with **Python Flask**, HTML, CSS, JavaScript, and a local JSON file.

## Features

- Add a task with a title, subject, and Low / Medium / High priority.
- View all tasks and filter by All, Pending, or Completed.
- Mark a task completed or reopen it.
- Delete tasks.
- See total, pending, completed, and pending high-priority statistics.
- Save tasks in `tasks.json`, so they remain after the server restarts.
- Responsive layout for desktop, tablet, and mobile screens.

## Requirements

- Python 3.9 or newer
- pip

## Run the project

1. Open a terminal in this project folder.
2. (Recommended) Create and activate a virtual environment:

   **Windows**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

   **macOS / Linux**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install Flask:

   ```bash
   pip install -r requirements.txt
   ```

4. Start the Flask server:

   ```bash
   python app.py
   ```

5. Open this address in your browser:

   http://127.0.0.1:5000

The app creates or updates `tasks.json` automatically when tasks are added, updated, or deleted.

## Project structure

```text
classroom_task_tracker/
│
├── app.py                 # Flask routes, task functions, statistics
├── tasks.json             # Local task data (starts empty)
├── requirements.txt       # Python dependency
├── README.md              # Setup instructions
│
├── templates/
│   └── index.html         # Browser page
│
└── static/
    ├── style.css          # Responsive design
    └── app.js             # Frontend interactions and API calls
```

## Beginner Python concepts used

| Concept | Where it is used |
|---|---|
| Functions | `load_tasks()`, `save_tasks()`, `calculate_statistics()` |
| Lists | The collection of tasks |
| Dictionaries | Each task and the statistics result |
| If / else | Status filtering and validation |
| For loops | Finding a task to update |
| List comprehensions | Counting and filtering tasks |
| JSON | Reading and writing saved task data |

## API routes

| Method | Route | Purpose |
|---|---|---|
| GET | `/api/tasks` | Get tasks and statistics |
| GET | `/api/tasks?status=pending` | Get pending tasks |
| GET | `/api/tasks?status=completed` | Get completed tasks |
| POST | `/api/tasks` | Add a task |
| PATCH | `/api/tasks/<task_id>` | Change completed status |
| DELETE | `/api/tasks/<task_id>` | Delete a task |

This is a local learning project. Flask debug mode is enabled for development; turn it off before deploying the app publicly.
