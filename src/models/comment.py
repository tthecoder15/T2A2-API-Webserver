from datetime import date
from init import db, ma
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Text, String, ForeignKey, Date, Boolean
from marshmallow import fields
from marshmallow.validate import OneOf, Length


class Comment(db.Model):
    __tablename__ = "comments"
    comment_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    message: Mapped[str] = mapped_column(Text)
    urgency: Mapped[str] = mapped_column(String)
    date_created: Mapped[date] = mapped_column(Date)

    comment_edited: Mapped[bool] = mapped_column(Boolean(), server_default="false")
    date_edited: Mapped[date] = mapped_column(Date, nullable=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="comments")

    child_id: Mapped[int] = mapped_column(ForeignKey("children.id"))
    child: Mapped["Child"] = relationship(back_populates="comments")


class CommentSchema(ma.Schema):
    message = fields.String(validate= Length(min=3, error = "Comments need to be at least 3 characters long"))
    date_created = fields.String()
    urgency = fields.String(validate= OneOf(["urgent", "positive", "neutral"]))
    
    user = fields.Nested("UserSchema", only=['first_name', "id"])
    child = fields.Nested("ChildSchema", only=["id", "first_name", "last_name"])

    class Meta:
        ordered = True
        fields = ("child", "user", "comment_edited", "date_edited", "date_created", "urgency", "message")
