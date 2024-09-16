from pydantic import BaseModel, Field, field_validator
from typing import Annotated


class ReviewBase(BaseModel):
    user_account_id: int
    rating: Annotated[int, Field(ge=1, le=5)]
    comment: Annotated[str, Field(max_length=350)] | None = ""

    @field_validator('rating')
    def validate_rating(cls, rating):
        if rating < 1 or rating > 5:
            raise ValueError('Rating should be between 1 and 5')
        return rating

    @field_validator('comment')
    def validate_comment(cls, comment):
        if comment is not None and len(comment) > 350:
            raise ValueError('String should have at most 350 characters')
        return comment


class ReviewPostRequest(ReviewBase):
    pass


class ReviewPatchRequest(ReviewBase):
    rating: Annotated[int, Field(ge=1, le=5)] | None = None


class ReviewResponse(ReviewBase):
    review_id: int
    campsite_id: int
    username: str
    rating: Annotated[int, Field(ge=1, le=5)]


class Review(ReviewBase):
    review_id: int
    campsite_id: int
    username: str
    rating: Annotated[int, Field(ge=1, le=5)]

    class ConfigDict:
        from_attributes = True
