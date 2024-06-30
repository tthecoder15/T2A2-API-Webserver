"""
    Contains blueprint formatting, functions and endpoints for "Teacher" entities
"""

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.teacher import Teacher, TeacherSchema
from init import db
from auth import admin_check

# Initialises flask Blueprint class "teachers_bp"
# Defines url prefix for endpoints defined in with @teachers_bp wrapper
teachers_bp = Blueprint("teacher", __name__, url_prefix="/teachers")


# GET Teachers
# Wrapper links function "get_teachers" to endpoint "/teacherss" when request is made with GET method
@teachers_bp.route("/", methods=["GET"])
@jwt_required()
def get_teachers():
    # Sets the user_id var to the id in the header JWT
    user_id = get_jwt_identity()
    # Checks if the user is an admin or returns a 403
    if admin_check(user_id):
        # Generates an SQL query selecting all teacher instances
        stmt = db.select(Teacher)
        # Submits query
        teachers = db.session.scalars(stmt).all()
        # Returns all teacher SQL objects as a JSON via marshmallow schema
        return TeacherSchema(many=True).dump(teachers)
    # If the user is not an admin, an error message is returned
    else:
        return {"Error": "You are not authorised to access this resource"}, 403


# GET Teacher
@teachers_bp.route("/<int:id>", methods=["GET"])
@jwt_required()
def get_teacher(id):
    """Returns single teacher instance provided user has appropriate permissions.
    Endpoint for "GET" "/teachers/<int>".
    """
    # The database is queried for a "teacher" instance with an "id" value matching the submitted URI value
    # If no matches are found, a 404 error is raised
    teacher = db.get_or_404(Teacher, id)
    # A returned SQLAlchemy object is converted to a dictionary via marshmallow
    teacher_dict = TeacherSchema().dump(teacher)
    # Assigns the JWT id to a local var
    user_id = get_jwt_identity()
    # If the user is an admin, the dict is returned
    if admin_check(user_id):
        return teacher_dict
    # An error is returned for unauthorised users
    else:
        return {"Error": "You are not authorised to access this resource"}, 403


# POST Teacher
@teachers_bp.route("/", methods=["POST"])
@jwt_required()
def register_teacher():
    """Generates teacher object and sends it to be recorded in the connected database.
    Endpoint for "POST" "/teachers".
    """
    # Sets the user_id var to the id in the header JWT
    user_id = get_jwt_identity()
    # Checks if the user is an admin or raises a 403
    if admin_check(user_id):
        # Generates a local teacher dict with the submitted request json
        # marshmallow schema screens these values for inappropriate values
        teacher_info = TeacherSchema(
            only=["first_name", "email"], unknown="exclude"
        ).load(request.json)
        # Creates a local Contact SQLAlchemy Teacher object
        # Sanitises the "first_name" value to be capital
        new_teacher = Teacher(
            first_name=teacher_info["first_name"].capitalize(),
            email=teacher_info["email"],
        )
        # Queries the database for a teacher registered with the submitted email
        stmt = db.select(Teacher).where(
            Teacher.first_name == new_teacher.first_name,
            Teacher.email == new_teacher.email,
        )
        registered_teacher = db.session.scalar(stmt)
        # If a teacher is already recorded with the submitted email, a 400 error is returned
        if registered_teacher:
            return {"Error": "A teacher is already registered with this email"}, 400
        # The newly generated teacher is staged and commited to the database
        db.session.add(new_teacher)
        db.session.commit()
        # Returns the saved group instance as a dictionary
        return {"Success": TeacherSchema().dump(new_teacher)}, 201
    # An error is returned for unauthorised users
    else:
        return {"Error": "You are not authorised to access this resource"}, 403


# PATCH Teacher
@teachers_bp.route("/<int:id>", methods=["PATCH"])
@jwt_required()
def update_teacher(id):
    """Submits new values to update an existing group instance.
    Endpoint for "PATCH" "/groups/<int>".
    """
    # Sets the user_id var to the id in the header JWT
    user_id = get_jwt_identity()
    # Sanitises a submitted "first_name" value to be capitalised
    if "first_name" in request.json:
        request.json["first_name"] = request.json["first_name"].capitalize()
    # If an email is submitted, it is checked against teacher recorded in the database
    # If an instance already uses the same email, a 400 error is returned
    if "email" in request.json:
        stmt = db.select(Teacher).where(Teacher.email == request.json["email"])
        registered_teacher = db.session.scalar(stmt)
        if registered_teacher:
            return {"Error": "A teacher is already registered with this email"}, 400
    # Creates a local dict containing all submitted values to update
    # marshmallow screens the submitted values and returns an error if they are inappropriate
    new_info = TeacherSchema(
        only=["email", "first_name"],
        unknown="exclude",
    ).load(request.json)
    # Returns 400 if the request contains no values to update
    if new_info == {}:
        return {"Error": "Please provide at least one value to update"}, 400
    # Checks if the user is an admin or raises a 403
    if admin_check(user_id):
        # Retrieves the teacher instance to update
        teacher = db.get_or_404(Teacher, id)
        # Sets retrieved SQLAlchemy tuple "first_name" value to new provided value
        # If no value is provided, "first_name" value remains as it was
        teacher.first_name = request.json.get(
            "first_name", teacher.first_name
        ).capitalize()
        # Sets retrieved SQLAlchemy tuple "email" value to new provided value
        # If no value is provided, "email" value remains as it was
        teacher.email = request.json.get("email", teacher.email)
        # Commits changes to the database
        db.session.commit()
        # Returns all values submitted to update
        return {"Updated fields": new_info}, 200
    else:
        return {"Error": "You are not authorised to access this resource"}, 403


# DELETE Teacher
@teachers_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_teacher(id):
    """Deletes a teacher instance from the database with "id" value matching the URI submitted value.
    Endpoint for "DELETE" "/teachers/<int>".
    """
    # Sets the user_id var to the id in the header JWT
    user_id = get_jwt_identity()
    # Checks if the user is an admin or returns a 403
    if admin_check(user_id):
        # Queries the database for a teacher instance with "id" value matching the submitted URI value
        # If no matches are found, a 404 error is raised
        teacher = db.get_or_404(Teacher, id)
        # Stages deleting the returned teacher
        db.session.delete(teacher)
        # The deletion is committed to the database
        db.session.commit()
        return {"Success": "Teacher registration deleted"}, 200
    # If the user is not authorised, an error message is returned
    else:
        return {"Error": "You are not authorised to access this resource"}, 403
