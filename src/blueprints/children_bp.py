"""Contains blueprint and endpoints for "Children", "Comments" and "Attendances entities.
"""

from datetime import datetime
from flask import Blueprint, request
from models.child import Child, ChildSchema
from models.comment import Comment, CommentSchema
from models.attendance import Attendance, AttendanceSchema
from models.user import User
from init import db

from auth import user_status
from flask_jwt_extended import jwt_required, get_jwt_identity


children_bp = Blueprint("child", __name__, url_prefix="/children")


# READ Children
@children_bp.route("/", methods=["GET"])
@jwt_required()
def get_children():
    """Returns multiple child tuples based on user permissions. Endpoint for "GET" "/children".

    Parameters
    ----------
    JWT: _auth token_
        Required to request endpoint. Used to check user permissions.

    Returns
    -------
    dict: Dictionary containing child instance data.
        If user is an "Admin", all child instances are returned.
        If user is a "Parent", only child instances registered to the user are returned.

        Example:
        {
            [
                {
                    "id": 1,
                    "user_id": 3,
                    "first_name": "Kyle",
                    "last_name": "Johnston",
                    "attendances": [
                        {
                            "group": {
                                "group_name": "Koalas",
                                "day": "Thursday"
                            }
                        }
                    ],
                    "comments": [
                        {
                            "user": {
                                "first_name": "Bobby",
                                "id": 3
                            },
                            "date_created": "2024-06-28",
                            "urgency": "neutral",
                            "message": "Kyle slept poorly last night. He might not be energetic today."
                        },
                    ]
                }
            ]
        }

    dict: Dictionary describing a request error.
    If user is a "Teacher", an error is returned.
        Example:
        {
            "Error": "You are not authorised to access this resource"
        }

    int: A HTTP response code describing if the request was successful.
        Example:
            201
    """

    user_id = get_jwt_identity()
    # Creates local variable storing "Admin", "Parent" or "Teacher" for later permission checks
    user_type = user_status(user_id)

    # If user is an "Admin", a database query selecting all "child" instances is submitted
    # Returned SQLAlchemy objects are converted to dictionaries via marshmallow and returned to the user
    if user_type == "Admin":
        stmt = db.select(Child)
        children = db.session.scalars(stmt).all()
        return ChildSchema(many=True).dump(children)

    # If user is a "Parent", a database query selecting all "child" instances with a matching "user_id" is submitted
    # Returned SQLAlchemy objects are converted to dictionaries via marshmallow and returned to the user
    if user_type == "Parent":
        stmt = db.select(Child).where(Child.user_id == user_id)
        registered_children = db.session.scalars(stmt)
        return ChildSchema(many=True).dump(registered_children)

    # If the user is not an "Admin" or "Parent" an error message is returned
    else:
        return {"Error": "You are not authorised to access this resource"}, 403


# READ Child
@children_bp.route("/<int:id>", methods=["GET"])
@jwt_required()
def get_child(id):
    """Returns single child instance provided user has appropriate permissions. Endpoint for "GET" "/children/<int>".

    Parameters
    ----------
    id: _int_
        Passed in the URI, specifies which child to query based on the child's "id" value in the database.
    JWT: _auth token_
        Required to request endpoint. Used to check user permissions.

    Returns
    -------
    dict: Dictionary containing child instance data.
        If the user is an "Admin", the requested child data is returned.
        If the user is a "Parent", the child's "user_id" value are compared, if they match, the child data is returned.
        Example:
        {
            "id": 2,
            "user_id": 3,
            "first_name": "Jason",
            "last_name": "Wu",
            "attendances":
                [
                    {
                        "group": {
                            "group_name": "Joeys",
                            "day": "Thursday"
                        }
                    },
                ],
            "comments": []
        }

    dict: Dictionary describing a request error.
        Example:
        {
            "Error": "You are not authorised to access this resource"
        }

    int: A HTTP response code describing if the request was successful.
        Example:
            201
    """
    # The database is queried for a "child" instance with an "id" value matching the submitted URI value
    # If no matches are found, a 404 error is raised
    child = db.get_or_404(Child, id)
    # A returned SQLAlchemy object is converted to a dictionary via marshmallow
    child_dict = ChildSchema().dump(child)
    user_id = get_jwt_identity()
    # Creates local variable storing "Admin", "Parent" or "Teacher" for later permission checks
    user_type = user_status(user_id)
    # If the user is an "Admin", the dictionary is returned
    # If the user is not an "Admin", the dictionary's "user_id" value is compared to the user_id provided in the JWT
    if user_type == "Admin" or child_dict["user_id"] == user_id:
        return child_dict
    # If the user is not an "Admin" or their JWT id does not match the requested child, an error is returned
    else:
        return {"Error": "You are not authorised to access this resource"}, 403


