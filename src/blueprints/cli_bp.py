from datetime import datetime
from flask import Blueprint
from init import db, bcrypt
from models.user import User
from models.child import Child
from models.comment import Comment
from models.teacher import Teacher
from models.contact import Contact
from models.group import Group
from models.attendance import Attendance

cli_commands = Blueprint("cli", __name__)


@cli_commands.cli.command("db_init")
def db_create():
    db.drop_all()
    db.create_all()
    print("Dropped then created tables!")
    users = [
        User(
            email="admin@childcare.com",
            password=bcrypt.generate_password_hash("admin123").decode("utf-8"),
            first_name="Admin",
            is_admin=True,
            is_teacher=False,
        ),
        User(
            email="jenny@childcare.com",
            password=bcrypt.generate_password_hash("jenny123").decode("utf-8"),
            first_name="Jenny",
            is_admin=False,
            is_teacher=True,
        ),
        User(
            email="bobby@spam.com",
            password=bcrypt.generate_password_hash("bobby123").decode("utf-8"),
            first_name="Bobby",
            is_admin=False,
            is_teacher=False,
        ),
        User(
            email="roberta@spam.com",
            password=bcrypt.generate_password_hash("roberta123").decode("utf-8"),
            first_name="Roberta",
            is_admin=False,
            is_teacher=False,
        ),
        User(
            email="nestle@spam.com",
            password=bcrypt.generate_password_hash("nestle123").decode("utf-8"),
            first_name="Nessie",
            is_admin=False,
            is_teacher=False,
        ),
    ]
    db.session.add_all(users)
    db.session.commit()
    print("Users are a go, roger roger")

    children = [
        Child(first_name="Kyle", last_name="Johnston", user_id=3),
        Child(first_name="James", last_name="Johnston", user_id=3),
        Child(first_name="Becky", last_name="Lou", user_id=4),
        Child(first_name="Milo", last_name="Swiss", user_id=5),
    ]
    db.session.add_all(children)
    db.session.commit()
    print("Children are registered!")

    comments = [
        Comment(
            message="Kyle had a big taco for lunch. He might not be hungry in the afternoon",
            urgency="neutral",
            date_created=datetime.now().date(),
            user_id=3,
            child_id=1,
        ),
        Comment(
            message="Thanks Bobby, that's noted.",
            urgency="neutral",
            date_created=datetime.now().date(),
            user_id=2,
            child_id=1,
        ),
        Comment(
            message="Becky has fallen ill and needs picking up. I am attempting to contact now",
            urgency="urgent",
            date_created=datetime.now().date(),
            user_id=2,
            child_id=3,
        ),
    ]
    db.session.add_all(comments)

    teachers = [
        Teacher(first_name="Jenny", email="jenny@childcare.com"),
        Teacher(first_name="Hutch", email="hutch@childcare.com"),
        Teacher(first_name="Rylo", email="Rylo@childcare.com"),
    ]
    db.session.add_all(teachers)

    contacts = [
        Contact(
            user_id=3,
            first_name="Bobby",
            ph_number="0488999444",
            emergency_contact=True,
        ),
        Contact(
            user_id=3,
            first_name="Grandpa Joe",
            ph_number="0488111333",
        ),
        Contact(
            user_id=4,
            first_name="Roberta",
            ph_number="0444433312",
            emergency_contact=True,
        ),
        Contact(
            user_id=5,
            first_name="Nessie",
            ph_number="0451696323",
            emergency_contact=True,
        ),
    ]
    db.session.add_all(contacts)

    groups = [
        Group(teacher_id=1, group_name="Koalas", day="Friday"),
        Group(teacher_id=1, group_name="Koalas", day="Thursday"),
        Group(teacher_id=2, group_name="Koalas", day="Tuesday"),
        Group(teacher_id=2, group_name="Emus", day="Friday"),
        Group(teacher_id=3, group_name="Joeys", day="Thursday"),
        Group(teacher_id=3, group_name="Joeys", day="Tuesday"),
    ]
    db.session.add_all(groups)
    db.session.commit()
    print("Comments, teachers, contacts, groups all registered.")

    attendances = [
        Attendance(child_id=1, group_id=2, contact_id=2),
        Attendance(child_id=2, group_id=5, contact_id=2),
        Attendance(child_id=1, group_id=6, contact_id=1),
        Attendance(child_id=2, group_id=3, contact_id=3),
        Attendance(child_id=2, group_id=3, contact_id=4),
    ]
    db.session.add_all(attendances)
    db.session.commit()
    print("Attendances seeded, well done!")
