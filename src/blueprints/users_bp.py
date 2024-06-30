from datetime import timedelta
from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_jwt_extended import create_access_token
from models.user import User, UserSchema
from init import db, bcrypt
from auth import admin_check, user_status


# Initialises flask Blueprint class "users_bp"
# Defines url prefix for endpoints defined in with @users_bp wrapper
users_bp = Blueprint("user", __name__, url_prefix="/users")


# LOGIN
@users_bp.route("/login", methods=["POST"])
def login():
    """Returns JWT token if a user submits the correct credentials.
    Endpoint for "POST" "users/login".
    """
    # If the user submits a password shorter than 8 characters, a 400 error is returned
    if len(request.json["password"]) < 8:
        return {"Error": "Incorrect email or password"}, 400
    # Creates a local dict containing submitted login credentials
    # marshmallow screens the submitted values and returns an error if they are inappropriate
    params = UserSchema(only=["email", "password"]).load(
        request.json, unknown="exclude"
    )
    # Checks the database for a user with the provided email
    stmt = db.select(User).where(User.email == params["email"])
    user = db.session.scalar(stmt)
    # If a user with the submitted email exists
    # The submitted "password" value is hashed and compared to the recorded hashed password
    # If they are equal, the user is returned a JWT token
    if user and bcrypt.check_password_hash(user.password, params["password"]):
        token = create_access_token(identity=user.id, expires_delta=timedelta(hours=2))
        return {"token": token}
    # If a user with the email value does not exist or the password is incorrect
    # A 401 error is returned
    else:
        return {"Error": "Incorrect email or password"}, 401


# Get All Users
@users_bp.route("/", methods=["GET"])
@jwt_required()
def get_users():
    """Returns all user tuples if user has admin authentication.
    Endpoint for "GET" "/users".
    """
    # Sets the user_id var to the id in the header JWT
    user_id = get_jwt_identity()
    # Checks if the user is an admin or returns a 403
    if admin_check(user_id):
        # Generates an SQL query selecting all user instances
        stmt = db.select(User)
        # Submits query
        users = db.session.scalars(stmt).all()
        # Returns all user SQL objects as a JSON via marshmallow schema
        # Returned dict does not contain "password" values
        return UserSchema(many=True, exclude=["password"]).dump(users)
    # If the user is not an admin, an error message is returned
    else:
        return {"Error": "You are not authorised to access this resource"}, 403


# GET One User
@users_bp.route("/<int:id>", methods=["GET"])
@jwt_required()
def get_user(id):
    """Returns single user instance provided user is an admin.
    Endpoint for "GET" "/users/<int>".
    """
    user_id = get_jwt_identity()
    # Creates local variable storing "Admin", "Parent" or "Teacher" for later permission checks
    user_type = user_status(user_id)
    # If the user is an "Admin", the user's request is authorised to proceed
    if user_type == "Admin":
        # The database is queried for a "user" instance with an "id" value matching the submitted URI value
        # If no matches are found, a 404 error is raised
        user = db.get_or_404(User, id)
        # Returns a dict containing all user values except "password"
        return UserSchema(exclude=["password"]).dump(user)
    # Checks if the user is a parent or teacher user type
    if user_type == "Parent" or user_type == "Teacher":
        # The database is queried for a "user" instance with an "id" value matching the submitted URI value
        # If no matches are found, a 404 error is raised
        user = db.get_or_404(User, id)
        # Checks the returned user has the same "id" value as the requesting users JWT id
        if user.id == user_id:
            # Returns a dict containing all user values except "password", "is_admin" and "is_teacher"
            return UserSchema(exclude=["password", "is_admin", "is_teacher"]).dump(user)
        else:
            return {"Error": "You are not authorised to access this resource"}, 403
    else:
        return {"Error": "You are not authorised to access this resource"}, 403


