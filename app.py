from flask import Flask, render_template, request, jsonify
import json
import os
from uuid import uuid4

app = Flask(__name__)
DATA_FILE = os.path.join(os.path.dirname(__file__), "tasks.json")


def load_tasks():
    """Load tasks from the JSON file. Return an empty list if it doesn't exist."""
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        return []


def save_tasks(tasks):
    """Save the complete task list to the JSON file."""
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(tasks, file, indent=4)


def calculate_statistics(tasks):
    """Calculate dashboard totals using loops and list comprehensions."""
    total = len(tasks)
    completed = len([task for task in tasks if task["completed"]])
    pending = len([task for task in tasks if not task["completed"]])
    high_priority = len([task for task in tasks if task["priority"] == "High" and not task["completed"]])

    return {
        "total": total,
        "pending": pending,
        "completed": completed,
        "high_priority": high_priority
    }


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/tasks", methods=["GET"])
def get_tasks():
    """Return tasks, optionally filtered by status."""
    tasks = load_tasks()
    status = request.args.get("status", "all")

    if status == "pending":
        filtered_tasks = [task for task in tasks if not task["completed"]]
    elif status == "completed":
        filtered_tasks = [task for task in tasks if task["completed"]]
    else:
        filtered_tasks = tasks

    return jsonify({
        "tasks": filtered_tasks,
        "statistics": calculate_statistics(tasks)
    })


@app.route("/api/tasks", methods=["POST"])
def add_task():
    data = request.get_json(silent=True) or {}
    title = data.get("title", "").strip()
    subject = data.get("subject", "").strip()
    priority = data.get("priority", "Medium")

    if not title or not subject:
        return jsonify({"error": "Please enter both a task title and subject."}), 400

    if priority not in ["Low", "Medium", "High"]:
        priority = "Medium"

    tasks = load_tasks()
    new_task = {
        "id": str(uuid4()),
        "title": title,
        "subject": subject,
        "priority": priority,
        "completed": False
    }
    tasks.append(new_task)
    save_tasks(tasks)

    return jsonify({
        "message": "Task added successfully.",
        "task": new_task,
        "statistics": calculate_statistics(tasks)
    }), 201


@app.route("/api/tasks/<task_id>", methods=["PATCH"])
def update_task(task_id):
    data = request.get_json(silent=True) or {}
    tasks = load_tasks()

    for task in tasks:
        if task["id"] == task_id:
            task["completed"] = bool(data.get("completed", task["completed"]))
            save_tasks(tasks)
            return jsonify({
                "message": "Task status updated.",
                "task": task,
                "statistics": calculate_statistics(tasks)
            })

    return jsonify({"error": "Task not found."}), 404


@app.route("/api/tasks/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    tasks = load_tasks()
    updated_tasks = [task for task in tasks if task["id"] != task_id]

    if len(updated_tasks) == len(tasks):
        return jsonify({"error": "Task not found."}), 404

    save_tasks(updated_tasks)
    return jsonify({
        "message": "Task deleted successfully.",
        "statistics": calculate_statistics(updated_tasks)
    })


if __name__ == "__main__":
    # debug=True is useful while learning; turn it off before public deployment.
    app.run(debug=True)
