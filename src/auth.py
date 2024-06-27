from init import db
from models.user import User, UserSchema



def admin_check(user_id):
    stmt = db.select(User).where(User.id == user_id, User.is_admin)
    user = db.session.scalar(stmt)
    if user:
        return True
    else:
        return False 
        

def user_status(user_id):
    user = db.get_or_404(User, user_id)
    user = UserSchema(exclude=["password"]).dump(user)
    if user["is_admin"] == True:
        return "Admin"
    elif user["is_teacher"] == True:
        return "Teacher"
    else:
        return "Parent"