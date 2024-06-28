from typing import List
from init import db, ma
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Text, ForeignKey, String
from marshmallow import fields
from marshmallow.validate import And, Regexp, Length, OneOf


class Group(db.Model):
    __tablename__ = "groups"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    group_name: Mapped[str] = mapped_column(Text)
    day: Mapped[str] = mapped_column(String)

    teacher_id: Mapped[int] = mapped_column(ForeignKey("teachers.id"))
    teacher: Mapped["Teacher"] = relationship(back_populates="groups")

    attendances: Mapped[List["Attendance"]] = relationship(
        back_populates="group", cascade="all, delete"
    )


class GroupSchema(ma.Schema):
    group_name = fields.String(validate=And(
            Regexp(
                "^[a-zA-Z'-]+(?: [a-zA-Z'-]+)*$",
                error="Names must not contain numbers or special characters besides hyphens, apostrophes and spaces",
            ),
            Length(min=3, error="Group names must be at least 3 characters")))
    
    day = fields.String(
        validate=OneOf(
            [
                "Monday",
                "Tuesday",
                "Wednesday",
                "Thursday",
                "Friday",
                "Saturday",
                "Sunday",
            ]
        )
    )

    teacher = fields.Nested("TeacherSchema", exclude=["groups"])
    attendances = fields.List(fields.Nested("AttendanceSchema", exclude=["group"]))

    class Meta:
        ordered = True
        fields = ("id", "day", "group_name", "teacher")
