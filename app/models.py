from pydantic import BaseModel, Field


class Task(BaseModel):
    id: int
    title: str
    done: bool = False


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=120)
