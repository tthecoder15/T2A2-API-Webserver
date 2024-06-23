from models.users import User
from init import db
from marshmallow import ValidationError


def auth_check(user_id):
    stmt = db.select(User).where(User.id == user_id, User.is_admin)
    user = db.session.scalar(stmt)
    if user:
        return
    else:
        raise ValidationError("You must be an admin to access this resource", 403)
