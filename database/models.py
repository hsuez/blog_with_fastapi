from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
    WriteOnlyMapped
)
from sqlalchemy import (
    Integer, 
    String,
    ForeignKey,
    text,
)
from pydantic import EmailStr
from typing import Optional, Annotated
from datetime import datetime

from . import Base
from .mixin import UserRelationMixin


class User(Base):
    username: Mapped[str] = mapped_column(String(64), index=True)
    password_hash: Mapped[str] = mapped_column(String)
    email: Mapped[Optional[EmailStr]] = mapped_column(String(128), nullable=True)

    posts: WriteOnlyMapped[list["Post"]] = relationship("Post", back_populates="user")
    profile: WriteOnlyMapped["Profile"] = relationship("Profile", back_populates="user")

created_at = Annotated[datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]

class Post(UserRelationMixin, Base):
    back_populates = 'posts'

    title: Mapped[str] = mapped_column(String(256))
    body: Mapped[Optional[str]] = mapped_column(String)
    created_at: Mapped[created_at]

str_64 = Annotated[str, mapped_column(String(64))]

class Profile(UserRelationMixin, Base):
    back_populates = 'profile'

    name: Mapped[str_64]
    surname: Mapped[str_64]
    created_at: Mapped[created_at]