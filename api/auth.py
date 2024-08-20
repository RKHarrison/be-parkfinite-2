from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from jose import jwt, JWTError

from api.config.config import SECRET_KEY, ALGORITHM
from database.database_utils.get_db import get_db

from starlette import status

from api.models.user_models import User
from api.schemas.user_schemas import CreateUserRequest
from api.schemas.authentication_schemas import Token

from api.crud.auth_crud import create_user, create_access_token_on_login

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


router = APIRouter(
    prefix='/auth',
    tags=['auth']
)


oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')


db_dependency = Annotated[Session, Depends(get_db)]


@router.post("/", status_code=status.HTTP_201_CREATED)
def post_user(db: db_dependency, create_user_request: CreateUserRequest):
    user = create_user(db=db, request=create_user_request)
    return {"message": "User created successfully, please log in to continue."}


@router.post("/token", response_model=Token)
def login_for_access_token(db: db_dependency, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    return create_access_token_on_login(db=db, form_data=form_data)


def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        if not username or not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user.')
        return {'username': username, 'id': user_id}
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user.')