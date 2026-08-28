from fastapi import FastAPI
from src.utils.db import Base,engine
from src.tasks.models import TaskModel
from src.user.router import user_routes
from src.tasks.router import task_routes

Base.metadata.create_all(engine)

app=FastAPI(title="This is the TaskMaster project")

# importing the task endpoints
app.include_router(task_routes)

# importing the user endpoints
app.include_router(user_routes)