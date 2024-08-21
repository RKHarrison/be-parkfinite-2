from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Annotated
from database.database_utils.get_db import get_db
from api.utils.security.authentication_utils import get_current_user
from api.crud.reviews_crud import remove_review_by_review_id

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Depends(get_current_user)

router = APIRouter(
    prefix='/reviews',
    tags=['reviews'],
    dependencies=[user_dependency]
)


@router.delete("/{review_id}", status_code=204)
def delete_review_by_review_id(review_id, db: Session = Depends(get_db)):
    return remove_review_by_review_id(db=db, review_id=review_id)
