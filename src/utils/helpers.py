from fastapi import HTTPException, status, Request,Depends
from sqlalchemy.orm import Session
from src.user.models import UserModel
from src.utils.settings import settings
from src.utils.db import get_db
import jwt
from jwt import InvalidTokenError


# Token Sent--
def is_authenticated(request: Request, db: Session=Depends(get_db)):
    try:
        token = request.headers.get("authorization")

        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="You are unauthorized"
            )
        token = token.split(" ")[-1]

        # to verify the token we need to decode it using the same secret key and the algorithm
        data = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)

        user_id = data.get("_id")

        # verifying if an user exists holding the user_id
        user = db.query(UserModel).filter(UserModel.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="You are unauthorized"
            )
        return user

    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="You are unauthorized"
        )