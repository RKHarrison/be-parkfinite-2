from fastapi import HTTPException
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
