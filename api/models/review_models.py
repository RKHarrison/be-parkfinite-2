from database.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped


class Review(Base):
    __tablename__ = "reviews"

    review_id = Column(Integer, primary_key=True)
    rating = Column(Integer)
    comment = Column(String)
    user_account_id = Column(Integer, ForeignKey("user_accounts.user_account_id"))

    campsite_id = Column(Integer, ForeignKey(
        "campsites.campsite_id", ondelete="CASCADE"))
    
    user_account = relationship("User_Account", back_populates="reviews")
    campsite = relationship("Campsite", back_populates="reviews")
