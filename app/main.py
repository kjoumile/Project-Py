import logging
import time

from fastapi import FastAPI, HTTPException
from fastapi import Request

from app.models import Task, TaskCreate, TaskUpdate
from app.storage import find_task_index, load_tasks, save_tasks

app = FastAPI(title="Study Tasks API")
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("study_tasks")


@app.middleware("http")
async def log_requests(request: Request, call_next):
    started_at = time.perf_counter()
    response = await call_next(request)
    elapsed_ms = (time.perf_counter() - started_at) * 1000
    logger.info(
        "%s %s -> %s %.1fms",
        request.method,
        request.url.path,
        response.status_code,
        elapsed_ms,
    )
    return response


@app.get("/")
def read_root():
    return {"message": "Study Tasks API is running"}


@app.get("/tasks", response_model=list[Task])
def get_tasks():
    return load_tasks()


@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int):
    tasks = load_tasks()
    task_index = find_task_index(tasks, task_id)
    if task_index is not None:
        return tasks[task_index]
    raise HTTPException(status_code=404, detail="Task not found")


@app.post("/tasks", response_model=Task, status_code=201)
def create_task(task: TaskCreate):
    tasks = load_tasks()
    next_id = max([item.id for item in tasks], default=0) + 1
    new_task = Task(id=next_id, title=task.title)
    tasks.append(new_task)
    save_tasks(tasks)
    return new_task


@app.patch("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, update: TaskUpdate):
    tasks = load_tasks()
    task_index = find_task_index(tasks, task_id)
    if task_index is not None:
        updated_task = tasks[task_index].model_copy(update={"done": update.done})
        tasks[task_index] = updated_task
        save_tasks(tasks)
        return updated_task
    raise HTTPException(status_code=404, detail="Task not found")
