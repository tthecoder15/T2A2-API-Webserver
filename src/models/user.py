from typing import Optional, List
from init import db, ma
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean
from marshmallow import fields
from marshmallow.validate import Length, And, Regexp


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
    email = fields.Email()
    first_name = fields.String(
        validate=And(
            Regexp(
                "^[a-zA-Z'-]+(?: [a-zA-Z'-]+)*$",
                error="Names must not contain numbers or special characters besides hyphens, apostrophes and spaces",
            ),
            Length(min=2, error="First name must be at least 2 characters"),
        )
    )
    password = fields.String(validate=Length(min=8))
    is_admin = fields.Boolean()
    is_teacher = fields.Boolean()

    children = fields.List(
        fields.Nested("ChildSchema", only=["first_name", "last_name"])
    )
    contacts = fields.List(fields.Nested("ContactSchema"))
    comments = fields.List(fields.Nested("CommentSchema", exclude=["user"]))

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
