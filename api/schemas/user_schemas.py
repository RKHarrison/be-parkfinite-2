from pydantic import BaseModel, field_validator
from api.schemas.campsite_schemas import Campsite
import re


class UserCredentialsBase(BaseModel):
    username: str

    class ConfigDict:
        from_attributes = True

    @field_validator('username')
    @classmethod
    def validate_username(cls, username):
        if len(username) < 6 or len(username) > 30:
            raise ValueError('Username should be between 6 and 30 characters.')
        if not re.match('^[a-zA-Z0-9_]*$', username):
            raise ValueError(
                'Username must be alphanumeric and can include underscores.')
        return username


class CreateUserCredentialsRequest(UserCredentialsBase):
    password: str

    @field_validator('password')
    @classmethod
    def validate_password_strength(cls, password):
        if len(password) < 8 or len(password) > 64:
            raise ValueError('Password should be between 8 and 64 characters.')
        if not re.search(r"\d", password):
            raise ValueError('Password must include at least one digit.')
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            raise ValueError(
                'Password must include at least one special character.')
        return password


class UserCredentials(UserCredentialsBase):
    user_id: int


class UserAccountBase(BaseModel):
    user_id: int

class CreateUserAccountDetails(UserAccountBase):
    user_firstname: str
    user_lastname: str
    user_email: str
    camera_permission: bool


class UserAccountDetails(UserCredentialsBase):
    user_firstname: str
    user_lastname: str
    user_email: str
    xp: int
    user_type: str
    camera_permission: bool

class UserFavourites(UserAccountBase):
    favourites: list[Campsite] = []






# NEEDS RENAMING TO FavouriteUserCampsite
class UserCampsiteBase(BaseModel):
    user_id: str
    campsite_id: int


class CreateUserCampsite(UserCampsiteBase):
    pass


class UserCampsite(UserCampsiteBase):
    user_campsite_id: int