# POST User, Admin Auth
@users_bp.route("/admin", methods=["POST"])
@jwt_required()
def create_user_admin():
    """Generates user object and sends it to be recorded in the connected database.
    Endpoint for users with admin authorisation.
    Allows user to submit "is_admin" and "is_teacher" values.
    Endpoint for "POST" "/users/admin".
    """
    user_id = get_jwt_identity()
    # Creates local variable storing "Admin", "Parent" or "Teacher" for later permission checks
    user_type = user_status(user_id)
    # Checks if the user is an admin or returns a 403 error
    if user_type == "Admin":
        # Queries the database for a user registered with the submitted email
        stmt = db.select(User).where(User.email == request.json["email"])
        user = db.session.scalar(stmt)
        # If a user is already recorded with the submitted email, a 400 error is returned
        if user:
            return {
                "Error": "Email already registered. Please provide a unique email address"
            }, 400
        # Generates a local user dict with the submitted request JSON
        # marshmallow schema screens these values for inappropriate values
        input_info = UserSchema(
            only=["email", "first_name", "password", "is_admin", "is_teacher"],
            unknown="exclude",
        ).load(request.json)
        # Creates a local Contact SQLAlchemy User object using submitted body JSON values
        # Hashes the provided "password" value
        # Sanitises the "first_name" value to be capital
        # Converts the "is_admin" and "is_teacher" to booleans
        new_user = User(
            email=input_info["email"],
            password=bcrypt.generate_password_hash(input_info["password"]).decode(
                "utf-8"
            ),
            first_name=input_info["first_name"].capitalize(),
            is_admin=str(input_info["is_admin"]).capitalize() in ["True"],
            is_teacher=str(input_info["is_teacher"]).capitalize() in ["True"],
        )
        # The newly generated user is staged and commited to the database
        db.session.add(new_user)
        db.session.commit()
        # Returns the saved User instance as a dictionary
        return {
            "Success": UserSchema(
                only=["email", "first_name", "is_admin", "is_teacher"]
            ).dump(new_user)
        }, 201
    # An error is returned for unauthorised users
    else:
        return {"Error": "You are not authorised to access this resource"}, 403


# POST User, no auth
@users_bp.route("/", methods=["POST"])
def create_user():
    """Generates user object and sends it to be recorded in the connected database.
    For users without an account yet and no authentication.
    Endpoint for "POST" "/users".
    """
    # Queries the database for a user registered with the submitted email
    stmt = db.select(User).where(User.email == request.json["email"])
    user = db.session.scalar(stmt)
    # If a user is already recorded with the submitted email, a 400 error is returned
    if user:
        return {
            "Error": "This email is already registered to a user. Please provide a unique email address"
        }, 400
    # Generates a local user dict with the submitted request JSON
    # marshmallow schema screens these values for inappropriate values
    input_info = UserSchema(
        only=["email", "first_name", "password"],
        unknown="exclude",
    ).load(request.json)
    # Creates a local Contact SQLAlchemy User object using submitted body JSON values
    # Hashes the provided "password" value
    # Sanitises the "first_name" value to be capital
    new_user = User(
        email=input_info["email"],
        password=bcrypt.generate_password_hash(input_info["password"]).decode("utf-8"),
        first_name=input_info["first_name"].capitalize(),
    )
    # The newly generated user is staged and commited to the database
    db.session.add(new_user)
    db.session.commit()
    # Returns the saved User instance as a dictionary
    return {"Success": UserSchema(only=["email", "first_name"]).dump(new_user)}, 201


