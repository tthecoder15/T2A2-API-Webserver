from datetime import datetime
from flask import Blueprint, request
from models.child import Child, ChildSchema
from models.comment import Comment, CommentSchema
from models.user import User
from init import db
from marshmallow.exceptions import ValidationError
from auth import user_status
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
def register_child():
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
            return {"Error": "No such user. Please check 'user_id' matches a registered user"}, 400
        new_child.user_id = request.json["user_id"]

    elif user_type == "Parent":
        new_child.user_id = user_id

    # Check if child with the same f/l_name & user_id is in database already
    stmt = db.select(Child).where(
        Child.first_name == new_child.first_name,
        Child.last_name == new_child.last_name,
        Child.user_id == new_child.user_id,
    )

    child = db.session.scalar(stmt)
    if child:
        return {"Error": "This child is already registered to this user"}, 400

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

    new_info = ChildSchema(
        only=["first_name", "last_name"],
        unknown="exclude",
    ).load(request.json)
    if new_info == {}:
        return {"Error": "Please provide at least one value to update"}, 400

    if user_type == "Admin" or child.user_id == user_id:
        child.first_name = request.json.get("first_name", child.first_name)
        child.last_name = request.json.get("last_name", child.last_name)
        db.session.commit()
        return ChildSchema().dump(child), 200

    else:
        raise ValidationError("You are not authorised to access this resource", 401)


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
        raise ValidationError("You are not authorised to access this resource", 403)


# READ Comments about child
@children_bp.route("/<int:id>/comments", methods=["GET"])
@jwt_required()
def get_child_comments(id):
    user_id = get_jwt_identity()
    user_type = user_status(user_id)

    child = db.get_or_404(Child, id)
    child_dict = ChildSchema(
        only=["user_id", "first_name", "last_name", "comments"]
    ).dump(child)

    if (
        user_type == "Admin"
        or user_type == "Teacher"
        or child_dict["user_id"] == user_id
    ):
        return child_dict
    else:
        raise ValidationError(
            "You must are not authorised to access this resource", 403
        )


# READ Comment single about child
@children_bp.route("/<int:id>/comments/<int:id2>", methods=["GET"])
@jwt_required()
def get_comment(id, id2):

    user_id = get_jwt_identity()
    user_type = user_status(user_id)

    comment = db.get_or_404(Comment, id2)
    comment_dict = CommentSchema().dump(comment)

    if (
        user_type == "Admin"
        or user_type == "Teacher"
        or comment_dict["user"]["id"] == user_id
    ):
        return comment_dict
    else:
        raise ValidationError(
            "You must are not authorised to access this resource", 403
        )


# CREATE Comment about child
@children_bp.route("/<int:id>", methods=["POST"])
@jwt_required()
def post_comment(id):
    user_id = get_jwt_identity()
    user_type = user_status(user_id)

    if user_type == "Parent":
        child = db.get_or_404(Child, id)
        child_dict = ChildSchema().dump(child)

        if child_dict["user_id"] != user_id:
            raise ValidationError(
                "You must are not authorised to access this resource", 403
            )

    comment_info = CommentSchema(only=["message", "urgency"], unknown="exclude").load(
        request.json
    )
    new_comment = Comment(
        message=comment_info["message"],
        urgency=comment_info["urgency"],
        user_id=user_id,
        child_id=id,
        date_created=datetime.now().date(),
    )

    db.session.add(new_comment)
    db.session.commit()
    return {"Success": CommentSchema().dump(new_comment)}, 201


# UPDATE Comment about child
@children_bp.route("/<int:id>/comments/<int:id2>", methods=["PATCH"])
@jwt_required()
def update_comment(id, id2):
    user_id = get_jwt_identity()

    new_info = CommentSchema(
        only=["message", "urgency"],
        unknown="exclude",
    ).load(request.json)
    if new_info == {}:
        return {"Error": "Please provide at least one value to update"}, 400

    comment = db.get_or_404(Comment, id2)
    comment_dict = CommentSchema().dump(comment)

    if comment_dict["user"]["id"] == user_id:
        comment.message = request.json.get("message", comment.message)
        comment.urgency = request.json.get("urgency", comment.urgency)
        comment.comment_edited = True
        comment.date_edited = datetime.now().date()
        db.session.commit()
        return CommentSchema().dump(comment), 200
    else:
        raise ValidationError(
            "You must are not authorised to access this resource", 403
        )


# DELETE Comment about child
@children_bp.route("/<int:id>/comments/<int:id2>", methods=["DELETE"])
@jwt_required()
def delete_comment(id, id2):

    user_id = get_jwt_identity()
    user_type = user_status(user_id)

    comment = db.get_or_404(Comment, id2)
    comment_dict = CommentSchema().dump(comment)
    if user_type == "Admin" or comment_dict["user"]["id"] == user_id:
        db.session.delete(comment)
        db.session.commit()
        return {"Success": "Comment deleted"}, 200
    else:
        raise ValidationError(
            "You must are not authorised to access this resource", 403
        )
