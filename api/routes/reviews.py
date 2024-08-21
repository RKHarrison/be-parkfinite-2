from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Annotated
from database.database_utils.get_db import get_db
from api.utils.security.authentication_utils import get_current_user
from api.schemas.review_schemas import ReviewCreateRequest, Review, ReviewUpdateRequest
from api.crud.reviews_crud import create_review_by_campsite_id, read_reviews_by_campsite_id, update_review_by_review_id, remove_review_by_review_id

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Depends(get_current_user)

router = APIRouter(
    prefix='/{campsite_id}/reviews',
    tags=['reviews'],
    dependencies=[user_dependency]
)



@router.post("/", status_code=201, response_model=Review)
def post_review_by_campsite_id(campsite_id, request: ReviewCreateRequest, db: Session = Depends(get_db), user=user_dependency):
    return create_review_by_campsite_id(db=db, campsite_id=campsite_id, request=request)


@router.get("/", response_model=list[Review])
def get_reviews_by_campsite_id(campsite_id, db: Session = Depends(get_db), user=user_dependency):
    return read_reviews_by_campsite_id(db, campsite_id)


@router.patch("/{review_id}", status_code=200, response_model=Review)
def patch_review_by_review_id(campsite_id, review_id, request: ReviewUpdateRequest, db: Session = Depends(get_db), user=user_dependency):
    return update_review_by_review_id(db=db, request=request, campsite_id=campsite_id, review_id=review_id)


@router.delete("/{review_id}", status_code=204)
def delete_review_by_review_id(review_id, db: Session = Depends(get_db)):
    return remove_review_by_review_id(db=db, review_id=review_id)

