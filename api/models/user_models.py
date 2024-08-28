from typing import List
from database.database import Base
from sqlalchemy import Column, Integer, String, Boolean, LargeBinary, ForeignKey, Table
from sqlalchemy.orm import relationship, Mapped

user_campsite_favourites = Table(
    "user_campsite_favourites",
    Base.metadata,
    Column("user_account_id", Integer, ForeignKey(
        'user_accounts.user_account_id', ondelete="CASCADE"), primary_key=True),
    Column("campsite_id", Integer, ForeignKey(
        "campsites.campsite_id", ondelete="CASCADE"), primary_key=True)
)


class User_Credentials(Base):
    __tablename__ = "user_credentials"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(30), unique=True)
    hashed_password = Column(LargeBinary)


class User_Account(Base):
    __tablename__ = "user_accounts"

    user_account_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user_credentials.user_id"))
    user_firstname = Column(String, default="n/a")
    user_lastname = Column(String, default="n/a")
    user_email = Column(String, default="n/a")
    xp = Column(Integer, default=0)
    user_type = Column(String, default="NORMAL")
    camera_permission = Column(Boolean, default=False)

    favourites: Mapped[List["Campsite"]] = relationship(
        'Campsite', secondary=user_campsite_favourites, back_populates='favourited_by')
    reviews = relationship(
        "Review", back_populates="user_account", lazy='dynamic')
    campsites = relationship(
        "Campsite", back_populates="user_account", lazy='dynamic')
