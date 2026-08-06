from fastapi import APIRouter,Depends,status
from sqlalchemy.orm import Session
from src.user.dtos import UserSchema,UserResponseSchema
from src.utils.db import get_db
from src.user import controller

user_routes=APIRouter(prefix="/user")

@user_routes.post("/register",response_model=UserResponseSchema,status_code=status.HTTP_201_CREATED)
def register(body:UserSchema,db:Session=Depends(get_db)):
    return controller.register(body,db)