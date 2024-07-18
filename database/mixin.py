from sqlalchemy.orm import (
    declared_attr,
    Mapped,
    mapped_column,
    relationship,
)
from sqlalchemy import (
    Integer, 
    String,
    ForeignKey,
)
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import User


class UserRelationMixin:
    back_populates: str

    @declared_attr
    def user(cls) -> Mapped['User']:
        return relationship(back_populates=cls.back_populates)
    
    @declared_attr
    def user_id(cls) -> Mapped[Integer]:
        return mapped_column(Integer, ForeignKey('users.id'))