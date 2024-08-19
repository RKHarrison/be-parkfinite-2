from fastapi import HTTPException
from api.models.user_models import User
from api.schemas.user_schemas import CreateUserRequest
import bcrypt


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


def hash_password(password):
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password=pwd_bytes, salt=salt)
    return hashed_password


def verify_password(plain_password, hashed_password):
    password_byte_enc = plain_password.encode('utf-8')
    return bcrypt.checkpw(password=password_byte_enc, hashed_password=hashed_password)
