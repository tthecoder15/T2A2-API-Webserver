"""
    Contains blueprint formatting, functions and endpoints for "Child", "Comment" and "Attendance" entities.
"""

from datetime import datetime
from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.child import Child, ChildSchema
from models.comment import Comment, CommentSchema
from models.contact import Contact
from models.attendance import Attendance, AttendanceSchema
from models.user import User
from init import db
from auth import user_status

# Initialises flask Blueprint class "children_bp"
# Defines url prefix for endpoints defined in with @children_bp wrapper
children_bp = Blueprint("child", __name__, url_prefix="/children")


# GET Children
# wrapper links function "get_children" to endpoint "/children" when request is made with GET method
@children_bp.route("/", methods=["GET"])
# Mandates a JWT for requests to this endpoint
@jwt_required()
def get_children():
    """Returns multiple child tuples based on user permissions.
    Endpoint for "GET" "/children"
    """
    user_id = get_jwt_identity()
    # Creates local variable storing "Admin", "Parent" or "Teacher" for later permission checks
    user_type = user_status(user_id)

    # If user is an "Admin"
    # A database query selecting all "child" instances is submitted
    # Returned SQLAlchemy objects are converted to dictionaries via marshmallow
    # Thenreturned to the user
    if user_type == "Admin":
        stmt = db.select(Child)
        children = db.session.scalars(stmt).all()
        return ChildSchema(many=True).dump(children)

    # If user is a "Parent"
    # A database query selecting all "child" instances with a matching "user_id" is submitted
    # Returned SQLAlchemy objects are converted to dictionaries via marshmallow
    # Then returned to the user
    if user_type == "Parent":
        stmt = db.select(Child).where(Child.user_id == user_id)
        registered_children = db.session.scalars(stmt).all()
        return ChildSchema(many=True).dump(registered_children)

    # If the user is not an "Admin" or "Parent" an error message is returned
    else:
        return {"Error": "You are not authorised to access this resource"}, 403


# GET Child
@children_bp.route("/<int:id>", methods=["GET"])
@jwt_required()
def get_child(id):
    """Returns single child instance provided user has appropriate permissions.
    Endpoint for "GET" "/children/<int>".
    """
    user_id = get_jwt_identity()
    # Creates local variable storing "Admin", "Parent" or "Teacher" for later permission checks
    user_type = user_status(user_id)
    # The database is queried for a "child" instance with an "id" value matching the id value submitted in the URI
    # If no matches are found, a 404 error is raised
    child = db.get_or_404(Child, id)
    # A returned SQLAlchemy object is converted to a dictionary via marshmallow
    child_dict = ChildSchema().dump(child)

    # If the user is an "Admin", the dictionary is returned
    # If the user is not an "Admin", the child's "user_id" value must equal the id passed in the JWT
    if user_type == "Admin" or child_dict["user_id"] == user_id:
        return child_dict
    # If the user is not an "Admin" or the JWT id does not match the child_id value, an error is returned
    else:
        return {"Error": "You are not authorised to access this resource"}, 403


# POST Child
@children_bp.route("/", methods=["POST"])
@jwt_required()
def register_child():
    """Generates child object and sends it to be recorded in the connected database.
    Endpoint for "POST" "/children".
    """
    user_id = get_jwt_identity()
    # Creates local variable storing "Admin", "Parent" or "Teacher" for later permission checks
    user_type = user_status(user_id)

    # If user is not an "Admin" or "Parent" user, a 403 error message is returned
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
    # "Admin" users must provide the "user_id" value for the child instance in the request body
    # If the user is an "Admin", a database query checks if the provided "user_id" exists
    # If no such user exists, an error is raised
    if user_type == "Admin":
        stmt = db.select(User).where(User.id == request.json["user_id"])
        user = db.session.scalar(stmt)
        if not user:
            return {
                "Error": "No such user. Please check 'user_id' matches a registered user"
            }, 400
        new_child.user_id = request.json["user_id"]
    # If the user is a "Parent", the SQLAlchemy object's "user_id" value is automatically assigned the JWT id
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
    # The submitted values are commited to the database
    db.session.commit()
    # The submitted instance data is returned as a dictionary
    return {
        "Success": ChildSchema(only=["first_name", "last_name", "user_id"]).dump(
            new_child
        )
    }, 201