# PATCH User
@users_bp.route("/<int:id>", methods=["PATCH"])
@jwt_required()
def update_user(id):
    """Submits new values to update an existing user instance in the database.
    Endpoint for "PATCH" "/users/<int>".
    """
    user_id = get_jwt_identity()
    # Creates local variable storing "Admin", "Parent" or "Teacher" for later permission checks
    user_type = user_status(user_id)
    # If an "email" value is present in the request body
    # The database is queried for a user with a matching email
    # A 400 error is returned if one exists
    if "email" in request.json:
        stmt = db.select(User).where(User.email == request.json["email"])
        user = db.session.scalar(stmt)
        if user:
            return {
                "Error": "This email is already registered to a user. Please provide a unique email address"
            }, 400
    # Sanitises a submitted "first_name" value to be capitalised
    if "first_name" in request.json:
        request.json["first_name"] = request.json["first_name"].capitalize()
    # Sanitises a submitted "is_admin" value to be capitalised
    if "is_admin" in request.json:
        request.json["is_admin"] = request.json["is_admin"].capitalize()
    # Sanitises a submitted "is_admin" value to be capitalised
    if "is_teacher" in request.json:
        request.json["is_teacher"] = request.json["is_teacher"].capitalize()
    # Creates a local dict containing all submitted values to update
    # marshmallow screens the submitted values and returns an error if they are inappropriate
    new_info = UserSchema(
        only=["email", "first_name", "is_admin", "is_teacher", "password"],
        unknown="exclude",
    ).load(request.json)
    # Returns 400 if the request contains no values to update
    if new_info == {}:
        return {"Error": "Please provide at least one value to update"}, 400
    # Retrieves the user instance to update
    user = db.get_or_404(User, id)
    # Checks if the user is an admin or the targeted user's id matches the JWT id
    if user_type == "Admin" or user.id == user_id:
        # Sets retrieved SQLAlchemy tuple "email" value to new provided value
        # If no value is provided, "email" value remains as it was
        user.email = request.json.get("email", user.email)
        # Sets retrieved SQLAlchemy tuple "first_name" value to new provided value
        # If no value is provided, "first_name" value remains as it was
        user.first_name = request.json.get("first_name", user.first_name)

        # Checks if password was contained in user request
        if "password" in request.json:
            # Hashes submitted "password value"
            new_password = bcrypt.generate_password_hash(
                request.json["password"]
            ).decode("utf-8")
            # Sets retrieved SQLAlchemy tuple "password" value to new provided value
            user.password = new_password
            # Updates new_info dict to note that password was updated
            new_info.update({"password": "Password successfully updated"})

        # Checks if the user is an admin
        if user_type == "Admin":
            # Sets retrieved SQLAlchemy tuple "is_admin" value to new provided value
            # If no value is provided, "is_admin" value remains as it was
            user.is_admin = str(request.json.get("is_admin", user.is_admin)) in ["True"]
            # Sets retrieved SQLAlchemy tuple "is_teacher" value to new provided value
            # If no value is provided, "is_teacher" value remains as it was
            user.is_teacher = str(request.json.get("is_teacher", user.is_teacher)) in [
                "True"
            ]
        # Commits changes to the database
        db.session.commit()
        # Checks if user is not admin
        # Removes "is_admin" or "is_teacher" from list of updates if user isn't admin
        if user_type != "Admin":
            if "is_admin" in new_info:
                new_info.pop("is_admin")
            if "is_teacher" in new_info:
                new_info.pop("is_teacher")
        # Returns all values submitted to update
        return {"Updated fields": new_info}, 200
    else:
        return {"Error": "You are not authorised to access this resource"}, 403


# DELETE User
@users_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_user(id):
    """Deletes a user instance from the database with "id" value matching the URI submitted value.
    Endpoint for "DELETE" "/users/<int>".
    """
    # Sets the user_id var to the id in the header JWT
    user_id = get_jwt_identity()
    # Assigns a local var the user's account type
    user_type = user_status(user_id)
    # Queries the database for a user instance with "id" value matching the submitted URI value
    # If no matches are found, a 404 error is raised
    user = db.get_or_404(User, id)
    # Checks if the user is an admin or returns a 403
    if user_type == "Admin":
        # Stages deleting the returned user
        db.session.delete(user)
        # The deletion is committed to the database
        db.session.commit()
        return {"Success": "User registration deleted"}, 200
    # If the user is not authorised, an error message is returned
    else:
        return {"Error": "You are not authorised to access this resource"}, 403
