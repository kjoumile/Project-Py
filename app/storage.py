import json
from pathlib import Path

from app.models import Task

DATA_FILE = Path("data/tasks.json")


def load_tasks() -> list[Task]:
    if not DATA_FILE.exists():
        return []

    with DATA_FILE.open("r", encoding="utf-8") as file:
        raw_tasks = json.load(file)

    return [Task(**task) for task in raw_tasks]


def save_tasks(tasks: list[Task]) -> None:
    DATA_FILE.parent.mkdir(exist_ok=True)
    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump([task.model_dump() for task in tasks], file, ensure_ascii=False, indent=2)
