from init import app
from blueprints.cli_bp import cli_commands

# from src.blueprints.attendances_bp import cli_commands

from marshmallow.exceptions import ValidationError
from sqlalchemy.exc import IntegrityError

app.register_blueprint(cli_commands)

# app.register_blueprint(actors_bp)

@app.route("/")
def hello():
    return {"message": "Welcome to Ripe Tomatoes API"}


@app.errorhandler(405)
@app.errorhandler(404)
def not_found(err):
    return {"Error": "no resource found"}


@app.errorhandler(ValidationError)
def invalid_request(err):
    return {"Error": vars(err)["messages"]}, 400


@app.errorhandler(IntegrityError)
def integrity_error(err):
    return {"Error": str(vars(err)['orig'])}, 400


@app.errorhandler(KeyError)
def missing_key(err):
    return {"Error": f"Missing field: {str(err)}"}


print(app.url_map)
