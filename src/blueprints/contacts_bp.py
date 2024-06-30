"""
    Contains blueprint formatting, functions and endpoints for "Contact" entities
"""

from flask import Blueprint, request
from models.contact import Contact, ContactSchema
from init import db
from auth import user_status
from flask_jwt_extended import jwt_required, get_jwt_identity

# Initialises flask Blueprint class "contact_bp" and defines url prefix for endpoints defined in with @contacts_bp wrapper
contacts_bp = Blueprint("contact", __name__, url_prefix="/contacts")


# GET Contacts
# Wrapper links function "get_contacts" to endpoint "/contacts" when request is made with GET method
@contacts_bp.route("/", methods=["GET"])
# Used throughout module, ensures JWT token is sent in request header
@jwt_required()
def get_contacts():
    """Returns multiple contact tuples based on user permissions.
    Endpoint for "GET" "/contacts".
    """
    user_id = get_jwt_identity()
    # Creates local variable storing "Admin", "Parent" or "Teacher" for later permission checks
    user_type = user_status(user_id)
    # If user is an "Admin" or "Teacher", a database query selecting all "contact" instances is submitted
    # Returned SQLAlchemy objects are converted to dictionaries via marshmallow and returned to the user
    if user_type == "Admin" or user_type == "Teacher":
        stmt = db.select(Contact)
        contacts = db.session.scalars(stmt).all()
        return ContactSchema(many=True).dump(contacts)
    # If user is a "Parent", a database query selecting all "contact" instances with a "user_id" matching the JWT id is submitted
    # Returned SQLAlchemy objects are converted to dictionaries via marshmallow and returned to the user
    if user_type == "Parent":
        stmt = db.select(Contact).where(Contact.user_id == user_id)
        registered_contacts = db.session.scalars(stmt).all()
        return ContactSchema(many=True).dump(registered_contacts)
    # If the user is not an "Admin" or "Parent" an error message is returned
    else:
        return {"Error": "You are not authorised to access this resource"}, 403


# GET Contact
@contacts_bp.route("/<int:id>", methods=["GET"])
@jwt_required()
def get_contact(id):
    """Returns single child instance provided user has appropriate permissions.
    Endpoint for "GET" "/contacts/<int>".
    """
    # The database is queried for a "contact" instance with an "id" value matching the submitted URI value
    # If no matches are found, a 404 error is raised
    contact = db.get_or_404(Contact, id)
    # A returned SQLAlchemy object is converted to a dictionary via marshmallow
    contact_dict = ContactSchema().dump(contact)
    user_id = get_jwt_identity()
    # Creates local variable storing "Admin", "Parent" or "Teacher" for later permission checks
    user_type = user_status(user_id)

    # If the user is an "Admin" or "Teacher", the dictionary is returned
    # If the user is not an "Admin" or "Teacher", the dictionary's "user_id" value is compared to the user_id provided in the JWT
    if (
        user_type == "Admin"
        or user_type == "Teacher"
        or contact_dict["user_id"] == user_id
    ):
        return contact_dict
    # If the user is not an "Admin" or their JWT id does not match the requested contact, an error is returned
    else:
        return {"Error": "You are not authorised to access this resource"}, 403


# POST Contact
@contacts_bp.route("/", methods=["POST"])
@jwt_required()
def register_contact():
    """Generates contact object and sends it to be recorded in the connected database.
    Endpoint for "POST" "/contacts".
    """
    user_id = get_jwt_identity()
    # Creates local variable storing "Admin", "Parent" or "Teacher" for later permission checks
    user_type = user_status(user_id)
    # Checks if the user is an admin or parent or returns an error
    if user_type == "Admin" or user_type == "Parent":
        # Sanitises submitted "ph_number" value
        # If the number is submitted as an integer it is sometimes auto deleted
        # The check ensures a "0" begins the submitted phone number or adds it
        if str(request.json["ph_number"])[0] != "0":
            request.json["ph_number"] = "0" + str(request.json["ph_number"])
        # Generates a local contact dict witht he submitted request json
        # marshmallow schema screens these values for inappropriate values
        contact_info = ContactSchema(
            only=["first_name", "email", "emergency_contact", "ph_number"],
            unknown="exclude",
        ).load(request.json)
        # Creates a local Contact SQLAlchemy Group object
        new_contact = Contact(
            first_name=contact_info["first_name"].capitalize(),
            email=contact_info["email"],
            ph_number=request.json["ph_number"],
            emergency_contact=contact_info["emergency_contact"],
        )
        # Checks if the user is an admin
        # If they are, they must submit a "user_id" value in their request body
        # This operand checks if a user exists with that id
        # If they do, the contact's "user_id" value is assigned the request's value
        if user_type == "Admin":
            stmt = db.select(Contact).where(Contact.user_id == request.json["user_id"])
            user = db.session.scalar(stmt)
            if not user:
                return {
                    "Error": "No such user. Please check 'user_id' matches a registered user"
                }, 400
            new_contact.user_id = request.json["user_id"]
        # If the user is parent, the contact is assigned their JWT id as the "user_id" value
        elif user_type == "Parent":
            new_contact.user_id = user_id
        # Checks if a contact is already registered with this phone number to this user
        # Returns an error if so
        stmt = db.select(Contact).where(
            Contact.ph_number == new_contact.ph_number,
            Contact.user_id == new_contact.user_id,
        )
        contact = db.session.scalar(stmt)
        if contact:
            return {
                "Error": "A contact is already registered with this phone number"
            }, 400
        # Stages new contact for submission
        db.session.add(new_contact)
        # Commits new contact to the database
        db.session.commit()
        # Returns the new contact's dictionary
        return {"Success": ContactSchema().dump(new_contact)}, 201
    else:
        return {"Error": "You are not authorised to access this resource"}, 403


