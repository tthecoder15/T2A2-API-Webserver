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
  
    user=fields.Nested("UserSchema", exclude=["password", "is_admin", "is_teacher"])
    comments=fields.List(fields.Nested("CommentSchema", exclude=['child']))
    attendances=fields.List(fields.Nested("AttendanceSchema", only=['group']))


    class Meta:
        ordered = True
        fields = ("id", "user_id", "first_name", "last_name", "attendances", "comments")
