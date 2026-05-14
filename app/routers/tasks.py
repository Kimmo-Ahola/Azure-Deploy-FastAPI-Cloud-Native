from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app import schemas, model

router = APIRouter(prefix="/tasks", tags=["tasks"])


class TaskNotFound(HTTPException):
    openapi: dict[int | str, dict[str, Any]] = {
        404: {"description": "Task not found", "model": schemas.ErrorResponse}
    }

    def __init__(self, task_id: int):
        super().__init__(status_code=404, detail=f"Task {task_id} not found")


@router.post("", response_model=schemas.TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(payload: schemas.TaskCreate, db: Session = Depends(get_db)):
    """
    Create a new task.
    # Header 1
    ## Header 2
    ### Header 3
    ###### Header 6
    *kursiv text*
    **fet text**
    The `title` is required. `description` and `done` are optional.
    """
    task = model.Task(**payload.model_dump())
    db.add(task)
    db.commit()
    db.refresh(task, attribute_names=["category"])
    return task


# get one
@router.get(
    "/{task_id}",
    response_model=schemas.TaskRead,
    responses=TaskNotFound.openapi,
)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.get(model.Task, task_id)
    if task is None:
        raise TaskNotFound(task_id)
    return task


# get all/many
@router.get("", response_model=list[schemas.TaskRead])
def list_tasks(db: Session = Depends(get_db), skip: int = 0, limit: int = 50):
    return db.query(model.Task).offset(skip).limit(limit).all()


@router.patch(
    "/{task_id}", response_model=schemas.TaskRead, responses=TaskNotFound.openapi
)
def update_task(
    task_id: int, payload: schemas.TaskUpdate, db: Session = Depends(get_db)
):
    task = db.get(model.Task, task_id)
    if task is None:
        raise TaskNotFound(task_id)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(task, field, value)
    db.commit()
    db.refresh(task, attribute_names=["category"])
    return task


@router.delete(
    "/{task_id}", status_code=status.HTTP_204_NO_CONTENT, responses=TaskNotFound.openapi
)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.get(model.Task, task_id)
    if task is None:
        raise TaskNotFound(task_id)
    db.delete(task)
    db.commit()


# ---------- Categories ----------
# Note: living under /tasks/categories as a teaching shortcut.
# In a real codebase these would have their own router.

cat_router = APIRouter(prefix="/categories", tags=["categories"])


@cat_router.post("", response_model=schemas.CategoryRead, status_code=201)
def create_category(payload: schemas.CategoryCreate, db: Session = Depends(get_db)):
    category = model.Category(**payload.model_dump())
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


@cat_router.get("", response_model=list[schemas.CategoryRead])
def list_categories(db: Session = Depends(get_db)):
    return db.query(model.Category).all()
