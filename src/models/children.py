from typing import List
from datetime import date
from init import db, ma
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey
from marshmallow import fields


class Child(db.Model):
    __tablename__ = "children"
    id: Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(200))
    last_name: Mapped[str] = mapped_column(String(200))

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="children")

    comments: Mapped[List["Comment"]] = relationship(
        back_populates="children", cascade="all, delete"
    )

    attendances: Mapped[List["Attendance"]] = relationship(
        back_populates="children", cascade="all, delete"
    )


class ChildSchema(ma.Schema):
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    
    comments=fields.Nested("CommentSchema", exclude=["user", "child"])

    attendances=fields.Nested("AttendanceSchema", exclude=["child"])

    class Meta:
        ordered = True
        fields = ("id", "first_name", "last_name", "attendances", "comments")
