from flask import Blueprint, request
from models.contact import Contact, ContactSchema
from init import db
from auth import admin_check, user_status
from flask_jwt_extended import jwt_required, get_jwt_identity


contacts_bp = Blueprint("contact", __name__, url_prefix="/contacts")


# READ Contact
@contacts_bp.route("/", methods=["GET"])
@jwt_required()
def get_contacts():
    user_id = get_jwt_identity()

    if admin_check(user_id):
        stmt = db.select(Contact)
        contacts = db.session.scalars(stmt).all()
        return ContactSchema(many=True).dump(contacts)
    else:
        return{"Error": "You are not authorised to access this resource"}, 403 


@contacts_bp.route("/<int:id>", methods=["GET"])
@jwt_required()
def get_contact(id):
    contact = db.get_or_404(Contact, id)
    contact_dict = ContactSchema().dump(contact)
    user_id = get_jwt_identity()

    if admin_check(user_id):
        return contact_dict
    else:
        return {"Error": "You are not authorised to access this resource"}, 403


# CREATE Contact
@contacts_bp.route("/", methods=["POST"])
@jwt_required()
def register_contact():
    user_id = get_jwt_identity()
    user_type = user_status(user_id)
    if user_type == "Admin" or user_type == "Parent":

        # SANITISE: Check for 0 at start of ph number, accepts int or str now
        if str(request.json["ph_number"])[0] != "0":
            request.json["ph_number"] = "0" + str(request.json["ph_number"])

        contact_info = ContactSchema(
            only=["first_name", "email", "emergency_contact", "ph_number"],
            unknown="exclude",
        ).load(request.json)

        new_contact = Contact(
            first_name=contact_info["first_name"].capitalize(),
            email=contact_info["email"],
            ph_number=request.json["ph_number"],
            emergency_contact=contact_info["emergency_contact"],
        )

        if user_type == "Admin":
            stmt = db.select(Contact).where(Contact.user_id == request.json["user_id"])
            user = db.session.scalar(stmt)
            if not user:
                return {
                    "Error": "No such user. Please check 'user_id' matches a registered user"
                }, 400
            new_contact.user_id = request.json["user_id"]

        elif user_type == "Parent":
            new_contact.user_id = user_id

        # Check is a contact is already registered with this phone number to this user
        stmt = db.select(Contact).where(
            Contact.ph_number == new_contact.ph_number,
            Contact.user_id == new_contact.user_id,
        )
        contact = db.session.scalar(stmt)
        if contact:
            return {
                "Error": "A contact is already registered with this phone number"
            }, 400

        db.session.add(new_contact)
        db.session.commit()
        return {"Success": ContactSchema().dump(new_contact)}, 201
    else:
        return {"Error": "You are not authorised to access this resource"}, 403


# UPDATE Contact
@contacts_bp.route("/<int:id>", methods=["PATCH"])
@jwt_required()
def update_contact(id):
    user_id = get_jwt_identity()
    user_type = user_status(user_id)
    contact = db.get_or_404(Contact, id)

    if user_type == "Admin" or contact.user_id == user_id:
        # Sanitising ph_number to have 0 at the start
        if "ph_number" in request.json and str(request.json["ph_number"])[0] != "0":
            request.json["ph_number"] = "0" + str(request.json["ph_number"])
        
        if "first_name" in request.json:
            request.json["first_name"] = request.json["first_name"].capitalize()
        if "emergency_contact" in request.json:
            request.json["emergency_contact"] = request.json["emergenct_contact"].capitalize()
       
        new_info = ContactSchema(
            only=["first_name", "emergency_contact", "email", "ph_number"],
            unknown="exclude",
        ).load(request.json)

        # Returns 400 if no update values
        if new_info == {}:
            return {"Error": "Please provide at least one value to update"}, 400

        contact.first_name = request.json.get(
            "first_name", contact.first_name
        )
        contact.emergency_contact = str(
            request.json.get("emergency_contact", contact.emergency_contact)
        ) in ["True"]
        contact.email = request.json.get("email", contact.email)
        contact.ph_number = request.json.get("ph_number", contact.ph_number)
        db.session.commit()
        return {"Updated fields": new_info}, 200
    else:
        return {"Error": "You are not authorised to access this resource"}, 403


# DELETE Contact
@contacts_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_contact(id):
    user_id = get_jwt_identity()
    user_type = user_status(user_id)
    contact = db.get_or_404(Contact, id)
    if user_type == "Admin" or contact.user_id == user_id:
        db.session.delete(contact)
        db.session.commit()
        return {"Success": "Contact registration deleted"}, 200
    else:
        return {"Error": "You are not authorised to access this resource"}, 403
