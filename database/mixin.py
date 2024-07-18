from sqlalchemy.orm import (
    declared_attr,
    Mapped,
    WriteOnlyMapped,
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
    def user(cls) -> WriteOnlyMapped['User']:
        return relationship('User', back_populates=cls.back_populates)
    
    @declared_attr
    def user_id(cls) -> Mapped[Integer]:
        return mapped_column(Integer, ForeignKey('users.id'))