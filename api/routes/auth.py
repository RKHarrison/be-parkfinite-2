from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Annotated
from starlette import status

from database.database_utils.get_db import get_db
from api.schemas.user_schemas import CreateUserRequest
from api.schemas.authentication_schemas import Token
from api.crud.auth_crud import create_user, create_access_token_on_login

db_dependency = Annotated[Session, Depends(get_db)]

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')


@router.post("/", status_code=status.HTTP_201_CREATED)
def post_user(db: db_dependency, create_user_request: CreateUserRequest):
    user = create_user(db=db, request=create_user_request)
    return {"message": "User created successfully, please log in to continue."}


@router.post("/token", response_model=Token)
def login_for_access_token(db: db_dependency, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    return create_access_token_on_login(db=db, form_data=form_data)
