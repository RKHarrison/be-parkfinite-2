from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from database.database_utils.get_db import get_db

from starlette import status
from datetime import timedelta, datetime, timezone

from api.models.user_models import User
from api.schemas.user_schemas import CreateUserRequest
from api.schemas.authentication_schemas import Token

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt
import bcrypt

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

SECRET_KEY = 'cb886136c58b553b1dac8455cc10add008b390fdb936c807a29e65fb434322be'
ALGORITHM = 'HS256'

oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')


db_dependency = Annotated[Session, Depends(get_db)]


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(db: db_dependency, create_user_request: CreateUserRequest):
    create_user_model = User(
        username=create_user_request.username,
        hashed_password=hash_password(create_user_request.password)
    )

    try:
        db.add(create_user_model)
        db.commit()
        db.refresh(create_user_model)
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=409, detail="Username already exists.")


def hash_password(password):
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password=pwd_bytes, salt=salt)
    return hashed_password

def verify_password(plain_password, hashed_password):
    password_byte_enc = plain_password.encode('utf-8')
    return bcrypt.checkpw(password=password_byte_enc, hashed_password=hashed_password)