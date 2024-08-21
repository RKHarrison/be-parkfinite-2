import uvicorn
from os import getenv
from fastapi import FastAPI, Depends, HTTPException
from fastapi.exceptions import RequestValidationError, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from starlette import status
from database.database import engine, Base
from database.database_utils.get_db import get_db
from api.crud.reviews_crud import remove_review_by_review_id
from api.crud.user_crud import read_users, read_user_by_username, update_user_xp, create_user_favourite_campsite, read_user_campsite_favourites_by_username, remove_user_favourite_campsite
from api.schemas.campsite_schemas import Campsite

from api.schemas.user_schemas import User
from api.errors.error_handling import (
    validation_exception_handler, attribute_error_handler,  http_exception_handler, sqlalchemy_exception_handler)
from api.utils.security.authentication_utils import get_current_user

import api.routes.auth as auth_route
import api.routes.campsites as campsites_route

Base.metadata.create_all(bind=engine)

user_dependency = Depends(get_current_user)
app = FastAPI()

app.include_router(auth_route.router)
app.include_router(campsites_route.router)


app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(AttributeError, attribute_error_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)


@app.get("/", status_code=status.HTTP_200_OK)
def health_check():
    return {"Server": "Healthy and happy!"}


@app.delete("/reviews/{review_id}", status_code=204)
def delete_review_by_review_id(review_id, db: Session = Depends(get_db), user=user_dependency):
    return remove_review_by_review_id(db=db, review_id=review_id)


@app.get("/users", response_model=list[User])
def get_users(db: Session = Depends(get_db), user=user_dependency):
    return read_users(db)


@app.get("/users/{username}", response_model=User)
def get_user_by_id(username, db: Session = Depends(get_db), user=user_dependency):
    return read_user_by_username(db, username)


@app.patch("/users/{username}/{xp}", response_model=User)
def patch_user_xp(username: str, xp: str, db: Session = Depends(get_db), user=user_dependency):
    return update_user_xp(db=db, username=username, xp=xp)


@app.get("/users/{username}/favourites", response_model=list[Campsite])
def get_user_favourite_campsites(username, db: Session = Depends(get_db), user=user_dependency):
    favourites = read_user_campsite_favourites_by_username(db, username)
    print(favourites)
    return favourites


@app.post("/users/{username}/favourites/{campsite_id}", status_code=201)
def post_user_favourite_campsite(username, campsite_id, db: Session = Depends(get_db), user=user_dependency):
    return create_user_favourite_campsite(db=db, username=username, campsite_id=campsite_id)


@app.delete("/users/{username}/favourites/{campsite_id}", status_code=204)
def delete_user_favourite_campsite(username, campsite_id, db: Session = Depends(get_db), user=user_dependency):
    return remove_user_favourite_campsite(db=db, username=username, campsite_id=campsite_id, )


if __name__ == "__main__":
    PORT = int(getenv('PORT', 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=PORT, reload=True)
