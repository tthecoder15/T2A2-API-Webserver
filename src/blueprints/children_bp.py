"""
    Contains blueprint formatting and endpoints for "Child", "Comment" and "Attendance" entities.
"""

from datetime import datetime
from flask import Blueprint, request
from models.child import Child, ChildSchema
from models.comment import Comment, CommentSchema
from models.contact import Contact
from models.attendance import Attendance, AttendanceSchema
from models.user import User
from init import db
from auth import user_status
from flask_jwt_extended import jwt_required, get_jwt_identity

# Initialises flask Blueprint class "children_bp" and defines url prefix for endpoints defined in with @children_bp wrapper
children_bp = Blueprint("child", __name__, url_prefix="/children")


# READ Children
# wrapper links function "get_children" to endpoint "/children" when request is made with GET method
@children_bp.route("/", methods=["GET"])
# mandates a JWT for requests to this endpoint
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

    Raises
    -------
    403 Forbidden, User Identity Known: If the user does not have authorisation to access a child instance.
    404 Not Found: If a child with the given "child_id" value does not exist.

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
        registered_children = db.session.scalars(stmt).all()
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

    Raises
    -------
    403 Forbidden, User Identity Known: If the user does not have authorisation to access the child instance.
    404 Not Found: If a child with the given "child_id" value does not exist.

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

    Raises
    -------
    403 Forbidden, User Identity Known: If the user does not have authorisation to register a child instance.
    404 Not Found: If a child with the given "child_id" value does not exist.

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

    Raises
    -------
    400 Bad Request: If the user's request does not contain any appropriate fields or values to update.
    403 Forbidden, User Identity Known: If the user does not have authorisation to access the child instance.
    404 Not Found: If a child with the given "child_id" value does not exist.

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
    """Deletes a child instance from the database with "id" value matching the URI submitted value. Endpoint for "DELETE" "/children/<int>".

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

    Raises
    -------
    403 Forbidden, User Identity Known: If the user does not have authorisation to access the child instance.
    404 Not Found: If a child with the given "child_id" value does not exist.

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

    Raises
    -------
    403 Forbidden, User Identity Known: If the user does not have authorisation to access the child instance.
    404 Not Found: If a child with the given "child_id" value does not exist.

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
        Passed in the URI, specifies the id value of the child whose comment is queried.
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

    Raises
    -------
    403 Forbidden, User Identity Known: If the user does not have authorisation to access the comment.
    404 Not Found: If a comment with the given "child_id" and "comment_id" values does not exist.

    """

    user_id = get_jwt_identity()
    # Creates local variable storing "Admin", "Parent" or "Teacher" for later permission checks
    user_type = user_status(user_id)
    # The database is queried for a "comment" with a "child_id" value matching id and a "comment_id" value matching id2
    stmt = db.select(Comment).where(Comment.child_id == id, Comment.comment_id == id2)
    comment = db.session.scalar(stmt)

    # Checks if a comment matching the URI-input id values is in the database or returns a 404 error
    if comment:

        # Converts the retrieved comment SQLAlchemy object to a dict via marshmallow schema
        # Only converts "user_id", "first_name", "last_name" and "comments" data
        comment_dict = CommentSchema(
            only=[
                "child",
                "user",
                "comment_edited",
                "date_edited",
                "date_created",
                "urgency",
                "message",
            ]
        ).dump(comment)

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

    # Error message returned if no comment matches the input child id and comment id values
    else:
        return {"Error": "No resource found"}, 404


