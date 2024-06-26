from datetime import datetime
from flask import Blueprint, request
from models.group import Group, GroupSchema
from models.comment import Comment, CommentSchema
from models.user import User
from init import db
from marshmallow.exceptions import ValidationError
from auth import admin_check
from flask_jwt_extended import jwt_required, get_jwt_identity


groups_bp = Blueprint("group", __name__, url_prefix="/groups")


# READ Groups
@groups_bp.route("/", methods=["GET"])
@jwt_required()
def get_groups():
    user_id = get_jwt_identity()

    if admin_check(user_id):
        stmt = db.select(Group)
        groups = db.session.scalars(stmt).all()
        return GroupSchema(many=True).dump(groups)
    else:
        stmt = db.select(Group).where(Group.user_id == user_id)
        registered_groups = db.session.scalars(stmt)
        return GroupSchema(many=True).dump(registered_groups)


# READ Single Group
@groups_bp.route("/<int:id>", methods=["GET"])
@jwt_required()
def get_group(id):
    group = db.get_or_404(Group, id)
    group_dict = GroupSchema().dump(group)
    user_id = get_jwt_identity()

    if admin_check(user_id):
        return group_dict
    else:
        return {"Error": "You are not authorised to access this resource"}, 403


# CREATE Group
@groups_bp.route("/", methods=["POST"])
@jwt_required()
def register_group():
    user_id = get_jwt_identity()

    group_info = GroupSchema(only=["group_name", "day"], unknown="exclude").load(
        request.json
    )
    new_group = Group(
        group_name=group_info["group_name"].capitalize(),
        day=group_info["day"].capitalize(),
        teacher_id=int(request.json["teacher_id"]),
    )

    if admin_check(user_id):
        stmt = db.select(Group).where(
            Group.group_name == new_group.group_name,
            Group.day == new_group.day,
        )
        group = db.session.scalar(stmt)
        if group:
            return {
                "Error": "A group is already registered with this name and day"
            }, 400

        db.session.add(new_group)
        db.session.commit()
        return {"Success": GroupSchema().dump(new_group)}, 201

    else:
        return {"Error": "You are not authorised to access this resource"}, 403


# UPDATE Group
@groups_bp.route("/<int:id>", methods=["PATCH"])
@jwt_required()
def update_group(id):
    user_id = get_jwt_identity()

    new_info = GroupSchema(
        only=["group_name", "day"],
        unknown="exclude",
    ).load(request.json)

    if "teacher_id" in request.json:
        new_info["teacher_id"] = request.json["teacher_id"]

    if new_info == {}:
        return {"Error": "Please provide at least one value to update"}, 400

    if admin_check(user_id):
        group = db.get_or_404(Group, id)
        group.group_name = request.json.get("group_name", group.group_name).capitalize()
        group.day = request.json.get("day", group.day).capitalize()
        group.teacher_id = int(request.json.get(("teacher_id"), group.teacher_id))
        db.session.commit()
        return GroupSchema().dump(group), 200
    else:
        return {"Error": "You are not authorised to access this resource"}, 403


# DELETE Group
@groups_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_group(id):
    user_id = get_jwt_identity()
    if admin_check(user_id):
        group = db.get_or_404(Group, id)
        db.session.delete(group)
        db.session.commit()
        return {"Success": "Group registration deleted"}, 200
    else:
        return {"Error": "You are not authorised to access this resource"}, 403
