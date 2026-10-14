from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI(title="Todo API")

class Task(BaseModel):
    id: int
    title: str
    done: bool = False

tasks: List[Task] = []
@app.get("/health")
def health():
    return{"status": "ok"}

@app.get("/tasks", response_model=list[Task])
def get_tasks():
    return tasks

@app.post("/tasks", response_model=Task, status_code=201)
def create_task(task: Task):
    if any(t.id == task.id for t in tasks):
        raise HTTPException(status_code=400, detail="Task id already exists")
    tasks.append(task)
    return task

@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    global tasks
    if not any(t.id == task_id for t in tasks):
        raise HTTPException(status_code=404, detail="Task not found")
    tasks = [t for t in tasks if t.id != task_id]
    