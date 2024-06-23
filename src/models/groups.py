from typing import List
from datetime import date
from init import db, ma
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Text, Date, ForeignKey, String
from marshmallow import fields


class Group(db.Model):
    __tablename__ = "groups"
    id: Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    group_name: Mapped[str] = mapped_column(Text)
    day: Mapped[str] = mapped_column(String)

    teacher_id: Mapped[int] = mapped_column(ForeignKey("teachers.id"))
    teacher: Mapped["Teacher"] = relationship(back_populates="groups")

    attendances: Mapped[List["Attendance"]] = relationship(
        back_populates="group", cascade="all, delete"
    )


class GroupSchema(ma.Schema):
    group_name = fields.String(required=True)
    day = fields.String(required=True)

    teacher = fields.Nested("TeacherSchema")
    
    attendances=fields.Nested("AttendanceSchema", exclude=["group"])

    class Meta:
        ordered=True
        fields = ("id", "day", "group_name", "teacher")
