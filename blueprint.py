from flask import Blueprint

api_blueprint = Blueprint('api', __name__)
STUDENT_ID = 10


@api_blueprint.route("/hello-world")
def hello_world_def():
    return f"Hello World!!!"


@api_blueprint.route(f"/hello-world-{STUDENT_ID}")
def hello_world():
    return f"Hello, World {STUDENT_ID}"
