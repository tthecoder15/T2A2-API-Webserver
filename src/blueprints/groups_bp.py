"""
    Contains blueprint formatting, functions and endpoints for "Group" entities
"""

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.group import Group, GroupSchema
from init import db
from auth import admin_check, user_status

# Initialises flask Blueprint class "groups_bp" and defines url prefix for endpoints defined in with @groups_bp wrapper
groups_bp = Blueprint("group", __name__, url_prefix="/groups")


# GET Groups
# Wrapper links function "get_groups" to endpoint "/groups" when request is made with GET method
@groups_bp.route("/", methods=["GET"])
# Used throughout module, ensures JWT token is sent in request header
@jwt_required()
def get_groups():
    """Returns multiple group tuples based on user permissions.
    Endpoint for "GET" "/groups".
    """
    user_id = get_jwt_identity()
    # Creates local variable storing "Admin", "Parent" or "Teacher" for later permission checks
    user_type = user_status(user_id)
    # If user is an "Admin", "Teacher" or "Parent", a database query selecting all "group" instances is submitted
    # Returned SQLAlchemy objects are converted to dictionaries via marshmallow and returned to the user
    if user_type == "Admin" or user_type == "Teacher" or user_type == "Parent":
        stmt = db.select(Group)
        groups = db.session.scalars(stmt).all()
        return GroupSchema(many=True).dump(groups)
    # If the user is not an "Admin", "Teacher" or "Parent" an error message is returned
    else:
        return {"Error": "You are not authorised to access this resource"}, 403


# GET Single Group
@groups_bp.route("/<int:id>", methods=["GET"])
@jwt_required()
def get_group(id):
    """Returns single group instance provided user has appropriate permissions.
    Endpoint for "GET" "/groups/<int>".
    """
    # The database is queried for a "group" instance with an "id" value matching the submitted URI value
    # If no matches are found, a 404 error is raised
    group = db.get_or_404(Group, id)
    # A returned SQLAlchemy object is converted to a dictionary via marshmallow
    group_dict = GroupSchema().dump(group)

    user_id = get_jwt_identity()
    # Creates local variable storing "Admin", "Parent" or "Teacher" for later permission checks
    user_type = user_status(user_id)

    # If the user is an "Admin", "Teacher", or "Parent", the dictionary is returned
    if user_type == "Admin" or user_type == "Teacher" or user_type == "Parent":
        return group_dict
    # If the user is not an "Admin", "Teacher" or "Parent" an error message is returned
    else:
        return {"Error": "You are not authorised to access this resource"}, 403


# POST Group
@groups_bp.route("/", methods=["POST"])
@jwt_required()
def register_group():
    """Generates group object and sends it to be recorded in the connected database.
    Endpoint for "POST" "/groups".
    """
    # Sets the user_id var to the id in the header JWT
    user_id = get_jwt_identity()
    # Sanitises a submitted day variable to make it capital
    request.json["day"] = request.json["day"].capitalize()
    # Generates a local contact dict with the submitted request json
    # marshmallow schema screens these values for inappropriate values
    group_info = GroupSchema(only=["group_name", "day"], unknown="exclude").load(
        request.json
    )
    # Creates a local Contact SQLAlchemy Group object
    new_group = Group(
        group_name=group_info["group_name"].capitalize(),
        day=group_info["day"],
        teacher_id=int(request.json["teacher_id"]),
    )
    # Checks if the user is an admin
    # If they are not, the function returns a 403
    if admin_check(user_id):
        # Generates and submits a request to the database to see if a group with the submitted group name and day value exists
        # Checks if a group with the same group name and day already exists
        stmt = db.select(Group).where(
            Group.group_name == new_group.group_name,
            Group.day == new_group.day,
        )
        group = db.session.scalar(stmt)
        # If a group exists with these values, a 400 error is returned
        if group:
            return {
                "Error": "A group is already registered with this name and day"
            }, 400
        # Stages and commits new group to the database
        db.session.add(new_group)
        db.session.commit()
        # Returns the saved group instance as a dictionary
        return {"Success": GroupSchema().dump(new_group)}, 201

    else:
        return {"Error": "You are not authorised to access this resource"}, 403


# UPDATE Group
@groups_bp.route("/<int:id>", methods=["PATCH"])
@jwt_required()
def update_group(id):
    """Submits new values to update an existing group instance.
    Endpoint for "PATCH" "/groups/<int>".
    """
    # Sets the user_id var to the id in the header JWT
    user_id = get_jwt_identity()
    # Sanitises any submitted "group_name" or "day" values to be capitalised
    if "group_name" in request.json:
        request.json["group_name"] = request.json["group_name"].capitalize()
    if "day" in request.json:
        request.json["day"] = request.json["day"].capitalize()
    # Creates a local dict containing all submitted values to update
    # marshmallow screens the submitted values and returns an error if they are inappropriate
    new_info = GroupSchema(
        only=["group_name", "day"],
        unknown="exclude",
    ).load(request.json)
    # assigns a submitted "teacher_id" value to the data to be saved
    if "teacher_id" in request.json:
        new_info["teacher_id"] = request.json["teacher_id"]
    # Returns 400 if the request contains no values to update
    if new_info == {}:
        return {"Error": "Please provide at least one value to update"}, 400
    # Checks if the user is an admin
    # If not returns a 403
    if admin_check(user_id):
        # Checks if a group instance already exists with the same "group_name" and "day" values
        stmt = db.select(Group).where(
            Group.group_name == new_info["group_name"],
            Group.day == new_info["day"],
        )
        group = db.session.scalar(stmt)
        # Returns a 400 error if these values are already recorded to an instance
        if group:
            return {
                "Error": "A group is already registered with this name and day"
            }, 400
        # Retrieves the group instance to update
        group = db.get_or_404(Group, id)
        # Sets retrieved SQLAlchemy tuple "group_name" value to new provided value
        # If no value is provided, "group_name" value remains as it was
        group.group_name = request.json.get("group_name", group.group_name).capitalize()
        # Sets retrieved SQLAlchemy tuple "day" value to new provided value
        # If no value is provided, "day" value remains as it was
        group.day = request.json.get("day", group.day)
        # Sets retrieved SQLAlchemy tuple "teacher_id" value to new provided value
        # If no value is provided, "teacher_id" value remains as it was
        group.teacher_id = int(request.json.get(("teacher_id"), group.teacher_id))
        # Commits changes to the database
        db.session.commit()
        # Returns all values submitted to update
        return {"Updated fields": new_info}, 200
    else:
        return {"Error": "You are not authorised to access this resource"}, 403


# DELETE Group
@groups_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_group(id):
    """Deletes a group instance from the database with "id" value matching the URI submitted value.
    Endpoint for "DELETE" "/groups/<int>".
    """
    # Sets the user_id var to the id in the header JWT
    user_id = get_jwt_identity()
    # Checks if the user is an admin or returns a 403
    if admin_check(user_id):
        # Queries the database for a group instance with "id" value matching the submitted URI value
        # If no matches are found, a 404 error is raised
        group = db.get_or_404(Group, id)
        # Stages deleting the returned group
        db.session.delete(group)
        # The deletion is committed to the database
        db.session.commit()
        return {"Success": "Group registration deleted"}, 200
    # If the user is not authorised, an error message is returned
    else:
        return {"Error": "You are not authorised to access this resource"}, 403