# UPDATE Contact
@contacts_bp.route("/<int:id>", methods=["PATCH"])
@jwt_required()
def update_contact(id):
    """Submits new values to update an existing contact instance.
    Endpoint for "PATCH" "/users/<int>".
    """
    user_id = get_jwt_identity()
    # Creates local variable storing "Admin", "Parent" or "Teacher" for later permission checks
    user_type = user_status(user_id)
    # Checks if a contact exists with the URI-submitted id value or returns a 404
    contact = db.get_or_404(Contact, id)
    # Checks if the user is an admin or the contact to be edited is registered to the user
    if user_type == "Admin" or contact.user_id == user_id:
        # Santises a submitted "ph_number" value to have a 0 at its start
        if "ph_number" in request.json and str(request.json["ph_number"])[0] != "0":
            request.json["ph_number"] = "0" + str(request.json["ph_number"])
        # If the request body contains a "first_name" value, it is capitalised
        if "first_name" in request.json:
            request.json["first_name"] = request.json["first_name"].capitalize()
        # If the request body contains an "emergency_contact" value, it is capitalised
        # This is to ensure it is an appropriate boolean later in the function
        if "emergency_contact" in request.json:
            request.json["emergency_contact"] = request.json[
                "emergenct_contact"
            ].capitalize()
        # Creates a local dict containing all submitted values to update
        # marshmallow screens the submitted values and returns an error if they are inappropriate
        new_info = ContactSchema(
            only=["first_name", "emergency_contact", "email", "ph_number"],
            unknown="exclude",
        ).load(request.json)
        # Returns 400 if request contains no values to update
        if new_info == {}:
            return {"Error": "Please provide at least one value to update"}, 400
        # Sets retrieved SQLAlchemy tuple "first_name" value to new provided value
        # If no value is provided, "first_name" value remains as it was
        contact.first_name = request.json.get("first_name", contact.first_name)
        contact.emergency_contact = str(
            request.json.get("emergency_contact", contact.emergency_contact)
        ) in ["True"]
        # Sets retrieved SQLAlchemy tuple "email" value to new provided value
        # If no value is provided, "email" value remains as it was
        contact.email = request.json.get("email", contact.email)
        # Sets retrieved SQLAlchemy tuple "ph_number" value to new provided value
        # If no value is provided, "ph_number" value remains as it was
        contact.ph_number = request.json.get("ph_number", contact.ph_number)
        # Commits changes to database
        db.session.commit()
        # Returns all values submitted to update
        return {"Updated fields": new_info}, 200
    else:
        return {"Error": "You are not authorised to access this resource"}, 403


# DELETE Contact
@contacts_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_contact(id):
    """Deletes a child instance from the database with "id" value matching the URI submitted value. Endpoint for "DELETE" "/children/<int>"."""
    user_id = get_jwt_identity()
    # Creates local variable storing "Admin", "Parent" or "Teacher" for later permission checks
    user_type = user_status(user_id)
    # Queries the database for a contact instance with "id" value matching the submitted URI value
    # If no matches are found, a 404 error is raised
    contact = db.get_or_404(Contact, id)
    # If the user is an "Admin", the user's request is authorised to proceed
    # If the user is not an "Admin", the contact instance's "user_id" value is compared to the id provided in the JWT
    # If the user is authorised, the instance is deleted from the database
    if user_type == "Admin" or contact.user_id == user_id:
        db.session.delete(contact)
        # The deletion is committed to the database
        db.session.commit()
        return {"Success": "Contact registration deleted"}, 200
    # If the user is not authorised, an error message is returned
    else:
        return {"Error": "You are not authorised to access this resource"}, 403
