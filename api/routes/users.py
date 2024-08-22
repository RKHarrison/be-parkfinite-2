from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Annotated
from database.database_utils.get_db import get_db
from api.utils.security.authentication_utils import get_current_user
from api.crud.user_crud import read_user_account_by_user_id, update_user_xp, create_user_favourite_campsite, read_user_campsite_favourites_by_user_id, remove_user_favourite_campsite
from api.schemas.campsite_schemas import Campsite
from api.schemas.user_schemas import UserAccountDetails

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Depends(get_current_user)

router = APIRouter(
    prefix='/users',
    tags=['users'],
    dependencies=[user_dependency]
)

# DISABLED PENDING AMDMINISTRATION LEVEL RESTRICTION
# @router.get("/", response_model=list[UserAccountDetails])
# def get_users(db: Session = Depends(get_db), user=user_dependency):
#     return read_users(db)


@router.get("/{user_id}", response_model=UserAccountDetails)
def get_user_by_id(user_id: str, db: Session = Depends(get_db), user=user_dependency):
    return read_user_account_by_user_id(db, user_id)


@router.patch("/{user_id}/{xp}", response_model=UserAccountDetails)
def patch_user_xp(user_id: str, xp: str, db: Session = Depends(get_db), user=user_dependency):
    return update_user_xp(db=db, user_id=user_id, xp=xp)


@router.get("/{user_id}/favourites", response_model=list[Campsite])
def get_user_favourite_campsites(user_id, db: Session = Depends(get_db), user=user_dependency):
    favourites = read_user_campsite_favourites_by_user_id(db, user_id=user_id)
    print(favourites)
    return favourites


@router.post("/{user_id}/favourites/{campsite_id}", status_code=201)
def post_user_favourite_campsite(user_id, campsite_id, db: Session = Depends(get_db), user=user_dependency):
    return create_user_favourite_campsite(db=db, user_id=user_id, campsite_id=campsite_id)


@router.delete("/{user_id}/favourites/{campsite_id}", status_code=204)
def delete_user_favourite_campsite(user_id, campsite_id, db: Session = Depends(get_db), user=user_dependency):
    return remove_user_favourite_campsite(db=db, user_id=user_id, campsite_id=campsite_id, )
