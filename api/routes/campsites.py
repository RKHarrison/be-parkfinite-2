from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Annotated
from database.database_utils.get_db import get_db
from api.utils.security.authentication_utils import get_current_user
from api.schemas.campsite_schemas import CampsiteDetailed, CampsiteCreateRequest, Campsite
from api.schemas.review_schemas import ReviewCreateRequest, Review, ReviewUpdateRequest
from api.crud.campsite_crud import create_campsite, read_campsites, read_campsite_by_id
from api.crud.reviews_crud import create_review_by_campsite_id, read_reviews_by_campsite_id, update_review_by_review_id, remove_review_by_review_id


router = APIRouter(
    prefix='/campsites',
    tags=['campsites']
)

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Depends(get_current_user)

# router.include_router(reviews_route.router)

@router.post("/", status_code=201, response_model=CampsiteDetailed)
def post_campsite(request: CampsiteCreateRequest, db: db_dependency, user=user_dependency):
    return create_campsite(db=db, request=request)


@router.get("/", response_model=list[Campsite])
def get_campsites(skip: int = 0, limit: int = 250, db: Session = Depends(get_db)):
    return read_campsites(db, skip=skip, limit=limit)

@router.get("/{campsite_id}", response_model=CampsiteDetailed)
def get_campsite_by_campsite_id(campsite_id, db: Session = Depends(get_db), user=user_dependency):
    return read_campsite_by_id(db, campsite_id)

@router.post("/{campsite_id}/reviews", status_code=201, response_model=Review)
def post_review_by_campsite_id(campsite_id, request: ReviewCreateRequest, db: Session = Depends(get_db), user=user_dependency):
    return create_review_by_campsite_id(db=db, campsite_id=campsite_id, request=request)


@router.get("/{campsite_id}/reviews", response_model=list[Review])
def get_reviews_by_campsite_id(campsite_id, db: Session = Depends(get_db), user=user_dependency):
    return read_reviews_by_campsite_id(db, campsite_id)


@router.patch("/{campsite_id}/reviews/{review_id}", status_code=200, response_model=Review)
def patch_review_by_review_id(campsite_id, review_id, request: ReviewUpdateRequest, db: Session = Depends(get_db), user=user_dependency):
    return update_review_by_review_id(db=db, request=request, campsite_id=campsite_id, review_id=review_id)
