import json
from pathlib import Path

from app.models import Task

DATA_FILE = Path("data/tasks.json")


def load_tasks() -> list[Task]:
    if not DATA_FILE.exists():
        return []

    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            raw_tasks = json.load(file)
    except json.JSONDecodeError:
        return []

    return [Task(**task) for task in raw_tasks]


def find_task_index(tasks: list[Task], task_id: int) -> int | None:
    for index, task in enumerate(tasks):
        if task.id == task_id:
            return index
    return None


def save_tasks(tasks: list[Task]) -> None:
    DATA_FILE.parent.mkdir(exist_ok=True)
    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump([task.model_dump() for task in tasks], file, ensure_ascii=False, indent=2)