# CREATE Comment about child
@children_bp.route("/<int:id>/comments", methods=["POST"])
@jwt_required()
def post_comment(id):
    """Submits comment instance to be recorded in the database. Endpoint for "POST" "/children/<int>/comments".

    Parameters
    ----------
    id: _int_
        Passed in the URI, specifies the id value of the child linked to the comment.
    JWT: _auth token_
        Required to request endpoint. Used to check user permissions.

    message : _str_
        The string recorded as the comment's "message" attribute.
    urgency : _str_
        Passed in the request body, a string describing the quality of the comment.
        Must be one of "urgent", "positive", "neutral".

    Returns
    -------
    dict: Dictionary containing recorded comment instance data.
        Example:
        {
            "Success": {
                "child": {
                    "id": 1,
                    "first_name": "Kyle",
                    "last_name": "Johnston"
                },
                "user": {
                    "first_name": "Bobby",
                    "id": 3
                },
                "date_created": "2024-06-28",
                "urgency": "neutral",
                "message": "Kyle has an injured finger. He may be sensitive today"
            }
        }

    Raises
    -------
        403 Forbidden, User Identity Known: If the user does not have authorisation to post a comment about the child.
        404 Not Found: If a child with the given "id" value does not exist.

    """
    user_id = get_jwt_identity()
    user_type = user_status(user_id)

    # Confirms user's account type is "Parent"
    if user_type == "Parent":
        # Attempts to retrieve child instance with an "id" value matching input id or returns 404
        child = db.get_or_404(Child, id)
        # Checks if user's id equals the child instances "id" or returns 403 error
        if child.user_id != user_id:
            return {"Error": "You are not authorised to access this resource"}, 403

    # Screens any provided comment values via the marshmallow schema
    comment_info = CommentSchema(only=["message", "urgency"], unknown="exclude").load(
        request.json
    )
    # Creates SQLAlchemy object in new_comment var
    new_comment = Comment(
        message=comment_info["message"],
        urgency=comment_info["urgency"],
        user_id=user_id,
        child_id=id,
        date_created=datetime.now().date(),
    )
    # Submits new_comment SQLAlchemy object to database
    db.session.add(new_comment)
    db.session.commit()
    # Returns new comment data excluding "comment_edited" and "date_edited" values
    return {
        "Success": CommentSchema(exclude=["comment_edited", "date_edited"]).dump(
            new_comment
        )
    }, 201


# UPDATE Comment about child
@children_bp.route("/<int:id>/comments/<int:id2>", methods=["PATCH"])
@jwt_required()
def update_comment(id, id2):
    """Submits new values to update an existing comment instance in the database. Endpoint for "PATCH" "/children/<int>/comments/int".

    Parameters
    ----------
    id: _int_
        Passed in the URI, specifies the id value of the child whose comment is queried.
    id2: _int_
        Passed in the URI, the id value of the comment to update.
    JWT: _auth token_
        Required to request endpoint. Used to check user permissions.

    Returns
    -------
    dict: Dictionary containing updated comment data.
        "comment_edited" is automatically set to true after a successful "PATCH" request.
        "date_edited" is automatically set to the date of the most recent successful "PATCH" request.

        Example:
        {
            "child": {
                "id": 1,
                "first_name": "Kyle",
                "last_name": "Johnston"
            },
            "user": {
                "first_name": "Bobby",
                "id": 3
            },
            "comment_edited": true,
            "date_edited": "2024-06-28",
            "date_created": "2024-06-28",
            "urgency": "neutral",
            "message": "Kyle has an injured leg today. He may be flat"
        }

    Raises
    -------
    400 Bad Request: If the user's request does not contain any appropriate fields or values to update.
    403 Forbidden, User Identity Known: If the user does not have authorisation to access the comment instance.
    404 Not Found: If a comment with the given "child_id" and "comment_id" values does not exist.

    """

    user_id = get_jwt_identity()
    # The database is queried for a "comment" with a "child_id" value matching id and a "comment_id" value matching id2
    stmt = db.select(Comment).where(Comment.child_id == id, Comment.comment_id == id2)
    comment = db.session.scalar(stmt)

    # Confirms a comment was retrieved or returns a 404 error
    if comment:
        # Checks if an "urgency" attribute is in the request and makes it lowercase
        # This sanitises the data for the marshmallow model
        if "urgency" in request.json:
            request.json["urgency"] = request.json["urgency"].lower()

        # Screens any provided attribute values via the marshmallow schema
        new_info = CommentSchema(
            only=["message", "urgency"],
            unknown="exclude",
        ).load(request.json)

        # Asserts that at least one value to update was provided or returns error
        if new_info == {}:
            return {"Error": "Please provide at least one value to update"}, 400

        # Checks if the comment's "user_id" value matches the user who submitted the "PATCH" request
        if comment.user.id == user_id:
            # Sets retrieved tuple's "message" value to the new provided value
            # If no value is provided, "message" value remains as it was
            comment.message = request.json.get("message", comment.message)
            # Sets retrieved tuple's "urgency" value to the new provided value
            # If no value is provided, "urgency" value remains as it was
            comment.urgency = request.json.get("urgency", comment.urgency)
            # Sets retrieved tuple's "comment_edited" value to True
            comment.comment_edited = True
            # Sets retrieved tuple's "date_edited" value to the current date
            comment.date_edited = datetime.now().date()

            # The updated comment is submitted to the connected database
            db.session.commit()
            return CommentSchema().dump(comment), 200
        # If the comment's "user_id" value does not match the id value in the JWT token an error is returned
        else:
            return {"Error": "You are not authorised to access this resource"}, 403
    # Error message returned if no comment matches the input child id and comment id values
    else:
        return {"Error": "No resource found"}, 404


