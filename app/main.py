from fastapi import FastAPI, HTTPException

from app.models import Task, TaskCreate
from app.storage import load_tasks, save_tasks

app = FastAPI(title="Study Tasks API")


@app.get("/")
def read_root():
    return {"message": "Study Tasks API is running"}


@app.get("/tasks", response_model=list[Task])
def get_tasks():
    return load_tasks()


@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int):
    tasks = load_tasks()
    for task in tasks:
        if task.id == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")


@app.post("/tasks", response_model=Task, status_code=201)
def create_task(task: TaskCreate):
    tasks = load_tasks()
    next_id = max([item.id for item in tasks], default=0) + 1
    new_task = Task(id=next_id, title=task.title)
    tasks.append(new_task)
    save_tasks(tasks)
    return new_task
