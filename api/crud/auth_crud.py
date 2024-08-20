from fastapi import HTTPException
from datetime import timedelta, datetime, timezone
from starlette import status
from jose import jwt
from api.models.user_models import User
from api.schemas.user_schemas import CreateUserRequest
from api.utils.security_utils.password_utils import hash_password, verify_password


def create_user(db, request: CreateUserRequest):
    existing_user = db.query(User).filter(
        User.username == request.username).first()
    if existing_user:
        raise HTTPException(status_code=409, detail="Username already exists.")

    new_user = User(
        username=request.username,
        hashed_password=hash_password(request.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"username": new_user.username, "user_id": new_user.user_id}


SECRET_KEY = 'cb886136c58b553b1dac8455cc10add008b390fdb936c807a29e65fb434322be'
ALGORITHM = 'HS256'


def create_access_token_on_login(db, form_data):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Incorrect username or password. Please try again.')
    token = create_access_token(
        user.username, user.user_id, timedelta(minutes=20))

    return {'access_token': token, 'token_type': 'bearer'}


def authenticate_user(username: str, password: str, db):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    encode = {'sub': username, 'id': user_id}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