# DELETE Comment about child
@children_bp.route("/<int:id>/comments/<int:id2>", methods=["DELETE"])
@jwt_required()
def delete_comment(id, id2):
    """Deletes a comment instance from the database. Endpoint for "DELETE" "/children/<int>/comments/int".

    Parameters
    ----------
    id: _int_
        Passed in the URI, specifies the id value of the child whose comment is to be deleted.
    id2: _int_
        Passed in the URI, the id value of the comment to delete.
    JWT: _auth token_
        Required to request endpoint. Used to check user permissions.

    Returns
    -------
    dict: Dictionary confirming successful request.

        Example:
        {
            "Success": "Comment deleted"
        }

    Raises
    -------
    403 Forbidden, User Identity Known: If the user does not have authorisation to access the comment instance.
    404 Not Found: If a comment with the given "child_id" and "comment_id" values does not exist.
    """

    user_id = get_jwt_identity()
    # Creates local variable storing "Admin", "Parent" or "Teacher" for later permission checks
    user_type = user_status(user_id)
    # The database is queried for a "comment" with a "child_id" value matching id and a "comment_id" value matching id2
    stmt = db.select(Comment).where(Comment.child_id == id, Comment.comment_id == id2)
    comment = db.session.scalar(stmt)

    # Confirms a comment was retrieved or returns a 404 error
    if comment:
        # Checks if the comment's "user_id" value matches the user who submitted the "PATCH" request or the user is an "Admin"
        if user_type == "Admin" or comment.user.id == user_id:
            # Deletes comment instance and commits delete to database
            db.session.delete(comment)
            db.session.commit()
            # Returns successful deletion message
            return {"Success": "Comment deleted"}, 200
        # If the user is not authorised, an error message is returned
        else:
            return {"Error": "You are not authorised to access this resource"}, 403
    # Error message returned if no comment matches the input child id and comment id values
    else:
        return {"Error": "No resource found"}, 404


# Attendances
# READ child's attendances
@children_bp.route("/<int:id>/attendances", methods=["GET"])
@jwt_required()
def get_child_attendances(id):
    """Returns attendance instances with "child_id" matching URI input id value. Endpoint for "GET" "/children/<int>/attendances".

    Parameters
    ----------
    JWT: _auth token_
        Required to request endpoint. Used to check user permissions.
    id: _int_
        Passed in the URI, specifies the id value of the child whose comment is to be deleted.

    Returns
    -------
    dict: Dictionary containing all attendance instance data for submitted child_id.

        Example:
        [
            {
                "child_id": 1,
                "child": {
                    "id": 1,
                    "user_id": 3,
                    "first_name": "Kyle",
                    "last_name": "Johnston"
                },
                "group": {
                    "group_name": "Koalas",
                    "day": "Thursday"
                },
                "contact": {
                    "first_name": "Grandpa Joe",
                    "emergency_contact": false,
                    "ph_number": "0488111333",
                    "email": "No email provided"
                }
            }
        ]

    Raises
    -------
    403 Forbidden, User Identity Known: If the user does not have authorisation to access a child instance.
    404 Not Found: If no attendances with input the "child_id" value does not exist.

    """
    user_id = get_jwt_identity()
    # Creates local variable storing "Admin", "Parent" or "Teacher" for later permission checks
    user_type = user_status(user_id)
    # Queries database for attendances where the child_id is equal to the URI input id value
    stmt = db.select(Attendance).where(Attendance.child_id == id)
    attendances = db.session.scalars(stmt).all()
    # Checks if any attendances were returned and returns error if not
    if attendances:
        # Converts returned SQLAlchemy objects to a dict
        attendances_dict = AttendanceSchema(many=True).dump(attendances)
        # Checks if the user is authorised to access the dictionary data based on user type
        if (
            user_type == "Admin"
            or user_type == "Teacher"
            # Checks if first returned attendance's nested "child" instance has a "user_id" value equal to the requesting user's id
            or attendances_dict[0]["child"]["user_id"] == user_id
        ):
            # Returns a dictionary containing all attendances
            return attendances_dict
        else:
            # Returns an error if the user is not authorised
            return {"Error": "You are not authorised to access this resource"}, 403
    # Error message returned if no attendances have a child_id matching the URI input id value
    else:
        return {"Error": "No resource found"}, 404