# CREATE Child
@children_bp.route("/", methods=["POST"])
@jwt_required()
def register_child():
    """Submits child instance to be recorded in the database. Endpoint for "POST" "/children".

    Parameters
    ----------
    JWT: _auth token_
        Required to request endpoint. Used to check user permissions.

    user_id : _int_
        If the user is an "Admin", user must provide "user_id" value in the request body.
        If the user is a "Parent", "user_id" value is automatically taken from the provided JWT.
    first_name : _str_
        Passed in the request body, the value provided for the child instance's attribute "first_name".
    last_name : _str_
        Passed in the request body, the value provided for the child instance's attribute "last_name".

    Returns
    -------
    dict: Dictionary containing recorded child instance data.
        Example:
        {
            "Success": {
                "first_name": "Robin",
                "last_name": "Nolan",
                "user_id": 3
            }
        }

    dict: Dictionary describing a request error.
        Example:
        {
            "Error": "This child is already registered to this user""
        }

    int: A HTTP response code describing if the request was successful.
        Example:
            201
    """

    user_id = get_jwt_identity()
    # Creates local variable storing "Admin", "Parent" or "Teacher" for later permission checks
    user_type = user_status(user_id)

    # If user is not an "Admin" or "Parent" user, a 403 error message is returned.
    if user_type != "Admin" and user_type != "Parent":
        return {"Error": "You are not authorised to access this resource"}, 403

    # Creates a dictionary using the provided request body and a marshmallow schema that mirrors the database's "child" table
    child_info = ChildSchema(only=["first_name", "last_name"], unknown="exclude").load(
        request.json
    )
    # Creates a SQLAlchemy object using the values in the marshmallow-formatted dictionary
    # The provided values are capitalised to sanitise them
    new_child = Child(
        first_name=child_info["first_name"].capitalize(),
        last_name=child_info["last_name"].capitalize(),
    )

    # If the user is an "Admin", a database query checks if the provided "user_id" exists
    # "Admin" users must provide the "user_id" value for the child instance in the request body
    if user_type == "Admin":
        stmt = db.select(User).where(User.id == request.json["user_id"])
        user = db.session.scalar(stmt)
        if not user:
            return {
                "Error": "No such user. Please check 'user_id' matches a registered user"
            }, 400
        new_child.user_id = request.json["user_id"]

    # If the user is a "Parent", the SQLAlchemy object's "user_id" value is automatically assigned the user's
    elif user_type == "Parent":
        new_child.user_id = user_id

    # A database query checks if a child is already registered with the provided "first_name", "last_name" and "user_id" values
    # An error is returned if the child already exists
    stmt = db.select(Child).where(
        Child.first_name == new_child.first_name,
        Child.last_name == new_child.last_name,
        Child.user_id == new_child.user_id,
    )
    child = db.session.scalar(stmt)
    if child:
        return {"Error": "This child is already registered to this user"}, 400

    # The SQLAlchemy child object is submitted to the connected database
    db.session.add(new_child)
    db.session.commit()

    # The submitted instance data is returned as a dictionary
    return {
        "Success": ChildSchema(only=["first_name", "last_name", "user_id"]).dump(
            new_child
        )
    }, 201


