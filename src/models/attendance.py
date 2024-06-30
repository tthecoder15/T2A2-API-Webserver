from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from marshmallow import fields
from init import db, ma


class Attendance(db.Model):
    __tablename__ = "attendances"
    attendance_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    child_id: Mapped[int] = mapped_column(ForeignKey("children.id"))
    child: Mapped["Child"] = relationship(back_populates="attendances")

    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id"))
    group: Mapped["Group"] = relationship(back_populates="attendances")

    contact_id: Mapped[int] = mapped_column(ForeignKey("contacts.id"))
    contact: Mapped["Contact"] = relationship(back_populates="attendances")


class AttendanceSchema(ma.Schema):

    child = fields.Nested(
        "ChildSchema",
        only=["id", "user_id", "first_name", "last_name"],
        exclude=["attendances"],
    )
    group = fields.Nested("GroupSchema", only=["group_name", "day"])
    contact = fields.Nested("ContactSchema", exclude=["attendances"])

    class Meta:
        ordered = True
        fields = ("attendance_id", "child_id", "child", "group", "contact")