# READ child's single attendance
@children_bp.route("/<int:id>/attendances/<int:id2>", methods=["GET"])
@jwt_required()
def get_attendance(id, id2):
    """Returns single attendance as a dictionary. Endpoint for "GET" "/children/<int>/attendances/<int>".

    Parameters
    ----------
    JWT: _auth token_
        Required to request endpoint. Used to check user permissions.
    id: _int_
        Passed in the URI, specifies the id value of the child whose attendances are queried.
    id2: _int_
        Passed in the URI, the id value of the attendance to query.

    Returns
    -------
    dict: Dictionary containing an attendance's data including child, group and contact instance data.

        Example:
        [
            {
                "child_id": 1,
                "child": {
                    "id": 1,
                    "user_id": 3,
                    "first_name": "Kyle",
                    "last_name": "Johnston"
                },
                "group": {
                    "group_name": "Koalas",
                    "day": "Thursday"
                },
                "contact": {
                    "first_name": "Grandpa Joe",
                    "emergency_contact": false,
                    "ph_number": "0488111333",
                    "email": "No email provided"
                }
            }
        ]

    Raises
    -------
    403 Forbidden, User Identity Known: If the user does not have authorisation to access the attendance instance.
    404 Not Found: If no attendances with input the "child_id" and "attendance_id" values does not exist.

    """
    user_id = get_jwt_identity()
    # Creates local variable storing "Admin", "Parent" or "Teacher" for later permission checks
    user_type = user_status(user_id)
    # The database is queried for an "attendance" with a "child_id" value matching id and an attendance "id" value matching id2
    stmt = db.select(Attendance).where(
        Attendance.child_id == id, Attendance.attendance_id == id2
    )
    attendance = db.session.scalar(stmt)
    # Confirms an attendance was retrieved or returns a 404 error
    if attendance:
        # Converts returned SQLAlchemy object to a dict
        attendance_dict = AttendanceSchema().dump(attendance)
        # Checks if the user is an "Admin", "Teacher" or the attendance's child user_id value equals the request user's
        if (
            user_type == "Admin"
            or user_type == "Teacher"
            or attendance_dict["child"]["user_id"] == user_id
        ):
            return attendance_dict

        return {"Error": "You are not authorised to access this resource"}, 403

    # Error message returned if no attendance matches the input child id and attendance id values
    else:
        return {"Error": "No resource found"}, 404


