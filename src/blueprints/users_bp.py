from datetime import timedelta
from flask import Blueprint, request
from models.user import User, UserSchema
from flask_jwt_extended import create_access_token
from init import db, bcrypt
from auth import admin_check, user_status
from flask_jwt_extended import jwt_required, get_jwt_identity


users_bp = Blueprint("user", __name__, url_prefix="/users")


# READ All User
@users_bp.route("/", methods=["GET"])
@jwt_required()
def get_users():
    user_id = get_jwt_identity()
    if admin_check(user_id):
        stmt = db.select(User)
        users = db.session.scalars(stmt).all()
        return UserSchema(many=True, exclude=["password"]).dump(users)
    else:
        return {"Error": "You are not authorised to access this resource"}, 403


# READ One User
@users_bp.route("/<int:id>", methods=["GET"])
@jwt_required()
def get_user(id):
    user_id = get_jwt_identity()
    user_type = user_status(user_id)
    if user_type == "Admin":
        user = db.get_or_404(User, id)
        return UserSchema(exclude=["password"]).dump(user)
    if user_type == "Parent" or user_type == "Teacher":
        user = db.get_or_404(User, id)
        if user.id == user_id:
            return UserSchema(exclude=["password", "is_admin", "is_teacher"]).dump(user)
        else:
            return {"Error": "You are not authorised to access this resource"}, 403


# LOGIN
@users_bp.route("/signin", methods=["POST"])
def login():
    if len(request.json["password"]) < 8:
        return {"Error": "Incorrect email or password"}, 400
    params = UserSchema(only=["email", "password"]).load(
        request.json, unknown="exclude"
    )
    stmt = db.select(User).where(User.email == params["email"])
    user = db.session.scalar(stmt)
    if user and bcrypt.check_password_hash(user.password, params["password"]):
        token = create_access_token(identity=user.id, expires_delta=timedelta(hours=2))
        return {"token": token}
    else:
        return {"Error": "Incorrect email or password"}, 403


# Create User, admin auth
@users_bp.route("/admin", methods=["POST"])
@jwt_required()
def create_user_admin():
    user_id = get_jwt_identity()
    user_type = user_status(user_id)

    if user_type == "Admin":
        # Check if email in db
        stmt = db.select(User).where(User.email == request.json["email"])
        user = db.session.scalar(stmt)

        if user:
            return {
                "Error": "Email already registered. Please provide a unique email address"
            }, 400

        input_info = UserSchema(
            only=["email", "first_name", "password", "is_admin", "is_teacher"],
            unknown="exclude",
        ).load(request.json)

        new_user = User(
            email=input_info["email"],
            password=bcrypt.generate_password_hash(input_info["password"]).decode(
                "utf-8"
            ),
            first_name=input_info["first_name"].capitalize(),
            is_admin=str(input_info["is_admin"]).capitalize() in ["True"],
            is_teacher=str(input_info["is_teacher"]).capitalize() in ["True"],
        )

        db.session.add(new_user)
        db.session.commit()

        return {
            "Success": UserSchema(
                only=["email", "first_name", "is_admin", "is_teacher"]
            ).dump(new_user)
        }, 201
    else:
        return {"Error": "You are not authorised to access this resource"}, 403


# Create User, not a user
@users_bp.route("/", methods=["POST"])
def create_user():
    # Check if email in db
    stmt = db.select(User).where(User.email == request.json["email"])
    user = db.session.scalar(stmt)
    if user:
        return {
            "Error": "This email is already registered to a user. Please provide a unique email address"
        }, 400

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


# UPDATE User
@users_bp.route("/<int:id>", methods=["PATCH"])
@jwt_required()
def update_user(id):
    user_id = get_jwt_identity()
    user_type = user_status(user_id)

    if "email" in request.json:
        stmt = db.select(User).where(User.email == request.json["email"])
        user = db.session.scalar(stmt)
        if user:
            return {
                "Error": "This email is already registered to a user. Please provide a unique email address"
            }, 400

    if "first_name" in request.json:
        request.json["first_name"] = request.json["first_name"].capitalize()
    if "is_admin" in request.json:
        request.json["is_admin"] = request.json["is_admin"].capitalize()
    if "is_teacher" in request.json:
        request.json["is_teacher"] = request.json["is_teacher"].capitalize()

    new_info = UserSchema(
        only=["email", "first_name", "is_admin", "is_teacher", "password"],
        unknown="exclude",
    ).load(request.json)

    if new_info == {}:
        return {"Error": "Please provide at least one value to update"}, 400

    user = db.get_or_404(User, id)

    if user_type == "Admin" or user.id == user_id:
        user.email = request.json.get("email", user.email)
        user.first_name = request.json.get("first_name", user.first_name)
        if user_type == "Admin":
            user.is_admin = str(
                request.json.get("is_admin", user.is_admin)
            ) in ["True"]
            user.is_teacher = str(
                request.json.get("is_teacher", user.is_teacher)
            ) in ["True"]
        db.session.commit()

        if "password" in request.json:
            new_info.update({"password": "Password successfully updated"})

        return {"Updated fields": new_info}, 200

    else:
        return {"Error": "You are not authorised to access this resource"}, 403


# DELETE User
@users_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_user(id):
    user_id = get_jwt_identity()
    user_type = user_status(user_id)
    user = db.get_or_404(User, id)

    if user_type == "Admin":
        db.session.delete(user)
        db.session.commit()
        return {"Success": "User registration deleted"}, 200
    else:
        return {"Error": "You are not authorised to access this resource"}, 403
