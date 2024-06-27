from flask import Blueprint, request
from models.teacher import Teacher, TeacherSchema
from init import db
from auth import admin_check
from flask_jwt_extended import jwt_required, get_jwt_identity


teachers_bp = Blueprint("teacher", __name__, url_prefix="/teachers")


# READ Teacher
@teachers_bp.route("/", methods=["GET"])
@jwt_required()
def get_teachers():
    user_id = get_jwt_identity()

    if admin_check(user_id):
        stmt = db.select(Teacher)
        teachers = db.session.scalars(stmt).all()
        return TeacherSchema(many=True).dump(teachers)
    else:
        return{"Error": "You are not authorised to access this resource"}, 403 


@teachers_bp.route("/<int:id>", methods=["GET"])
@jwt_required()
def get_teacher(id):
    teacher = db.get_or_404(Teacher, id)
    teacher_dict = TeacherSchema().dump(teacher)
    user_id = get_jwt_identity()

    if admin_check(user_id):
        return teacher_dict
    else:
        return{"Error": "You are not authorised to access this resource"}, 403


# CREATE Teacher
@teachers_bp.route("/", methods=["POST"])
@jwt_required()
def register_teacher():
    user_id = get_jwt_identity()
    if admin_check(user_id):    
        teacher_info = TeacherSchema(only=["first_name", "email"], unknown="exclude").load(
            request.json
        )

        new_teacher = Teacher(
            first_name=teacher_info["first_name"].capitalize(),
            email=teacher_info["email"],
        )

        # Check if a teacher is registered with this email
        stmt = db.select(Teacher).where(
            Teacher.first_name == new_teacher.first_name,
            Teacher.email == new_teacher.email,
        )
        registered_teacher = db.session.scalar(stmt)
        if registered_teacher:
            return{"Error": "A teacher is already registered with this email"}, 400

        db.session.add(new_teacher)
        db.session.commit()
        return {"Success": TeacherSchema().dump(new_teacher)}, 201

    else:
        return{"Error": "You are not authorised to access this resource"}, 403 
            

# UPDATE Teacher
@teachers_bp.route("/<int:id>", methods=["PATCH"])
@jwt_required()
def update_teacher(id):
    user_id = get_jwt_identity()

    if "first_name" in request.json:
        request.json["first_name"] = request.json["first_name"].capitalize()

    new_info = TeacherSchema(
        only=["email", "first_name"],
        unknown="exclude",
    ).load(request.json)

    if new_info == {}:
        return {"Error": "Please provide at least one value to update"}, 400

    if admin_check(user_id):
        teacher = db.get_or_404(Teacher, id)
        teacher.first_name = request.json.get(
            "first_name", teacher.first_name
        ).capitalize()
        teacher.email = request.json.get("email", teacher.email)
        db.session.commit()
        return {"Updated fields": new_info}, 200
    else:
        return{"Error": "You are not authorised to access this resource"}, 403 


# DELETE Teacher
@teachers_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_teacher(id):
    user_id = get_jwt_identity()
    if admin_check(user_id):
        teacher = db.get_or_404(Teacher, id)
        db.session.delete(teacher)
        db.session.commit()
        return {"Success": "Teacher registration deleted"}, 200
    else:
        return{"Error": "You are not authorised to access this resource"}, 403