# CREATE child's attendance
@children_bp.route("/<int:id>/attendances", methods=["POST"])
@jwt_required()
def post_attendance(id):
    """Submits attendance instance to be recorded in the database. Endpoint for "POST" "/children/<int>/attendances".

    Parameters
    ----------
    id: _int_
        Passed in the URI, specifies the id value of the child linked to the comment.
    JWT: _auth token_
        Required to request endpoint. Used to check user permissions.

    group_id : _int_
        Passed in the request body, the group id value that describes which group the child attends
    contact_id : _int_
        Passed in the request body, the contact id value that describes the child's contact for the attendance.

    Returns
    -------
    dict: Dictionary containing successfully recorded attendance instance data.
        Example:
        {
            "Success": {
                    "attendance_id": 7,
                    "child_id": 1,
                    "child": {
                    "id": 1,
                    "user_id": 3,
                    "first_name": "Kyle",
                    "last_name": "Johnston"
                },
                "group": {
                    "group_name": "Joeys",
                    "day": "Thursday"
                },
                "contact": {
                    "first_name": "Joe",
                    "emergency_contact": false,
                    "ph_number": "0488111333",
                    "email": "No email provided"
                }
            }
        }

    Raises
    -------
        400 Bad Request: If the user submits an attendance that has the same child_id and group_id as one in the database or a user submits a contact not registered to their account.
        403 Forbidden, User Identity Known: If the user does not have authorisation to post an attendance for the child.
        404 Not Found: If a child with the given "id" value does not exist.

    """

    user_id = get_jwt_identity()
    user_type = user_status(user_id)

    if user_type == "Parent":
        child = db.get_or_404(Child, id)
        if child.user_id != user_id:
            return {"Error": "You are not authorised to access this resource"}, 403
        contact = db.get_or_404(Contact, request.json["contact_id"])
        if contact.user_id != user_id:
            return {
                "Error": "Please enter a contact_id registered to your account"
            }, 400

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
    """Submits new values to update an existing attendance instance in the database. Endpoint for "PATCH" "/children/<int>/attendances/<int>".

    Parameters
    ----------
    id: _int_
        Passed in the URI, specifies the id value of the child whose comment is queried.
    id2: _int_
        Passed in the URI, the id value of the attendance to update.
    JWT: _auth token_
        Required to request endpoint. Used to check user permissions.

    Returns
    -------
    dict: Dictionary containing updated and saved attendance data.
        Example:
        {
            "Success": {
                "attendance_id": 1,
                "child_id": 1,
                "child": {
                    "id": 1,
                    "user_id": 3,
                    "first_name": "Kyle",
                    "last_name": "Johnston"
                },
                "group": {
                    "group_name": "Koalas",
                    "day": "Thursday"
                },
                "contact": {
                    "first_name": "Bobby",
                    "emergency_contact": true,
                    "ph_number": "0488999444",
                    "email": "No email provided"
                }
            }
        }

    Raises
    -------
    400 Bad Request: If the user's request does not contain any appropriate fields or values to update.
    403 Forbidden, User Identity Known: If the user does not have authorisation to access the attendance instance.
    404 Not Found: If a comment with the given "child_id" and "comment_id" values does not exist.

    """

    user_id = get_jwt_identity()
    # Creates local variable storing "Admin", "Parent" or "Teacher" for later permission checks
    user_type = user_status(user_id)

    # Checks that at least one valid field is provided in the response body to update
    # If not, an error is returned
    if "group_id" not in request.json and "contact_id" not in request.json:
        return {"Error": "Please provide at least one value to update"}, 400

    # The database is queried for an "attendance" with a "child_id" value matching id and an attendance "id" value matching id2
    stmt = db.select(Attendance).where(
        Attendance.child_id == id, Attendance.attendance_id == id2
    )
    attendance = db.session.scalar(stmt)

    # Confirms an attendance was retrieved or returns a 404 error
    if attendance:
        # Converts returned SQLAlchemy object to a dict
        attendance_dict = AttendanceSchema().dump(attendance)

        # Checks if the attendance's child is registered to the user or the user is an admin or returns an error
        if attendance_dict["child"]["user_id"] == user_id or user_type == "Admin":
            # Sets the retrieved attendance's "group_id" value to the one provided in the request
            # If no new value is provided, it remains as it was
            attendance.group_id = request.json.get("group_id", attendance.group_id)
            # Sets the retrieved attendance's "contact_id" value to the one provided in the request
            # If no new value is provided, it remains as it was
            attendance.contact_id = request.json.get(
                "contact_id", attendance.contact_id
            )
            # Submits changes to the database and returns the complete attendance dict as submitted
            db.session.commit()
            return {"Success": AttendanceSchema().dump(attendance)}, 200
        # Error message is returned if the user is not authorised to update the attendance
        else:
            return {"Error": "You are not authorised to access this resource"}, 403

    # Error message returned if no attendance matches the input child id and attendance id values
    else:
        return {"Error": "No resource found"}, 404


# DELETE child's Attendance
@children_bp.route("/<int:id>/attendances/<int:id2>", methods=["DELETE"])
@jwt_required()
def delete_attendance(id, id2):
    """Deletes an attendance from the database. Endpoint for "DELETE" "/children/<int>/attendances/<int>".

    Parameters
    ----------
    id: _int_
        Passed in the URI, specifies the id value of the child whose comment is queried.
    id2: _int_
        Passed in the URI, the id value of the attendance to update.
    JWT: _auth token_
        Required to request endpoint. Used to check user permissions.

    Returns
    -------
    dict: Dictionary describing the request's success.
        Example:
            {
                "Success": "Attendance deleted"
            }

    Raises
    -------
    403 Forbidden, User Identity Known: If the user does not have authorisation to access the child instance.
    404 Not Found: If a child with the given "child_id" value does not exist.

    """
    user_id = get_jwt_identity()
    # Creates local variable storing "Admin", "Parent" or "Teacher" for later permission checks
    user_type = user_status(user_id)

    # The database is queried for an "attendance" with a "child_id" value matching id and an attendance "id" value matching id2
    stmt = db.select(Attendance).where(
        Attendance.child_id == id, Attendance.attendance_id == id2
    )
    attendance = db.session.scalar(stmt)

    # Confirms an attendance was retrieved or returns a 404 error
    if attendance:
        # Converts returned SQLAlchemy object to a dict to query user_id associated
        attendance_dict = AttendanceSchema().dump(attendance)

        # Checks if the attendance's child is registered to the user or the user is an admin or returns an error
        if attendance_dict["child"]["user_id"] == user_id or user_type == "Admin":
            # Deletes attendance and commits change to the database
            db.session.delete(attendance)
            db.session.commit()
            # Returns successful deletion message
            return {"Success": "Attendance deleted"}, 200
        # Error message is returned if the user is not authorised to update the attendance
        else:
            return {"Error": "You are not authorised to access this resource"}, 403

    # Error message returned if no attendance matches the input child id and attendance id values
    else:
        return {"Error": "No resource found"}, 404
