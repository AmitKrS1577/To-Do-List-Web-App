from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# In-memory data structure to store tasks
# Each task is represented as a dictionary with keys: id, title, and description
tasks = []

@app.route("/")
def index():
    """
    Homepage route.
    Displays the list of all tasks.
    """
    return render_template("index.html", tasks=tasks)

@app.route("/add", methods=["GET", "POST"])
def add_task():
    """
    Route to add a new task.
    Handles both GET and POST requests.
    - GET: Displays the form to add a new task.
    - POST: Processes the form data and adds the new task to the tasks list.
    """
    if request.method == "POST":
        # Get form data
        title = request.form["title"]
        description = request.form.get("description", "")
        if title:  # Only add if the title is provided
            tasks.append({"id": len(tasks) + 1, "title": title, "description": description})
        return redirect(url_for("index"))
    return render_template("add_task.html")

@app.route("/edit/<int:task_id>", methods=["GET", "POST"])
def edit_task(task_id):
    """
    Route to edit an existing task.
    Handles both GET and POST requests.
    - GET: Displays the form pre-filled with the task's current details.
    - POST: Updates the task's details in the tasks list.
    """
    # Find the task by ID
    task = next((t for t in tasks if t["id"] == task_id), None)
    if not task:
        return "Task not found", 404

    if request.method == "POST":
        # Update task details
        task["title"] = request.form["title"]
        task["description"] = request.form.get("description", "")
        return redirect(url_for("index"))
    return render_template("edit_task.html", task=task)

@app.route("/delete/<int:task_id>")
def delete_task(task_id):
    """
    Route to delete a task by its ID.
    Removes the task from the tasks list and redirects to the homepage.
    """
    global tasks
    # Keep only the tasks that do not match the given ID
    tasks = [t for t in tasks if t["id"] != task_id]
    return redirect(url_for("index"))

@app.route("/complete/<int:task_id>")
def mark_complete(task_id):
    task = next((t for t in tasks if t["id"] == task_id), None)
    if task:
        task["completed"] = True
    return redirect(url_for("index"))

if __name__ == "__main__":
    # Run the application in debug mode
    app.run(debug=True)