# PATCH Child
@children_bp.route("/<int:id>", methods=["PATCH"])
@jwt_required()
def update_child(id):
    """Submits new values to update an existing child instance in the database.
    Endpoint for "PATCH" "/children/<int>".
    """
    user_id = get_jwt_identity()
    # Creates local variable storing "Admin", "Parent" or "Teacher" for later permission checks
    user_type = user_status(user_id)
    
    # The database is queried for a "child" instance with an "id" matching the one submitted in the URI
    # If no matches are found, a 404 error is raised
    child = db.get_or_404(Child, id)
    # Checks if the user is an "Admin" or the child is registered to the user
    if user_type == "Admin" or child.user_id == user_id:
        # If the request body contains a "first_name" value, it is capitalised
        if "first_name" in request.json:
            request.json["first_name"] = request.json["first_name"].capitalize()
        # If the request body contains a "last_name" value, it is capitalised
        if "last_name" in request.json:
            request.json["last_name"] = request.json["last_name"].capitalize()
        # Screens request body values via marshmallow schema and raises an error for invalid inputs
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
        # Changed child object is commited to the database
        db.session.commit()
        # All updated fields are returned
        return {"Updated fields": new_info}, 200
    # Error returned if user is not authorised to update child instance
    else:
        return {"Error": "You are not authorised to access this resource"}, 403


# DELETE Child
@children_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_child(id):
    """Deletes a child instance from the database with "id" value matching the URI submitted value. Endpoint for "DELETE" "/children/<int>"."""
    user_id = get_jwt_identity()
    # Creates local variable storing "Admin", "Parent" or "Teacher" for later permission checks
    user_type = user_status(user_id)
    # The database is queried for a "child" instance with an "id" value matching the submitted URI value
    # If no matches are found, a 404 error is raised
    child = db.get_or_404(Child, id)
    # If the user is an "Admin", the user's request is authorised to proceed
    # If the user is not an "Admin", the child instance's "user_id" value is compared to the id provided in the JWT
    # If the user is authorised, the instance is deleted from the database
    if user_type == "Admin" or child.user_id == user_id:
        db.session.delete(child)
        # The deletion is committed to the database
        db.session.commit()
        return {"Success": "Child registration deleted"}, 200
    # If the user is not authorised, an error message is returned
    else:
        return {"Error": "You are not authorised to access this resource"}, 403


# GET Comments about child
@children_bp.route("/<int:id>/comments", methods=["GET"])
@jwt_required()
def get_child_comments(id):
    """Returns child data and comments linked to them via foreign key. Endpoint for "GET" "/children/<int>/comments"."""
    user_id = get_jwt_identity()
    # Creates local variable storing "Admin", "Parent" or "Teacher" for later permission checks
    user_type = user_status(user_id)
    # The database is queried for a "child" instance with an "id" value matching the submitted URI value
    # If no matches are found, a 404 error is raised
    child = db.get_or_404(Child, id)
    # Converts the retrieved child SQLAlchemy object to a dict via marshmallow schema
    # Only intakes values in the schema
    child_dict = ChildSchema(
        only=["user_id", "first_name", "last_name", "comments"]
    ).dump(child)
    # Checks if the user is authorised to retrieve the data
    # If the user is an "Admin" or "Teacher" or the child's "user_id" value matches the JWT id value, the dict is returned
    if (
        user_type == "Admin"
        or user_type == "Teacher"
        or child_dict["user_id"] == user_id
    ):
        return child_dict
    # If the user is not authorised, an error message is returned
    else:
        return {"Error": "You are not authorised to access this resource"}, 403


