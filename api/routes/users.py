from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Annotated
from database.database_utils.get_db import get_db
from api.utils.security.authentication_utils import get_current_user
from api.crud.user_crud import read_users, read_user_by_username, update_user_xp, create_user_favourite_campsite, read_user_campsite_favourites_by_username, remove_user_favourite_campsite
from api.schemas.campsite_schemas import Campsite
from api.schemas.user_schemas import UserAccountDetails

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Depends(get_current_user)

router = APIRouter(
    prefix='/users',
    tags=['users'],
    dependencies=[user_dependency]
)


@router.get("/", response_model=list[UserAccountDetails])
def get_users(db: Session = Depends(get_db), user=user_dependency):
    return read_users(db)


@router.get("/{username}", response_model=UserAccountDetails)
def get_user_by_id(username, db: Session = Depends(get_db), user=user_dependency):
    return read_user_by_username(db, username)


@router.patch("/{username}/{xp}", response_model=UserAccountDetails)
def patch_user_xp(username: str, xp: str, db: Session = Depends(get_db), user=user_dependency):
    return update_user_xp(db=db, username=username, xp=xp)


@router.get("/{username}/favourites", response_model=list[Campsite])
def get_user_favourite_campsites(username, db: Session = Depends(get_db), user=user_dependency):
    favourites = read_user_campsite_favourites_by_username(db, username)
    print(favourites)
    return favourites


@router.post("/{username}/favourites/{campsite_id}", status_code=201)
def post_user_favourite_campsite(username, campsite_id, db: Session = Depends(get_db), user=user_dependency):
    return create_user_favourite_campsite(db=db, username=username, campsite_id=campsite_id)


@router.delete("/{username}/favourites/{campsite_id}", status_code=204)
def delete_user_favourite_campsite(username, campsite_id, db: Session = Depends(get_db), user=user_dependency):
    return remove_user_favourite_campsite(db=db, username=username, campsite_id=campsite_id, )
