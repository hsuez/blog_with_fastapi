from sqlalchemy.orm import (
    DeclarativeBase,
    declared_attr,
    Mapped,
    mapped_column,
)
from sqlalchemy import (
    Integer,
    String,
)
from typing import Annotated


class Base(DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    @declared_attr
    def __tablename__(cls) -> str:
        return f'{cls.__name__.lower()}s'


string = Annotated[str, mapped_column(String)]

class Cookie(Base):
    session_id: Mapped[str] = mapped_column(String, index=True)
    access_token: Mapped[string]
    refresh_token: Mapped[string]