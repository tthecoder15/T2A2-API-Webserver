from init import db, ma
from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey
from marshmallow import fields
from marshmallow.validate import Length, And, Regexp


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
    ph_number = fields.String(
        validate=And(
            Length(min=10, max=10, error="Phone numbers must be 10 characters"),
            Regexp("^[0-9]*$", error="Phone numbers must only contain numbers"),
        )
    )
    first_name = fields.String(
        validate=And(
            Regexp(
                "^[a-zA-Z'-]+(?: [a-zA-Z'-]+)*$",
                error="Names must not contain numbers or special characters besides hyphens, apostrophes and spaces",
            ),
            Length(min=2, error="First name must be at least 2 characters"),
        )
    )

    user = fields.Nested("UserSchema", exclude=["password", "is_admin", "is_teacher"])

    attendances = fields.List(fields.Nested("AttendanceSchema", exclude=["contact"]))

    class Meta:
        ordered = True
        fields = ("first_name", "emergency_contact", "ph_number", "email")
