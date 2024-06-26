from init import app
from blueprints.cli_bp import cli_commands
from blueprints.users_bp import users_bp
from blueprints.children_bp import children_bp
from blueprints.teachers_bp import teachers_bp
from blueprints.groups_bp import groups_bp
from blueprints.contacts_bp import contacts_bp

from marshmallow.exceptions import ValidationError
from sqlalchemy.exc import IntegrityError

app.register_blueprint(cli_commands)
app.register_blueprint(users_bp)
app.register_blueprint(children_bp)
app.register_blueprint(teachers_bp)
app.register_blueprint(groups_bp)
app.register_blueprint(contacts_bp)


@app.route("/")
def hello():
    return {"message": "Welcome to the ClassTracker API"}


@app.errorhandler(405)
@app.errorhandler(404)
def not_found(err):
    print(err)
    return {"Error": "No resource found"}, 404


@app.errorhandler(ValidationError)
def invalid_request(err):
    return {"Error": vars(err)["messages"]}, 400


@app.errorhandler(IntegrityError)
def integrity_error(err):
    return {"Error": str(vars(err)["orig"])}, 400


@app.errorhandler(KeyError)
def missing_key(err):
    return {"Error": f"Request is missing field: {str(err)}"}, 400


@app.errorhandler(TypeError)
def incorrect_body(err):
    return {
        "Error": f"{str(err).capitalize()}, please check your request body's formatting"
    }, 400


print(app.url_map)