# UPDATE Child
@children_bp.route("/<int:id>", methods=["PATCH"])
@jwt_required()
def update_child(id):
    """Submits new values to update an existing child instance in the database. Endpoint for "PATCH" "/children/<int>".

    Parameters
    ----------
    id: _int_
        Passed in the URI, specifies which child instance to update from the database.
    JWT: _auth token_
        Required to request endpoint. Used to check user permissions.

    first_name : _str_
        Passed in the request body, the value provided to update the child instance's attribute "first_name". Optional.
    last_name : _str_
        Passed in the request body, the value provided to update the child instance's attribute "last_name". Optional.

    Returns
    -------
    dict: Dictionary containing recorded child instance data.
        If the user is authorised to update the child instance, the new values are returned in a dict.
        Example:
        {
            "Updated fields": {
                "first_name": "Batman"
            }
        }

    dict: Dictionary describing a request error.
        If the request fails due to authentication or a request error, the error is described.
        Example:
        {
            "Error": "This child is already registered to this user""
        }

    int: A HTTP response code describing if the request was successful.
        Example:
            201
    """

    user_id = get_jwt_identity()
    # Creates local variable storing "Admin", "Parent" or "Teacher" for later permission checks
    user_type = user_status(user_id)
    # The database is queried for a "child" instance with an "id" value matching the submitted URI value
    # If no matches are found, a 404 error is raised
    child = db.get_or_404(Child, id)

    # If the user is an "Admin", a database query checks if the provided "user_id" exists
    # "Admin" users must provide the "user_id" value for the child instance in the request body
    if user_type == "Admin" or child.user_id == user_id:

        # If the request body contains a "first_name" value, it is capitalised
        # If the request body contains a "last_name" value, it is capitalised
        if "first_name" in request.json:
            request.json["first_name"] = request.json["first_name"].capitalize()
        if "last_name" in request.json:
            request.json["last_name"] = request.json["last_name"].capitalize()

        # Screens request body values via marshmallow schema
        # Records values that will be updated into "new_info" var as a dict
        new_info = ChildSchema(
            only=["first_name", "last_name"],
            unknown="exclude",
        ).load(request.json)
        # Asserts that at least one value to update was provided or returns error
        if new_info == {}:
            return {"Error": "Please provide at least one value to update"}, 400

        # Sets retrieved SQLAlchemy tuple "first_name" value to new provided value
        # If no value is provided, "first_name" value remains as it was
        child.first_name = request.json.get("first_name", child.first_name)
        # Sets retrieved SQLAlchemy tuple "last_name" value to new provided value
        # If no value is provided, "last_name" value remains as it was
        child.last_name = request.json.get("last_name", child.last_name)
        db.session.commit()
        return {"Updated fields": new_info}, 200

    # Error returned if user is not authorised to update child instance
    else:
        return {"Error": "You are not authorised to access this resource"}, 403


# DELETE Child
@children_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_child(id):
    """Delete a child instance from the database with "id" value matching the URI submitted value. Endpoint for "DELETE" "/children/<int>".

    Parameters
    ----------
    id: _int_
        Passed in the URI, specifies which child instance to delete from the database.
    JWT: _auth token_
        Required to request endpoint. Used to check user permissions.

    Returns
    -------
    dict: Dictionary describing the request's success.
        Example:
            {
                "Success": "Child registration deleted"
            }

    dict: Dictionary describing a request error.
        If the request fails due to an authentication or request error, the error is described.
        Example:
            {
                "Error": "No resource found"
            }

    int: A HTTP response code describing if the request was successful.
        Example:
            200
    """
    user_id = get_jwt_identity()
    # Creates local variable storing "Admin", "Parent" or "Teacher" for later permission checks
    user_type = user_status(user_id)
    # The database is queried for a "child" instance with an "id" value matching the submitted URI value
    # If no matches are found, a 404 error is raised
    child = db.get_or_404(Child, id)

    # If the user is an "Admin", the user's request is authorised to proceed
    # If the user is not an "Admin", the child instance's "user_id" value is compared to the user_id provided in the JWT
    # If the user is authorised, the instance is deleted from the database
    if user_type == "Admin" or child.user_id == user_id:
        db.session.delete(child)
        db.session.commit()
        return {"Success": "Child registration deleted"}, 200

    # If the user is not authorised, an error message is returned
    else:
        return {"Error": "You are not authorised to access this resource"}, 403


