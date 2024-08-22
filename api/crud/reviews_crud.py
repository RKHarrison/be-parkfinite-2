from fastapi import HTTPException
from api.models.review_models import Review
from api.models.campsite_models import Campsite
from api.models.user_models import User_Account, User_Credentials
from api.schemas.review_schemas import ReviewPostRequest, ReviewPatchRequest
from api.utils.update_campsite_average_rating import update_campsite_average_rating


def create_review_by_campsite_id(db, campsite_id: int, request: ReviewPostRequest):
    campsite = db.query(Campsite).filter(
        Campsite.campsite_id == campsite_id).first()
    if not campsite:
        raise HTTPException(
            status_code=404, detail="404 - Campsite Not Found!")

    user = db.query(User_Account).filter(User_Account.user_account_id == request.user_account_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="404 - User Not Found!")

    new_review = Review(
        campsite_id=campsite_id,
        rating=request.rating,
        comment=request.comment,
        user_account_id=request.user_account_id
    )
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    update_campsite_average_rating(db, campsite_id, Campsite, Review)
    
    return new_review


def read_reviews_by_campsite_id(db, id: int):
    reviews = db.query(
        Review,
        User_Credentials.username
    ).join(
        User_Account, User_Account.user_account_id == Review.user_account_id
    ).join(
        User_Credentials, User_Credentials.user_id == User_Account.user_id
    ).filter(
        Review.campsite_id == id
    ).all()
    
    reviews_with_username = []
    for review, username in reviews:
        review_data = review.__dict__
        review_data.update({'username': username})
        review_data.pop('_sa_instance_state', None)
        reviews_with_username.append(review_data)

    return reviews_with_username

def update_review_by_review_id(db, campsite_id: int, review_id: int, request: ReviewPatchRequest):
    review = db.get(Review, review_id)
    if not review:
        raise HTTPException(
            status_code=404, detail="404 - Review Not Found!")

    campsite = db.get(Campsite, campsite_id)
    if not campsite:
        raise HTTPException(
            status_code=404, detail="404 - Campsite Not Found!")

    if request.rating:
        review.rating = request.rating
        update_campsite_average_rating(db, campsite_id, Campsite, Review)
        db.commit()
    if request.comment:
        review.comment = request.comment
        db.commit()
    db.refresh(review)
    return review


def remove_review_by_review_id(db, review_id: int):
    review = db.get(Review, review_id)
    if not review:
        raise HTTPException(
            status_code=404, detail="404 - Review Not Found!")
    db.delete(review)
    db.commit()
