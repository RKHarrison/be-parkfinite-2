from pydantic import BaseModel, field_validator
from api.schemas.campsite_schemas import Campsite
import re


class UserBase(BaseModel):
    username: str

    class ConfigDict:
        from_attributes = True

    @field_validator('username')
    @classmethod
    def validate_username(cls, username):
        if len(username) < 6 or len(username) > 30:
            raise ValueError('Username should be between 6 and 30 characters.')
        return username


class CreateUserRequest(UserBase):
    password: str


class User(UserBase):
    hashed_password: str
    favourites: list[Campsite] = []
    user_firstname: str
    user_lastname: str
    user_email: str
    xp: int
    user_type: str
    camera_permission: bool


# NEEDS RENAMING TO FavouriteUserCampsite
class UserCampsiteBase(BaseModel):
    username: str
    campsite_id: int


class CreateUserCampsite(UserCampsiteBase):
    pass


class UserCampsite(UserCampsiteBase):
    user_campsite_id: int
