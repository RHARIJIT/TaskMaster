from fastapi import HTTPException, status, Request
from src.user.dtos import UserSchema, LoginSchema
from sqlalchemy.orm import Session
from src.user.models import UserModel
from pwdlib import PasswordHash
from src.utils.settings import settings
from datetime import datetime, timedelta, timezone
import jwt
from jwt import InvalidTokenError

# creating hasheed password
password_hash = PasswordHash.recommended()


def get_password_hash(password):
    return password_hash.hash(password)


def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)


def register(body: UserSchema, db: Session):
    print(body)
    is_user = db.query(UserModel).filter(UserModel.username == body.username).first()
    if is_user:
        raise HTTPException(400, detail="Username already exist..")

    is_email = db.query(UserModel).filter(UserModel.email == body.email).first()
    if is_email:
        raise HTTPException(400, detail="Email already exists...")

    hash_password = get_password_hash(body.password)

    new_user = UserModel(
        name=body.name,
        username=body.username,
        hash_password=hash_password,
        email=body.email,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def login_user(body: LoginSchema, db: Session):
    print(body)
    user = db.query(UserModel).filter(UserModel.username == body.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You have entered wrong username",
        )

    if not verify_password(body.password, user.hash_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You have entered wrong password",
        )

    exp_time = datetime.now() + timedelta(minutes=settings.EXP_TIME)
    # experimentation
    # exp_time = datetime.now(timezone.utc) + timedelta(seconds=30)

    token = jwt.encode(
        {"_id": user.id, "exp": exp_time}, settings.SECRET_KEY, settings.ALGORITHM
    )

    return {"token": token}


# Token Sent--
# def is_authenticated(request: Request, db: Session):
#     try:
#         token = request.headers.get("authorization")

#         if not token:
#             raise HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED, detail="You are unauthorized"
#             )
#         token = token.split(" ")[-1]

#         # to verify the token we need to decode it using the same secret key and the algorithm
#         data = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)

#         # print("DECODED DATA:", data)
#         # print("CURRENT TIME:", datetime.now().timestamp())

#         user_id = data.get("_id")

#         # verifying if an user exists holding the user_id
#         user = db.query(UserModel).filter(UserModel.id == user_id).first()
#         if not user:
#             raise HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED, detail="You are unauthorized"
#             )
#         return user

#     except InvalidTokenError:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED, detail="You are unauthorized"
#         )
