from fastapi import HTTPException
from api.models.user_models import User_Account, user_campsite_favourites
from api.models.campsite_models import Campsite

# DISABLED PENDING AMDMINISTRATION LEVEL RESTRICTION
# def read_users(db):
#     users = db.query(User_Account).all()
#     return users


def read_user_account_by_user_id(db, user_id):
    user_account = db.query(User_Account).filter(
        User_Account.user_id == user_id).first()
    if not user_account:
        raise HTTPException(
            status_code=404, detail="404 - User Account Not Found!")
    return user_account


def update_user_xp(db, user_id, xp):
    user_account = db.query(User_Account).filter(
        User_Account.user_id == user_id).first()
    if not user_account:
        raise HTTPException(
            status_code=404, detail="404 - User Account Not Found!")

    try:
        if xp.startswith('-'):
            xp_value = -int(xp[1:])
        else:
            xp_value = int(xp)
    except ValueError:
        raise HTTPException(status_code=400, detail="400 - Invalid XP Value")

    user_account.xp += xp_value
    db.commit()
    db.refresh(user_account)
    return user_account


def create_user_favourite_campsite(db, user_id, campsite_id):
    user = db.query(User_Account).filter(
        User_Account.user_id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=404, detail="404 - User Account Not Found!")

    campsite = db.get(Campsite, campsite_id)
    if not campsite:
        raise HTTPException(
            status_code=404, detail="404 - Campsite Not Found!")
    if campsite_id not in user.favourites:
        user.favourites.append(campsite)
        db.commit()
    return


def read_user_campsite_favourites_by_user_id(db, user_id: str):
    user_account = db.query(User_Account).filter(
        User_Account.user_id == user_id).first()
    if not user_account:
        raise HTTPException(
            status_code=404, detail="404 - User Account Not Found!")
    return user_account.favourites


def remove_user_favourite_campsite(db, user_id, campsite_id):
    user_account = db.query(User_Account).filter(
        User_Account.user_id == user_id).first()
    if not user_account:
        raise HTTPException(
            status_code=404, detail="404 - User Account Not Found!")

    campsite = db.get(Campsite, campsite_id)
    if not campsite:
        raise HTTPException(
            status_code=404, detail="404 - Campsite Not Found!")

    if campsite in user_account.favourites:
        user_account.favourites.remove(campsite)
        db.commit()
        return {"message": f"Campsite {campsite.campsite_id} removed from favourites."}
    else:
        raise HTTPException(
            status_code=404, detail="404 - Campsite Not Found In User's Favourites!")
