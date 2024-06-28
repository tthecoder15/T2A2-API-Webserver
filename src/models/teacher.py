from typing import List
from init import db, ma
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Text, String
from marshmallow import fields
from marshmallow.validate import Length, Regexp, And


class Teacher(db.Model):
    __tablename__ = "teachers"
    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    first_name: Mapped[str] = mapped_column(Text)
    email: Mapped[str] = mapped_column(String(200))
   
    groups: Mapped[List["Group"]] = relationship(
        back_populates="teacher", cascade="all, delete"
    )
    
class TeacherSchema(ma.Schema):
    first_name=fields.String(validate=And(
            Regexp(
                "^[a-zA-Z'-]+(?: [a-zA-Z'-]+)*$",
                error="Names must not contain numbers or special characters besides hyphens, apostrophes and spaces",
            ),
            Length(min=2, error="First name must be at least 2 characters")))
    groups=fields.List(fields.Nested("GroupSchema", exclude=['teacher']))

    class Meta:
        fields = ("id", "first_name", "email", "groups")
