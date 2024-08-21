from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Annotated
from database.database_utils.get_db import get_db
from api.utils.security.authentication_utils import get_current_user
from api.schemas.campsite_schemas import CampsiteDetailed, CampsiteCreateRequest, Campsite
from api.crud.campsite_crud import create_campsite, read_campsites, read_campsite_by_id
from api.routes.reviews import router as reviews_route

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Depends(get_current_user)

router = APIRouter(
    prefix='/campsites',
    tags=['campsites']
)

router.include_router(reviews_route, prefix='/{campsite_id}/reviews')


@router.post("/", status_code=201, response_model=CampsiteDetailed)
def post_campsite(request: CampsiteCreateRequest, db: db_dependency, user=user_dependency):
    return create_campsite(db=db, request=request)


@router.get("/", response_model=list[Campsite])
def get_campsites(skip: int = 0, limit: int = 250, db: Session = Depends(get_db)):
    return read_campsites(db, skip=skip, limit=limit)


@router.get("/{campsite_id}", response_model=CampsiteDetailed)
def get_campsite_by_campsite_id(campsite_id, db: Session = Depends(get_db), user=user_dependency):
    return read_campsite_by_id(db, campsite_id)
