from datetime import date
from init import db, ma
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Text, String, ForeignKey, Date
from marshmallow import fields


class Attendance(db.Model):
    __tablename__ = "attendances"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    child_id: Mapped[int] = mapped_column(ForeignKey("children.id"))
    child: Mapped["Child"] = relationship(back_populates="attendances")

    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id"))
    group: Mapped["Group"] = relationship(back_populates="attendances")

    contact_id: Mapped[int] = mapped_column(ForeignKey("contacts.id"))
    contact: Mapped["Contact"] = relationship(back_populates="attendances")


class AttendanceSchema(ma.Schema):
    message = fields.String(required=True)
    date_created = fields.String(required=True)

    child = fields.Nested("ChildSchema")
    group = fields.Nested("GroupSchema", only=["group_name", "day"])
    contact = fields.Nested("ContactSchema")

    class Meta:
        ordered = True
        fields = ("child", "group", "contact")
