from typing import Optional, List
from init import db, ma
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Text, String, Boolean
from marshmallow import fields
from marshmallow.validate import Length


class Teacher(db.Model):
    __tablename__ = "teachers"
    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    first_name: Mapped[str] = mapped_column(Text)
    email: Mapped[str] = mapped_column(String(200))
   
    groups: Mapped[List["Group"]] = relationship(
        back_populates="teacher", cascade="all, delete"
    )
    
class TeacherSchema(ma.Schema):
    email = fields.Email(required=True)

    groups=fields.Nested("GroupSchema", exclude=["teacher"])

    class Meta:
        fields = ("first_name", "email", "groups")
