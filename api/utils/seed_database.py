from api.models.user_models import user_campsite_favourites
from api.config.config import PRE_HASHED_USER_PASSWORD



def seed_categories(session, categories):
    for category in categories:
        session.add(category)
    session.commit()


def seed_facilities(session, facilities):
    for facility in facilities:
        session.add(facility)
    session.commit()


def seed_activities(session, activities):
    for activity in activities:
        session.add(activity)
    session.commit()


def seed_campsites(session, campsites):
    for campsite in campsites:
        session.add(campsite)
    session.commit()


def seed_photos(session, photos):
    for photo in photos:
        session.add(photo)
    session.commit()


def seed_contacts(session, contacts):
    for contact in contacts:
        session.add(contact)
    session.commit()


def seed_users_credentials(session, users_credentials):
    # Pre-hashed password to speed up the seeding process
    # This password was generated using the `hash_password` utility function.
    # It must be stored in a .ENV named .env.pre_hashed_user_password
    # the hash should be correctly formatted by the util function 
    # as a string as a string in the following format:
    # PRE_HASHED_USER_PASSWORD=b'HASHEDPASSWORDHERE'
    # If you need to update the password or set up a new local repo... 
    # generate a new hash using: `hash_password('your_password_here')`
    for user_credentials in users_credentials:
        user_credentials.hashed_password = PRE_HASHED_USER_PASSWORD
        session.add(user_credentials)
    session.commit()

def seed_user_accounts(session, user_accounts):
    for user_account in user_accounts:
        session.add(user_account)
    session.commit()

def seed_reviews(session, reviews):
    for review in reviews:
        session.add(review)
    session.commit()


def seed_user_campsite_favourites(session, favourites_data, user_campsite_favourites):
    for username, campsite_ids in favourites_data:
        for campsite_id in campsite_ids:
            session.execute(user_campsite_favourites.insert().values(
                username=username, campsite_id=campsite_id))
    session.commit()


def seed_database(session, data):
    if 'users_credentials' in data:
        seed_users_credentials(session, data['users_credentials'])
    if 'user_accounts' in data:
        seed_user_accounts(session, data['user_accounts'])
    if 'campsite_category' in data:
        seed_categories(session, data['campsite_category'])
    if 'facility' in data:
        seed_facilities(session, data['facility'])
    if 'activity' in data:
        seed_activities(session, data['activity'])
    if 'campsite' in data:
        seed_campsites(session, data['campsite'])
    if 'campsite_photo' in data:
        seed_photos(session, data['campsite_photo'])
    if 'campsite_contact' in data:
        seed_contacts(session, data['campsite_contact'])
    if 'review' in data:
        seed_reviews(session, data['review'])
    if 'user_campsite_favourites' in data:
        seed_user_campsite_favourites(
            session, data['user_campsite_favourites'], user_campsite_favourites)
