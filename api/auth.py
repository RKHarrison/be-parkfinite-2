from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from starlette import status

from database.database import SessionLocal
from api.models.user_models import User
from api.schemas.user_schemas import CreateUserRequest

from fastapi.security import OAuth2PasswordBearer
import bcrypt

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

SECRET_KEY = 'cb886136c58b553b1dac8455cc10add008b390fdb936c807a29e65fb434322be'
ALGORITHM = 'HS256'

oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(db: db_dependency, create_user_request: CreateUserRequest):
    create_user_model = User(
        username=create_user_request.username,
        hashed_password=hash_password(create_user_request.password)
    )

    db.add(create_user_model)
    db.commit()


def hash_password(password):
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password=pwd_bytes, salt=salt)
    return hashed_password

def verify_password(plain_password, hashed_password):
    password_byte_enc = plain_password.encode('utf-8')
    return bcrypt.checkpw(password = password_byte_enc , hashed_password = hashed_password)