# READ Comments about child
@children_bp.route("/<int:id>/comments", methods=["GET"])
@jwt_required()
def get_child_comments(id):
    """Returns child data and comments linked to them via foreign key. Endpoint for "GET" "/children/<int>/comments".

    Parameters
    ----------
    id: _int_
        Passed in the URI, specifies which child to query based on the child's "id" value in the database.
    JWT: _auth token_
        Required to request endpoint. Used to check user permissions.

    Returns
    -------
    dict: Dictionary containing child instance and comment data.
        If user is an "Admin" or "Teacher, all comments about the child are returned.
        If user is a "Parent", if the child is registered to the user, all comments about the child are returned.

        Example:
        {
            "user_id": 4,
            "first_name": "Becky",
            "last_name": "Lou",
            "comments": [
                {
                "user": {
                    "first_name": "Jenny",
                    "id": 2
                },
                "date_created": "2024-06-28",
                "urgency": "urgent",
                "message": "Becky has fallen ill and needs picking up. I am attempting to contact now"
                }
            ]
        }

    dict: Dictionary describing a request error.
    If user is a "Parent" and the child's "user_id" value does not match the user's, an error is returned.
        Example:
        {
            "Error": "You are not authorised to access this resource"
        }

    int: A HTTP response code describing if the request was successful.
        Example:
            200
    """

    user_id = get_jwt_identity()
    # Creates local variable storing "Admin", "Parent" or "Teacher" for later permission checks
    user_type = user_status(user_id)
    # The database is queried for a "child" instance with an "id" value matching the submitted URI value
    # If no matches are found, a 404 error is raised
    child = db.get_or_404(Child, id)

    # Converts the retrieved child SQLAlchemy object to a dict via marshmallow schema
    # Only converts "user_id", "first_name", "last_name" and "comments" data
    child_dict = ChildSchema(
        only=["user_id", "first_name", "last_name", "comments"]
    ).dump(child)

    # Checks if the user is authorised to retrieve the data
    # If the user is an "Admin" or "Teacher" or the child's "user_id" value matches the user's "id" value, the dict is returned
    if (
        user_type == "Admin"
        or user_type == "Teacher"
        or child_dict["user_id"] == user_id
    ):
        return child_dict

    # If the user is not authorised, an error message is returned
    else:
        return {"Error": "You are not authorised to access this resource"}, 403


# READ Comment single about child
@children_bp.route("/<int:id>/comments/<int:id2>", methods=["GET"])
@jwt_required()
def get_comment(id, id2):
    """Returns single comment. Endpoint for "GET" "/children/<int>/comments/<int>".

    Parameters
    ----------
    id: _int_
        Passed in the URI, specifies the id value of the child whose comments are queried.
    id2: _int_
        Passed in the URI, the id value of the comment requested.
    JWT: _auth token_
        Required to request endpoint. Used to check user permissions.

    Returns
    -------
    dict: Dictionary containing child instance data.
        If user is an "Admin" or "Teacher, the comment is returned.
        If user is a "Parent", if the child is registered to the user, the comment is returned.

        Example:
        {
            "user": {
                "first_name": "Bobby",
                "id": 3
            },
            "comment_edited": false,
            "date_edited": null,
            "date_created": "2024-06-28",
            "urgency": "neutral",
            "message": "Kyle slept poorly last night. He might not be energetic today."
        }

    dict: Dictionary describing a request error.
    If user is a "Parent" and the child's "user_id" value does not match the user's, an error is returned.
        Example:
        {
            "Error": "You are not authorised to access this resource"
        }

    int: A HTTP response code describing if the request was successful.
        Example:
            200
    """

    user_id = get_jwt_identity()
    # Creates local variable storing "Admin", "Parent" or "Teacher" for later permission checks
    user_type = user_status(user_id)
    # The database is queried for a "comment" with a "child_id" value matching id and a "comment_id" value matching id2
    stmt = db.select(Comment).where(Comment.child_id == id, Comment.comment_id == id2)
    comment = db.session.scalar(stmt)

    # Checks if a comment matching the input id values is found or returns a 404 error
    if comment:

        # Converts the retrieved comment SQLAlchemy object to a dict via marshmallow schema
        # Only converts "user_id", "first_name", "last_name" and "comments" data
        comment_dict = CommentSchema(only=["child", "user", "comment_edited", "date_edited", "date_created", "urgency", "message"]).dump(comment)

        # Checks if the user is authorised to retrieve the data
        # If the user is an "Admin" or "Teacher" or the child's "user_id" value matches the user's "id" value, the dict is returned
        if (
            user_type == "Admin"
            or user_type == "Teacher"
            or comment_dict["user"]["id"] == user_id
        ):
            return comment_dict

        # If the user is not authorised, an error message is returned
        else:
            return {"Error": "You are not authorised to access this resource"}, 403

    else:
        return {"Error": "No resource found"}, 404


