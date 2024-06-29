from typing import List
from datetime import date
from init import db, ma
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey
from marshmallow import fields
from marshmallow.validate import Regexp, And, Length


class Child(db.Model):
    __tablename__ = "children"
    id: Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(200))
    last_name: Mapped[str] = mapped_column(String(200))

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="children")

    comments: Mapped[List["Comment"]] = relationship(
        back_populates="child", cascade="all, delete"
    )
    attendances: Mapped[List["Attendance"]] = relationship(
        back_populates="child", cascade="all, delete"
    )


class ChildSchema(ma.Schema):
    first_name=fields.String(validate=And(Regexp("^[a-zA-Z'-]+(?: [a-zA-Z'-]+)*$", error="Names must not contain numbers or special characters besides hyphens, apostrophes and spaces"),
    Length(min=2, error="First name must be at least 2 characters")))
    last_name=fields.String(validate=And(Regexp("^[a-zA-Z'-]+(?: [a-zA-Z'-]+)*$", error="Names must not contain numbers or special characters besides hyphens, apostrophes and spaces"),
    Length(min=2, error="Last name must be at least 2 characters")))
    
    user=fields.Nested("UserSchema", exclude=["password", "is_admin", "is_teacher"])
    comments=fields.List(fields.Nested("CommentSchema", exclude=['child', 'comment_edited', 'date_edited']))
    attendances=fields.List(fields.Nested("AttendanceSchema", only=['attendance_id', 'group']))


    class Meta:
        ordered = True
        fields = ("id", "user_id", "first_name", "last_name", "attendances", "comments")
