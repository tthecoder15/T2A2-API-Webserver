from datetime import timedelta
from flask import Blueprint, request
from models.child import Child, ChildSchema
from models.user import User, UserSchema
from flask_jwt_extended import create_access_token
from init import db, bcrypt
from marshmallow.exceptions import ValidationError
from auth import auth_check, user_status
from flask_jwt_extended import jwt_required, get_jwt_identity


children_bp = Blueprint("child", __name__, url_prefix="/children")

# READ Child
@children_bp.route("/", methods=["GET"])
@jwt_required()
def get_children():
    user_id = get_jwt_identity()
    user_type = user_status(user_id)

    if user_type == "Admin":
        stmt = db.select(Child)
        children = db.session.scalars(stmt).all()
        return ChildSchema(many=True).dump(children)
    else:
        stmt = db.select(Child).where(Child.user_id == user_id)
        registered_children = db.session.scalars(stmt)
        return ChildSchema(many=True).dump(registered_children)


@children_bp.route("/<int:id>", methods=["GET"])
@jwt_required()
def get_child(id):
    child = db.get_or_404(Child, id)
    child_dict = ChildSchema().dump(child)
    print(child_dict)
    user_id = get_jwt_identity()
    user_type = user_status(user_id)
    if user_type == "Admin" or child_dict["user_id"] == user_id:
        return child_dict
    else:
        raise ValidationError(
            "You must are not authorised to access this resource", 403
        )


# CREATE Child
@children_bp.route("/", methods=["POST"])
@jwt_required()
def register_movie():
    user_id = get_jwt_identity()
    user_type = user_status(user_id)

    if user_type == "Teacher":
        raise ValidationError("This feature is for parent users", 403)

    child_info = ChildSchema(only=["first_name", "last_name"], unknown="exclude").load(
        request.json
    )

    new_child = Child(
        first_name=child_info["first_name"].capitalize(),
        last_name=child_info["last_name"].capitalize(),
    )

    if user_type == "Admin":
        stmt = db.select(User).where(User.id == request.json["user_id"])
        user = db.session.scalar(stmt)
        if not user:
            raise ValidationError(
                "No such user. Please check user_id matches a registered user"
            )
        new_child.user_id = request.json["user_id"]

    elif user_type == "Parent":
        new_child.user_id = user_id

    # Check if child with the same f/l_name & user_id is in database already
    stmt = db.select(Child).where(
        Child.first_name == new_child.first_name,
        Child.last_name == new_child.last_name,
        Child.user_id == new_child.user_id,
    )
    print(stmt)
    print(new_child.first_name)
    child = db.session.scalar(stmt)
    if child:
        raise ValidationError("This child is already registered to this user", 401)

    db.session.add(new_child)
    db.session.commit()
    return {
        "Success": ChildSchema(only=["first_name", "last_name", "user_id"]).dump(
            new_child
        )
    }, 201


# UPDATE Child
@children_bp.route("/<int:id>", methods=["PATCH"])
@jwt_required()
def update_child(id):
    user_id = get_jwt_identity()
    user_type = user_status(user_id)
    child = db.get_or_404(Child, id)

    if user_type == "Admin" or child.user_id == user_id:
        child.first_name = request.json.get("first_name", child.first_name)
        child.last_name = request.json.get("last_name", child.last_name)
        db.session.commit()
        return ChildSchema().dump(child), 200 
    
    else:
        raise ValidationError(
            "You are not authorised to access this resource", 401
        )
    
# DELETE Child
@children_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_child(id):
    user_id = get_jwt_identity()
    user_type = user_status(user_id)
    child = db.get_or_404(Child, id)
    
    if user_type == "Admin" or child.user_id == user_id:
        db.session.delete(child)
        db.session.commit()
        return {"Success": "Child registration deleted"}, 200
    else:
        raise ValidationError(
            "You are not authorised to access this resource", 403
        )
