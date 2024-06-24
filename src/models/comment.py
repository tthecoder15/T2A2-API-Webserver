from datetime import date
from init import db, ma
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Text, String, ForeignKey, Date
from marshmallow import fields
from marshmallow.validate import OneOf


class Comment(db.Model):
    __tablename__ = "comments"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    message: Mapped[str] = mapped_column(Text)
    urgency: Mapped[str] = mapped_column(String)
    date_created: Mapped[date] = mapped_column(Date)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="comments")

    child_id: Mapped[int] = mapped_column(ForeignKey("children.id"))
    children: Mapped["Child"] = relationship(back_populates="comments")


class CommentSchema(ma.Schema):
    message = fields.String(required=True)
    date_created = fields.String(required=True)
    urgency = fields.String(validate= OneOf(["urgent", "positive", "neutral"]))
    
    user = fields.Nested("UserSchema", only=['email'])
    child = fields.Nested("ChildSchema")

    class Meta:
        ordered = True
        fields = ("child", "user", "date_created", "urgency", "message")
