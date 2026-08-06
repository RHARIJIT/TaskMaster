from fastapi import APIRouter, Depends, status
from src.tasks import controller
from src.tasks.dtos import TaskSchema, TaskResponseSchema
from src.utils.db import get_db
from typing import List
from sqlalchemy.orm import Session

task_routes = APIRouter(prefix="/tasks")


@task_routes.post(
    "/create", response_model=TaskResponseSchema, status_code=status.HTTP_201_CREATED
)
def create_task(body: TaskSchema, db: Session = Depends(get_db)):
    return controller.create_task(body, db)


@task_routes.get(
    "/all_tasks",
    response_model=List[TaskResponseSchema],
    status_code=status.HTTP_200_OK,
)
def get_all_tasks(db: Session = Depends(get_db)):
    return controller.get_tasks(db)


@task_routes.get(
    "/one_task/{task_id}",
    response_model=TaskResponseSchema,
    status_code=status.HTTP_200_OK,
)
def get_get_task(task_id: int, db: Session = Depends(get_db)):
    return controller.get_one_task(task_id, db)


@task_routes.put(
    "/update_task/{task_id}",
    response_model=TaskResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
def update_task(body: TaskSchema, task_id: int, db: Session = Depends(get_db)):
    return controller.update_task(body, task_id, db)


@task_routes.delete(
    "/delete_task/{task_id}",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    return controller.delete_task(task_id, db)
