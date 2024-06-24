from typing import Optional, List
from init import db, ma
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Text, String, Boolean
from marshmallow import fields
from marshmallow.validate import Length, OneOf


class User(db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    email: Mapped[str] = mapped_column(String(200))
    password: Mapped[Optional[str]] = mapped_column(String(200))
    first_name: Mapped[str] = mapped_column(String(200))
    is_admin: Mapped[bool] = mapped_column(Boolean(), server_default="false")
    is_teacher: Mapped[bool] = mapped_column(Boolean(), server_default="false")

    children: Mapped[List["Child"]] = relationship(
        back_populates="user", cascade="all, delete"
    )

    comments: Mapped[List["Comment"]] = relationship(
        back_populates="user", cascade="all, delete"
    )

    contacts: Mapped[List["Contact"]] = relationship(
        back_populates="user", cascade="all, delete"
    )


class UserSchema(ma.Schema):
    email = fields.Email(required=True)
    first_name = fields.String(required=True)
    password = fields.String(validate=Length(min=8), required=True)
    is_admin = fields.Boolean()
    is_teacher = fields.Boolean()

    children = fields.List(
        fields.Nested("ChildSchema", only=["first_name", "last_name"])
    )
    contacts = fields.List(fields.Nested("ContactSchema"))

    class Meta:
        ordered = True
        fields = (
            "id",
            "email",
            "first_name",
            "is_admin",
            "is_teacher",
            "password",
            "children",
            "contacts",
        )