import sys
import json
import os
from datetime import datetime


# Task management functions


def load_tasks():
    if os.path.exists("tasks.json"):
        with open("tasks.json", "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                # Return an empty list if the file is empty or contains invalid JSON
                return []
    # Return an empty list if the file doesn't exist
    return []


def save_tasks(tasks):
    with open("tasks.json", "w") as f:
        json.dump(tasks, f, indent=4)


def add_tasks(description):
    tasks = load_tasks()
    task_id = len(tasks) + 1
    task = {
        "id": task_id,
        "description": description,
        "status": "todo",
        "createdAt": datetime.now().isoformat(),
        "updatedAt": datetime.now().isoformat(),
    }
    tasks.append(task)
    save_tasks(tasks)
    print(f"Task added successfully (ID: {task_id})")


def update_task(task_id, new_description):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["description"] = new_description
            task["updatedAt"] = datetime.now().isoformat()
            save_tasks(tasks)
            print(f"Task {task_id} updated successfully")
            return
    print(f"Task {task_id} not found")


def delete_task(task_id):
    tasks = load_tasks()
    filter_tasks = [task for task in tasks if task["id"] != task_id]

    if len(filter_tasks) == len(tasks):
        print(f"Task with ID {task_id} not found")
    else:
        save_tasks(tasks)
        print(f"Task {task_id} deleted successfully")


def mark_in_progress(task_id):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["status"] = "in-progress"
            task["updatedAt"] = datetime.now().isoformat()
            save_tasks(tasks)
            print(f"Task {task_id} updated successfully")
            return
    print(f"Task {task_id} not found")


def mark_done(task_id):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["status"] = "done"
            task["updatedAt"] = datetime.now().isoformat()
            save_tasks(tasks)
            print(f"Task {task_id} updated successfully")
            return
    print(f"Task {task_id} not found")


def list_tasks(status=None):
    tasks = load_tasks()
    filtered_tasks = tasks
    if status:
        filtered_tasks = [task for task in tasks if task["status"] == status]
    for task in filtered_tasks:
        print(
            f"ID: {task['id']}, Description: {task['description']}, Status: {task['status']}, "
            f"Created At: {task['createdAt']}, Updated At: {task['updatedAt']}"
        )


# Command-line interface handler


def handle_command():
    if len(sys.argv) < 2:
        print("Usage: task-cli <command> [options]")
        return

    command = sys.argv[1]

    if command == "add":
        add_tasks(" ".join(sys.argv[2:]))
    elif command == "update" and len(sys.argv) > 3:
        try:
            task_id = int(sys.argv[2])
            update_task(task_id, " ".join(sys.argv[3:]))
        except ValueError:
            print("Invalid task ID")
    elif command == "delete" and len(sys.argv) > 2:
        try:
            task_id = int(sys.argv[2])
            delete_task(task_id)
        except ValueError:
            print("Invalid task ID")
    elif command == "mark-in-progress" and len(sys.argv) > 2:
        try:
            task_id = int(sys.argv[2])
            mark_in_progress(task_id)
        except ValueError:
            print("Invalid task ID")
    elif command == "mark-done" and len(sys.argv) > 2:
        try:
            task_id = int(sys.argv[2])
            mark_done(task_id)
        except ValueError:
            print("Invalid task ID")
    elif command == "list":
        if len(sys.argv) > 2:
            list_tasks(sys.argv[2])
        else:
            list_tasks()
    else:
        print("Invalid command or arguments")


if __name__ == "__main__":
    handle_command()
