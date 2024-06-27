from datetime import date
from init import db, ma
from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Text, String, ForeignKey, Date
from marshmallow import fields
from marshmallow.validate import Length


class Contact(db.Model):
    __tablename__ = "contacts"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(200))
    ph_number: Mapped[int] = mapped_column(String)
    emergency_contact: Mapped[bool] = mapped_column(server_default="false")
    email: Mapped[str] = mapped_column(server_default="No email provided")

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="contacts")

    attendances: Mapped[List["Attendance"]] = relationship(
        back_populates="contact", cascade="all, delete"
    )


class ContactSchema(ma.Schema):
    email = fields.Email()
    ph_number = fields.String(validate=Length(min=10, max=10))

    user = fields.Nested("UserSchema", exclude=["password", "is_admin", "is_teacher"])
    
    attendances=fields.List(fields.Nested("AttendanceSchema", exclude=['contact']))

    class Meta:
        ordered = True
        fields = ("first_name", "emergency_contact", "ph_number", "email")
        