# CREATE Comment about child
@children_bp.route("/<int:id>/comments", methods=["POST"])
@jwt_required()
def post_comment(id):
    user_id = get_jwt_identity()
    user_type = user_status(user_id)

    if user_type == "Parent":
        child = db.get_or_404(Child, id)
        child_dict = ChildSchema().dump(child)

        if child_dict["user_id"] != user_id:
            return {"Error": "You are not authorised to access this resource"}, 403

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

    if "urgency" in request.json:
        request.json["urgency"] = request.json["urgency"].lower()

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
        return {"Error": "You are not authorised to access this resource"}, 403


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
        return {"Error": "You are not authorised to access this resource"}, 403


# Attendances
# READ child's attendances
@children_bp.route("/<int:id>/attendances", methods=["GET"])
@jwt_required()
def get_child_attendances(id):
    user_id = get_jwt_identity()
    user_type = user_status(user_id)

    child = db.get_or_404(Child, id)
    child_dict = ChildSchema(
        only=["user_id", "first_name", "last_name", "attendances"]
    ).dump(child)

    if (
        user_type == "Admin"
        or user_type == "Teacher"
        or child_dict["user_id"] == user_id
    ):
        return child_dict

    return {"Error": "You are not authorised to access this resource"}, 403


# READ child's single attendance
@children_bp.route("/<int:id>/attendances/<int:id2>", methods=["GET"])
@jwt_required()
def get_attendance(id, id2):

    user_id = get_jwt_identity()
    user_type = user_status(user_id)

    attendance = db.get_or_404(Attendance, id2)
    attendance_dict = AttendanceSchema().dump(attendance)

    if (
        user_type == "Admin"
        or user_type == "Teacher"
        or attendance_dict["child"]["user_id"] == user_id
    ):
        return attendance_dict

    return {"Error": "You are not authorised to access this resource"}, 403


# CREATE child's attendance
@children_bp.route("/<int:id>/attendances", methods=["POST"])
@jwt_required()
def post_attendance(id):
    user_id = get_jwt_identity()
    user_type = user_status(user_id)

    if user_type == "Parent":
        child = db.get_or_404(Child, id)
        child_dict = ChildSchema().dump(child)

        if child_dict["user_id"] != user_id:
            return {"Error": "You are not authorised to access this resource"}, 403

    elif user_type == "Teacher":
        return {"Error": "You are not authorised to access this resource"}, 403

    # Check for same child attending same group in DB
    stmt = db.select(Attendance).where(
        Attendance.child_id == id, Attendance.group_id == request.json["group_id"]
    )
    user = db.session.scalar(stmt)

    new_attendance = Attendance(
        group_id=request.json["group_id"],
        contact_id=request.json["contact_id"],
        child_id=id,
    )

    if user:
        return {"Error": "Child attendance is already registered for that group"}, 400

    db.session.add(new_attendance)
    db.session.commit()
    return {"Success": AttendanceSchema().dump(new_attendance)}, 201


# UPDATE child's attendance
@children_bp.route("/<int:id>/attendances/<int:id2>", methods=["PATCH"])
@jwt_required()
def update_attendance(id, id2):
    user_id = get_jwt_identity()

    if "group_id" not in request.json and "contact_id" not in request.json:
        return {"Error": "Please provide at least one value to update"}, 400

    attendance = db.get_or_404(Attendance, id2)
    attendance_dict = AttendanceSchema().dump(attendance)

    if attendance_dict["child"]["user_id"] == user_id:
        attendance.group_id = request.json.get("group_id", attendance.group_id)
        attendance.contact_id = request.json.get("contact_id", attendance.contact_id)
        db.session.commit()
        return AttendanceSchema().dump(attendance), 200
    else:
        return {"Error": "You are not authorised to access this resource"}, 403


# DELETE child's Attendance
@children_bp.route("/<int:id>/attendances/<int:id2>", methods=["DELETE"])
@jwt_required()
def delete_attendance(id, id2):

    user_id = get_jwt_identity()
    user_type = user_status(user_id)

    attendance = db.get_or_404(Attendance, id2)
    attendance_dict = AttendanceSchema().dump(attendance)
    if user_type == "Admin" or attendance_dict["child"]["user_id"] == user_id:
        db.session.delete(attendance)
        db.session.commit()
        return {"Success": "Attendance deleted"}, 200
    else:
        return {"Error": "You are not authorised to access this resource"}, 403
