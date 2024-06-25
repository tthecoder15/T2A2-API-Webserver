from datetime import timedelta
from flask import Blueprint, request
from models.user import User, UserSchema
from flask_jwt_extended import create_access_token
from init import db, bcrypt
from marshmallow.exceptions import ValidationError
from auth import auth_check
from flask_jwt_extended import jwt_required, get_jwt_identity


users_bp = Blueprint("user", __name__, url_prefix="/users")

# READ All
@users_bp.route("/", methods=["GET"])
@jwt_required()
def get_users():
    auth_check(get_jwt_identity())
    stmt = db.select(User)
    users = db.session.scalars(stmt).all()
    return UserSchema(many=True, exclude=["password"]).dump(users)

# READ One
@users_bp.route("/<int:id>", methods=["GET"])
@jwt_required()
def get_user(id):
    auth_check(get_jwt_identity())
    user = db.get_or_404(User, id)
    return UserSchema(exclude=["password"]).dump(user)

# LOGIN
@users_bp.route("/signin", methods=["POST"])
def login():
    if len(request.json["password"]) < 8:
        raise ValidationError("Incorrect email or password")
    params = UserSchema(only=["email", "password"]).load(
        request.json, unknown="exclude"
    )
    stmt = db.select(User).where(User.email == params["email"])
    user = db.session.scalar(stmt)
    if user and bcrypt.check_password_hash(user.password, params["password"]):
        token = create_access_token(identity=user.id, expires_delta=timedelta(hours=2))
        return {"token": token}
    else:
        raise ValidationError("Incorrect email or password")


# ADMIN USER REGISTER
@users_bp.route("/", methods=["POST"])
@jwt_required()
def signup_admin():
    auth_check(get_jwt_identity())

    # Check if email in db
    stmt = db.select(User).where(User.email == request.json["email"])
    user = db.session.scalar(stmt)
    if user:
        raise ValidationError("Email already registered. Please use a different email.")

    input_info = UserSchema(
        only=["email", "first_name", "password", "is_admin", "is_teacher"],
        unknown="exclude",
    ).load(request.json)

    new_user = User(
        email=input_info["email"],
        password=bcrypt.generate_password_hash(input_info["password"]).decode("utf-8"),
        first_name=input_info["first_name"].capitalize(),
        is_admin=input_info["is_admin"],
        is_teacher=input_info["is_teacher"],
    )

    db.session.add(new_user)
    db.session.commit()
    return {
        "Success": UserSchema(
            only=["email", "first_name", "is_admin", "is_teacher"]
        ).dump(new_user)
    }, 201


# NON-AUTHORISED USER REGISTER
@users_bp.route("/signup", methods=["POST"])
def user_signup():
    # Check if email in db
    stmt = db.select(User).where(User.email == request.json["email"])
    user = db.session.scalar(stmt)
    if user:
        raise ValidationError("Email already registered. Please use a different email.")

    input_info = UserSchema(
        only=["email", "first_name", "password"],
        unknown="exclude",
    ).load(request.json)

    new_user = User(
        email=input_info["email"],
        password=bcrypt.generate_password_hash(input_info["password"]).decode("utf-8"),
        first_name=input_info["first_name"].capitalize(),
    )

    db.session.add(new_user)
    db.session.commit()
    return {"Success": UserSchema(only=["email", "first_name"]).dump(new_user)}, 201