# GET Comment single about child
@children_bp.route("/<int:id>/comments/<int:id2>", methods=["GET"])
@jwt_required()
def get_comment(id, id2):
    """Returns single comment. Endpoint for "GET" "/children/<int>/comments/<int>"."""
    user_id = get_jwt_identity()
    # Creates local variable storing "Admin", "Parent" or "Teacher" for later permission checks
    user_type = user_status(user_id)
    # The database is queried for a "comment" with a "child_id" value matching id and a "comment_id" value matching id2
    stmt = db.select(Comment).where(Comment.child_id == id, Comment.comment_id == id2)
    comment = db.session.scalar(stmt)
    # Checks if a comment matching the URI-input id values is in the database or returns a 404 error
    if comment:
        # Converts the retrieved comment SQLAlchemy object to a dict via marshmallow schema
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
        # If the user is an "Admin" or "Teacher" or the child's "user_id" value matches the JWT id value, the dict is returned
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
    """Submits comment instance to be recorded in the database. Endpoint for "POST" "/children/<int>/comments"."""
    user_id = get_jwt_identity()
    # Creates local variable storing "Admin", "Parent" or "Teacher" for later permission checks
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


# PATCH Comment about child
@children_bp.route("/<int:id>/comments/<int:id2>", methods=["PATCH"])
@jwt_required()
def update_comment(id, id2):
    """Submits new values to update an existing comment instance in the database. Endpoint for "PATCH" "/children/<int>/comments/int"."""
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
    """Deletes a comment instance from the database. Endpoint for "DELETE" "/children/<int>/comments/int"."""
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
# GET child's attendances
@children_bp.route("/<int:id>/attendances", methods=["GET"])
@jwt_required()
def get_child_attendances(id):
    """Returns attendance instances with "child_id" matching URI input id value. Endpoint for "GET" "/children/<int>/attendances"."""
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


# GET child's single attendance
@children_bp.route("/<int:id>/attendances/<int:id2>", methods=["GET"])
@jwt_required()
def get_attendance(id, id2):
    """Returns single attendance as a dictionary. Endpoint for "GET" "/children/<int>/attendances/<int>"."""
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


# POST child's attendance
@children_bp.route("/<int:id>/attendances", methods=["POST"])
@jwt_required()
def post_attendance(id):
    """Submits attendance instance to be recorded in the database. Endpoint for "POST" "/children/<int>/attendances"."""
    user_id = get_jwt_identity()
    # Creates local variable storing "Admin", "Parent" or "Teacher" for later permission checks
    user_type = user_status(user_id)
    # If the user is a parent, checks if the child and contact submitted are both registered to them
    if user_type == "Parent":
        child = db.get_or_404(Child, id)
        if child.user_id != user_id:
            return {"Error": "You are not authorised to access this resource"}, 403
        contact = db.get_or_404(Contact, request.json["contact_id"])
        if contact.user_id != user_id:
            return {
                "Error": "Please enter a contact_id registered to your account"
            }, 400
    # If the user is a teacher, they are not permitted to generate attendances
    elif user_type == "Teacher":
        return {"Error": "You are not authorised to access this resource"}, 403
    # Check for same child attending same group in DB
    # If the child is already registered, an error is raised
    stmt = db.select(Attendance).where(
        Attendance.child_id == id, Attendance.group_id == request.json["group_id"]
    )
    attendance_exists = db.session.scalar(stmt)
    if attendance_exists:
        return {"Error": "Child attendance is already registered for that group"}, 400
    # Creates Attendance SQLAlchemy object prepared for submission
    new_attendance = Attendance(
        group_id=request.json["group_id"],
        contact_id=request.json["contact_id"],
        child_id=id,
    )
    # Submits attendance instance to the database
    db.session.add(new_attendance)
    db.session.commit()
    return {"Success": AttendanceSchema().dump(new_attendance)}, 201


# PATCH child's attendance
@children_bp.route("/<int:id>/attendances/<int:id2>", methods=["PATCH"])
@jwt_required()
def update_attendance(id, id2):
    """Submits new values to update an existing attendance instance in the database. Endpoint for "PATCH" "/children/<int>/attendances/<int>"."""
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
    """Deletes an attendance from the database. Endpoint for "DELETE" "/children/<int>/attendances/<int>"."""
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
