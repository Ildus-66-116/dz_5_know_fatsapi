import uvicorn
from fastapi import FastAPI, HTTPException
from typing import List
from models import Task, TaskCreate, TaskUpdate

app = FastAPI()
tasks_db = []


@app.get("/tasks", response_model=List[Task])
def get_tasks():
    return tasks_db


@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int):
    task = next((t for t in tasks_db if t.id == task_id), None)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.post("/tasks", response_model=Task)
def create_task(task: TaskCreate):
    task_id = len(tasks_db)
    new_task = Task(
        id=task_id, title=task.title, description=task.description, completed=False
    )
    tasks_db.append(new_task)
    return new_task


@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task: TaskUpdate):
    task_to_update = next((t for t in tasks_db if t.id == task_id), None)
    if task_to_update is None:
        raise HTTPException(status_code=404, detail="Task not found")
    task_to_update.title = task.title
    task_to_update.description = task.description
    task_to_update.completed = task.completed
    return task_to_update


@app.delete("/tasks/{task_id}", response_model=Task)
def delete_task(task_id: int):
    global tasks_db
    task_to_delete = next((t for t in tasks_db if t.id == task_id), None)
    if task_to_delete is None:
        raise HTTPException(status_code=404, detail="Task not found")
    tasks_db.remove(task_to_delete)
    return task_to_delete


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
