from fastapi import HTTPException
from api.models.user_models import User_Account, user_campsite_favourites
from api.models.campsite_models import Campsite

# DISABLED PENDING AMDMINISTRATION LEVEL RESTRICTION
# def read_users(db):
#     users = db.query(User_Account).all()
#     return users


def read_user_by_username(db, username):
    user = user = db.query(User_Account).filter(User_Account.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="404 - User Not Found!")
    return user


def update_user_xp(db, username, xp):
    user = user = db.query(User_Account).filter(User_Account.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="404 - User Not Found!")

    try:
        if xp.startswith('-'):
            xp_value = -int(xp[1:])
        else:
            xp_value = int(xp)
    except ValueError:
        raise HTTPException(status_code=400, detail="400 - Invalid XP Value")

    user.xp += xp_value
    db.commit()
    db.refresh(user)
    return user


def create_user_favourite_campsite(db, username, campsite_id):
    user = db.query(User_Account).filter(User_Account.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="404 - User Not Found!")

    campsite = db.get(Campsite, campsite_id)
    if not campsite:
        raise HTTPException(
            status_code=404, detail="404 - Campsite Not Found!")
    if campsite_id not in user.favourites:
        user.favourites.append(campsite)
        db.commit()
    return


def read_user_campsite_favourites_by_username(db, username: str):
    user = db.query(User_Account).filter(User_Account.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="404 - User Not Found!")
    print(user.username)
    return user.favourites


def remove_user_favourite_campsite(db, username, campsite_id):
    user = db.query(User_Account).filter(User_Account.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="404 - User Not Found!")

    campsite = db.get(Campsite, campsite_id)
    if not campsite:
        raise HTTPException(
            status_code=404, detail="404 - Campsite Not Found!")

    if campsite in user.favourites:
        user.favourites.remove(campsite)
        db.commit()
        return {"message": f"Campsite {campsite.campsite_id} removed from favourites."}
    else:
        raise HTTPException(
            status_code=404, detail="404 - Campsite Not Found In User Favourites!")
