from fastapi import HTTPException
from sqlalchemy.orm import joinedload
from api.models.campsite_models import Campsite, CampsitePhoto, CampsiteContact, CampsiteCategory
from api.models.review_models import Review
from api.models.user_models import User_Account, User_Credentials
from schemas.campsite_schemas import CampsiteCreateRequest, CampsiteDetailed
from utils.update_campsite_average_rating import update_campsite_average_rating


def create_campsite(db, request: CampsiteCreateRequest):
    category = db.query(CampsiteCategory).filter(
        CampsiteCategory.category_id == request.category_id).first()
    if not category:
        raise HTTPException(
            status_code=422, detail="Category ID does not exist!")

    new_campsite = Campsite(
        user_account_id=request.user_account_id,
        campsite_name=request.campsite_name,
        campsite_longitude=request.campsite_longitude,
        campsite_latitude=request.campsite_latitude,
        parking_cost=request.parking_cost,
        facilities_cost=request.facilities_cost,
        category_id=request.category_id,
        opening_month=request.opening_month,
        closing_month=request.closing_month
    )
    db.add(new_campsite)
    db.commit()
    db.refresh(new_campsite)

    for photo_request in request.photos:
        new_photo = CampsitePhoto(
            campsite_photo_url=photo_request.campsite_photo_url,
            campsite_id=new_campsite.campsite_id
        )
        db.add(new_photo)
    db.commit()

    for contact_request in request.contacts:
        new_contact = CampsiteContact(
            campsite_contact_name=contact_request.campsite_contact_name,
            campsite_contact_phone=contact_request.campsite_contact_phone,
            campsite_contact_email=contact_request.campsite_contact_email,
            campsite_id=new_campsite.campsite_id
        )
        db.add(new_contact)
    db.commit()

    username = db.query(User_Credentials.username).join(
        User_Account, User_Account.user_id == User_Credentials.user_id
    ).filter(
        User_Account.user_account_id == new_campsite.user_account_id
    ).first()

    if not username:
        raise HTTPException(
            status_code=404, detail="Username not found for this campsite."
        )

    db.refresh(new_campsite)

    campsite_data = CampsiteDetailed.model_validate({
        "campsite_name": new_campsite.campsite_name,
        "campsite_longitude": new_campsite.campsite_longitude,
        "campsite_latitude": new_campsite.campsite_latitude,
        "user_account_id": new_campsite.user_account_id,
        "photos": new_campsite.photos,
        "contacts": new_campsite.contacts,
        "campsite_id": new_campsite.campsite_id,
        "category": {
            "category_id": category.category_id,
            "category_name": category.category_name,
            "category_img_url": category.category_img_url
        },
        "date_added": new_campsite.date_added,
        "parking_cost": new_campsite.parking_cost,
        "facilities_cost": new_campsite.facilities_cost,
        "opening_month": new_campsite.opening_month,
        "closing_month": new_campsite.closing_month,
        "approved": False,
        "username": username[0]
    })

    return campsite_data





def read_campsites(db, skip: int = 0, limit: int = 250):
    campsites = db.query(Campsite).limit(limit).all()
    for campsite in campsites:
        update_campsite_average_rating(
            db, campsite.campsite_id, Campsite, Review)

    return campsites

def read_campsite_by_id(db, id: int):
    result = db.query(Campsite, User_Credentials.username
    ).join(
        User_Account, User_Account.user_account_id == Campsite.user_account_id
    ).join(
        User_Credentials, User_Credentials.user_id == User_Account.user_id
    ).options(
        joinedload(Campsite.photos),
        joinedload(Campsite.contacts),
        joinedload(Campsite.category)
    ).filter(
        Campsite.campsite_id == id
    ).first()

    if not result:
        raise HTTPException(status_code=404, detail="404 - Campsite Not Found!")

    campsite, username = result
    campsite_dict = campsite.__dict__.copy()
    campsite_dict['username'] = username
    campsite_data = CampsiteDetailed.model_validate(campsite_dict)

    return campsite_data
