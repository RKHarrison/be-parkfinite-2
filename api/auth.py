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

from api.crud.auth_crud import create_user

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt


router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

SECRET_KEY = 'cb886136c58b553b1dac8455cc10add008b390fdb936c807a29e65fb434322be'
ALGORITHM = 'HS256'

oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')


db_dependency = Annotated[Session, Depends(get_db)]


@router.post("/", status_code=status.HTTP_201_CREATED)
def post_user(db: db_dependency, create_user_request: CreateUserRequest):
    user = create_user(db=db, request=create_user_request)
    return {"message": "User created successfully, please log in to continue."}
