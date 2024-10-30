from http.client import HTTPException

import marshmallow
import sqlalchemy
from sqlalchemy import exc
from total import db_utils
import models
from db_utils import get_entry_by_username_scalar
from schemas import *
from models import *
import base64
from flask import Blueprint, jsonify, request, make_response
from flask_httpauth import HTTPBasicAuth
from flask_bcrypt import check_password_hash

api_blueprint = Blueprint('api', __name__)
errors = Blueprint('errors', __name__)
auth = HTTPBasicAuth()
STUDENT_ID = 10


@api_blueprint.route("/hello-world")
def hello_world_def():
    return f"Hello World!!!"


@api_blueprint.route(f"/hello-world-{STUDENT_ID}")
def hello_world():
    return f"Hello, World {STUDENT_ID}"


def verify_password(username, password):
    user = db_utils.get_entry_by_name(Person, username)
    if check_password_hash(user.password, password):
        return username
    return None


"""=========================  ERRORS  ================================================"""


@errors.app_errorhandler(sqlalchemy.exc.NoResultFound)
def handle_error(error):
    response = {
        'code': 404,
        'error': 'Not found'
    }

    return jsonify(response), 404


@errors.app_errorhandler(KeyError)
def handle_error(error):
    response = {
        'code': 400,
        'error': str(error.args[0]) + 'isnt presented in keys, add it or check existed one'
    }

    return jsonify(response), 400


@errors.app_errorhandler(sqlalchemy.exc.IntegrityError)
def handle_error(error):
    response = {
        'code': 400,
        'error': 'Not enough data'
    }

    return jsonify(response), 400


@errors.app_errorhandler(marshmallow.exceptions.ValidationError)
def handle_error(error):
    response = {
        'code': 400,
        'error': str(error.args[0])
    }

    return jsonify(response), 400


# ===================================================================================


def StatusResponse(response, code):
    param = response.json
    if isinstance(param, list):
        param.append({"code": code})
    else:
        param.update({"code": code})
    end_response = make_response(jsonify(param), code)
    return end_response


def admin_required(function):
    def wrapper(*args, **kwargs):
        username = auth.current_user()
        user = db_utils.get_entry_by_name(Person, username)
        if user.isAdmin == '1':
            return function(*args, **kwargs)
        else:
            return StatusResponse(jsonify({"error": f"User must be an admin to use {function.__name__}."}), 401)

    wrapper.__name__ = function.__name__
    return wrapper


""" ________________________________________________  USER  ________________________________________________"""


@api_blueprint.route("/users", methods=["GET"])
@auth.login_required()
@admin_required
def getUsers():
    user = db_utils.get_entry(Person)
    response = make_response(jsonify(GetPerson(many=True).dump(user)))
    response.status_code = 200

    return response.json


@api_blueprint.route('/user/register', methods=['POST'])
def create_user():
    try:
        person_data = CreatePerson().load(request.json)

        for key in person_data:
            if key == 'username':
                if db_utils.get_entry_by_username_scalar(total.models.Person, person_data[key]) is not None:
                    response = make_response(jsonify(message="Username duplicate", status=400))
                    response.status_code = 400
                    return response
            if key == 'email':
                if db_utils.get_entry_by_email_scalar(total.models.Person, person_data[key]) is not None:
                    response = make_response(jsonify(message="Email duplicate", status=400))
                    response.status_code = 400
                    return response

        user = db_utils.create_entry(total.models.Person, **person_data)
        response = make_response(jsonify(PersonData().dump(user)))
        response.status_code = 200
    except sqlalchemy.exc.IntegrityError:
        response = make_response(jsonify(message="Invalid data input", status=400))
        response.status_code = 400
    except ValidationError as err:
        response = dict({"Incorrect fields": err.normalized_messages()})
        return response, 400
    return response

def StatusResponse(response, code):
    param = response.json
    if isinstance(param, list):
        param.append({"code": code})
    else:
        param.update({"code": code})
    end_response = make_response(jsonify(param), code)
    return end_response


@api_blueprint.route("/user/login")
@auth.verify_password
def login(username, password):
    user = db_utils.get_entry_by_name(Person, username)
    if check_password_hash(user.password, password):
        return True
    return False


@api_blueprint.route("/user_login")
@auth.login_required()
def user_login():
    username = auth.username()
    user = db_utils.get_entry_by_name(Person, username)
    response = make_response(jsonify(PersonData().dump(user)), 200)
    return response
# @api_blueprint.route("/login")
# @auth.verify_password
# def login(username, password):
#     user = db_utils.get_entry_by_name(Person, username)
#     if check_password_hash(user.password, password):
#         return True
#
#     return False

@api_blueprint.route('/user/<int:user_id>', methods=['GET'])
@auth.login_required()
@admin_required
def get_user_by_id(user_id):
    try:
        user = db_utils.get_entry_by_id(Person, user_id)

        response = make_response(jsonify(PersonData().dump(user)))
        response.status_code = 200
    except sqlalchemy.exc.NoResultFound:
        response = make_response(jsonify(message="Invalid ID input", status=400))
        response.status_code = 400
    return response


@api_blueprint.route("/user/<int:user_id>", methods=["PUT"])
@auth.login_required()
def update_user(user_id):
    try:
        username = auth.current_user()
        user = db_utils.get_entry_by_name(Person, username)
        user_data = UpdatePerson().load(request.json)
        # if user.id != user_id:
        #     response = make_response(jsonify(message="You cannot update other person", status=400))
        #     response.status_code = 400
        #     return response
        for key in user_data:
            if key == 'username':
                if db_utils.get_entry_by_username_scalar(Person, user_data[key]) is not None:
                    response = make_response(jsonify(message="Username duplicate", status=400))
                    response.status_code = 400
                    return response
            if key == 'email':
                if db_utils.get_entry_by_email_scalar(Person, user_data[key]) is not None:
                    response = make_response(jsonify(message="Email duplicate", status=400))
                    response.status_code = 400
                    return response

        db_utils.get_entry_by_id(Person, user_id)
        db_utils.update_entry(Person, user_id, **user_data)
        response = make_response(jsonify(message="User data updated", status=200))
        response.status_code = 200
    except sqlalchemy.exc.IntegrityError:
        response = make_response(jsonify(message="Invalid data input", status=400))
        response.status_code = 400
    except sqlalchemy.exc.NoResultFound:
        response = make_response(jsonify(message="Invalid ID input", status=400))
        response.status_code = 400
    return response


@api_blueprint.route("/user/<int:user_id>", methods=["DELETE"])
@auth.login_required()
def delete_user(user_id):
    username = auth.current_user()
    user = db_utils.get_entry_by_name(Person, username)
    print(user.id)
    print(user_id)
    # if user.id != user_id:
    #     response = make_response(jsonify(message="You cannot delete other user!!", status=400))
    #     response.status_code = 200
    #     return response

    if db_utils.delete_entry(Person, user_id) == 405:
        response = make_response(jsonify(message="Invalid input id", status=405))
        response.status_code = 405
        return response
    try:
        db_utils.delete_entry(Person, user_id)
        response = make_response(jsonify(message="User deleted", status=200))
        response.status_code = 200
    except sqlalchemy.exc.NoResultFound:
        response = make_response(jsonify(message="Invalid ID input", status=400))
        response.status_code = 400
    return response


""" ________________________________________________ CALENDAR  ________________________________________________"""


@api_blueprint.route("/calendars", methods=["GET"])
@auth.login_required()
# @admin_required
def getCalendars():
    calendar = db_utils.get_entry(Calendar)
    response = make_response(jsonify(GetCalendar(many=True).dump(calendar)))
    response.status_code = 200
    return response


@api_blueprint.route('/calendar', methods=["POST"])
@auth.login_required()
def create_calendar():
    username = auth.current_user()
    user = db_utils.get_entry_by_name(Person, username)
    try:
        calendar_data = CreateCalendar().load(request.json)
        calendar_data['person_id'] = user.id
        calendar = db_utils.create_entry_calendar(Calendar, **calendar_data)
        response = make_response(jsonify(UpdateCalendar().dump(calendar)))
        response.status_code = 200
    except sqlalchemy.exc.IntegrityError:
        response = make_response(jsonify(message="Invalid data input", status=400))
        response.status_code = 400
    except ValidationError as err:
        response = dict({"Incorrect fields": err.normalized_messages()})
        return response, 400
    return response


@api_blueprint.route('/calendar/<int:calendar_id>', methods=['GET'])
@auth.login_required()
def get_calendar_by_id(calendar_id):
    try:
        calendar = db_utils.get_entry_by_id(Calendar, calendar_id)

        response = make_response(jsonify(CalendarData().dump(calendar)))
        response.status_code = 200
    except sqlalchemy.exc.NoResultFound:
        response = make_response(jsonify(message="Invalid ID input", status=400))
        response.status_code = 400
    return response


@api_blueprint.route("/calendar/<int:calendar_id>", methods=["PUT"])
@auth.login_required()
def update_calendar(calendar_id):
    username = auth.current_user()
    user = db_utils.get_entry_by_name(Person, username)
    # print(user.id)
    calendar = db_utils.get_entry_by_two_id_oneSec(Calendar, user.id, calendar_id)
    print(calendar)
    personCalendar = db_utils.get_entry_by_two_id_one(PersonCalendar, user.id, calendar_id)
    print(personCalendar)
    if personCalendar == 400 and calendar == 400:
        response = make_response(jsonify(message="This user cannot update this calendar", status=400))
        response.status_code = 400
        return response

    if (calendar != 400 and user.id == calendar.person_id) or user.id == personCalendar.person_id:
        try:
            calendar_data = UpdateCalendar().load(request.json)
            db_utils.get_entry_by_id(Calendar, calendar_id)
            db_utils.update_entry(Calendar, calendar_id, **calendar_data)
            response = make_response(jsonify(message="Calendar data updated", status=200))
            response.status_code = 200
        except sqlalchemy.exc.IntegrityError:
            response = make_response(jsonify(message="Invalid data input", status=400))
            response.status_code = 400
        except sqlalchemy.exc.NoResultFound:
            response = make_response(jsonify(message="Invalid ID input", status=400))
            response.status_code = 400
        except ValidationError as err:
            response = dict({"Incorrect fields": err.normalized_messages()})
            return response, 400
        return response
    else:
        response = make_response(jsonify(message="This user cannot update this calendar", status=400))
        return response, 400


@api_blueprint.route("/calendar/<int:calendar_id>", methods=["DELETE"])
@auth.login_required()
def delete_calendar(calendar_id):
    username = auth.current_user()
    user = db_utils.get_entry_by_name(Person, username)
    # print(user.id)
    calendar = db_utils.get_entry_by_two_id_oneSec(Calendar, user.id, calendar_id)
    if calendar == 400:
        response = make_response(jsonify(message="This user cannot delete this calendar", status=400))
        response.status_code = 400
        return response

    if db_utils.delete_entry(Calendar, calendar_id) == 405:
        response = make_response(jsonify(message="Invalid input id", status=405))
        response.status_code = 405
        return response
    try:
        db_utils.delete_entry(Calendar, calendar_id)
        response = make_response(jsonify(message="Calendar deleted", status=200))
        response.status_code = 200
    except sqlalchemy.exc.NoResultFound:
        response = make_response(jsonify(message="Invalid ID input", status=400))
        response.status_code = 400
    return response


@api_blueprint.route("/calendar/get_access/<int:user_id>/<int:calendar_id>", methods=["POST"])
@auth.login_required()
@admin_required
def get_access(user_id, calendar_id):
    # access_data = PersonCalendarData().load(request.json)

    try:
        if db_utils.get_entry_by_two_id(PersonCalendar, user_id, calendar_id) is not None:
            response = make_response(jsonify(message="Duplicate entry", status=400))
            response.status_code = 400
            return response

        db_utils.create_entry_two_id(PersonCalendar, user_id, calendar_id)
        response = make_response(jsonify(message="Successfully added access", status=200))
        response.status_code = 200
    except sqlalchemy.exc.IntegrityError:
        response = make_response(jsonify(message="Invalid ID input", status=400))
        response.status_code = 400
    except sqlalchemy.exc.NoResultFound:
        response = make_response(jsonify(message="Invalid ID input", status=400))
        response.status_code = 400
    except marshmallow.exceptions.ValidationError as e:
        response = make_response(jsonify(message=e.args[0], status=400))
        response.status_code = 400
    return response

# @api_blueprint.route("/access/<int:user_id>/<int:calendar_id>", methods=["POST"])
# @auth.login_required()
# def give_access(user_id, calendar_id):
#     try:





@api_blueprint.route("/calendar/get_access/<int:user_id>/<int:calendar_id>", methods=["DELETE"])
@auth.login_required()
@admin_required
def delete_access(user_id, calendar_id):
    try:
        if db_utils.get_entry_by_two_id(PersonCalendar, user_id, calendar_id) is None:
            response = make_response(jsonify(message="Entry doesn't exist", status=400))
            response.status_code = 400
            return response

        db_utils.delete_entry_two_id(PersonCalendar, user_id, calendar_id)
        response = make_response(jsonify(message="Successfully removed access", status=200))
        response.status_code = 200
    except sqlalchemy.exc.IntegrityError:
        response = make_response(jsonify(message="Invalid ID input", status=400))
        response.status_code = 400
    except sqlalchemy.exc.NoResultFound:
        response = make_response(jsonify(message="Invalid ID input", status=400))
        response.status_code = 400
    except marshmallow.exceptions.ValidationError as e:
        response = make_response(jsonify(message=e.args[0], status=400))
        response.status_code = 400
    return response


"""  ________________________________________________ EVENT  ________________________________________________"""


@api_blueprint.route("/events", methods=["GET"])
@auth.login_required()
# @admin_required
def getEvents():
    event = db_utils.get_entry(Event)
    response = make_response(jsonify(GetEvent(many=True).dump(event)))
    response.status_code = 200
    return response
    # get all events


@api_blueprint.route("/access", methods=["GET"])
@auth.login_required()
# @admin_required
def getAccesses():
    access = db_utils.get_entry(PersonCalendar)
    response = make_response(jsonify(UpdatePersonCalendar(many=True).dump(access)))
    response.status_code = 200
    return response


@api_blueprint.route('/event/<int:calendar_id>', methods=["POST"])
@auth.login_required()
def create_event(calendar_id):
    username = auth.current_user()
    user = db_utils.get_entry_by_name(Person, username)
    # print(user.id)
    calendar = db_utils.get_entry_by_two_id_oneSec(Calendar, user.id, calendar_id)
    personCalendar = db_utils.get_entry_by_two_id_one(PersonCalendar, user.id, calendar_id)
    if personCalendar == 400 and calendar == 400:
        response = make_response(jsonify(message="This user cannot update this calendar", status=400))
        response.status_code = 400
        return response
    if (calendar != 400 and user.id == calendar.person_id) or user.id == personCalendar.person_id:
        try:
            event_data = CreateEvent().load(request.json)
            event_data['person_id'] = user.id
            event_data['calendar_id'] = calendar_id
            event = db_utils.create_entry(Event, **event_data)

            response = make_response(jsonify(UpdateEvent().dump(event)))
            response.status_code = 200
            return response
        except sqlalchemy.exc.MultipleResultsFound:
            response = make_response(jsonify(message="Duplicate", status=400))
            response.status_code = 400
        except sqlalchemy.exc.IntegrityError:
            response = make_response(jsonify(message="Invalid data input", status=400))
            response.status_code = 400
        except ValidationError as err:
            response = dict({"Incorrect fields": err.normalized_messages()})
            return response, 400
        return response
    else:
        response = make_response(jsonify(message="This user cannot update this calendar", status=400))
        return response, 400


@api_blueprint.route('/event/<int:event_id>', methods=['GET'])
@auth.login_required()
# @admin_required
def get_event_by_id(event_id):
    try:
        event = db_utils.get_entry_by_id(Event, event_id)

        response = make_response(jsonify(EventData().dump(event)))
        response.status_code = 200
    except sqlalchemy.exc.NoResultFound:
        response = make_response(jsonify(message="Invalid ID input", status=400))
        response.status_code = 400
    return response


@api_blueprint.route("/event/<int:event_id>", methods=["PUT"])
@auth.login_required()
def update_event(event_id):
    username = auth.current_user()
    user = db_utils.get_entry_by_name(Person, username)
    try:
        event_data = UpdateEvent().load(request.json)
        event = db_utils.get_entry_id(Event, event_id)
        if user.id != event.person_id:
            response = make_response(jsonify(message="This user doesnt have an access", status=400))
            response.status_code = 400
            return response
        db_utils.get_entry_by_id(Event, event_id)
        db_utils.update_entry(Event, event_id, **event_data)
        response = make_response(jsonify(message="Event data updated", status=200))
        response.status_code = 200
    except sqlalchemy.exc.IntegrityError:
        response = make_response(jsonify(message="Invalid data input", status=400))
        response.status_code = 400
    except sqlalchemy.exc.NoResultFound:
        response = make_response(jsonify(message="Invalid ID input", status=400))
        response.status_code = 400
    except ValidationError as err:
        response = dict({"Incorrect fields": err.normalized_messages()})
        return response, 400
    return response


@api_blueprint.route("/event/<int:event_id>", methods=["DELETE"])
@auth.login_required()
def delete_event(event_id):
    username = auth.current_user()
    user = db_utils.get_entry_by_name(Person, username)

    event = db_utils.get_entry_by_id(Event, event_id)
    print(user.id)
    print(event)
    if event == 400:
        response = make_response(jsonify(message="Invalid id", status=400))
        response.status_code = 400
        return response

    if user.id == event.person_id:
        try:
            # if db_utils.delete_entry(Event, event_id) == 405:
            #     response = make_response(jsonify(message="Invalid input id", status=405))
            #     response.status_code = 405
            #     return response
            db_utils.delete_entry(Event, event_id)
            response = make_response(jsonify(message="Event deleted", status=200))
            response.status_code = 200
            return response
        except sqlalchemy.exc.NoResultFound:
            response = make_response(jsonify(message="Invalid ID input", status=400))
            response.status_code = 400
            return response
    else:
        response = make_response(jsonify(message="This user doesnt have an access", status=400))
        response.status_code = 400
        return response


"""_______________________________________________________ CATEGORY ________________________________________________ """


@api_blueprint.route("/categories", methods=["GET"])
@auth.login_required()
# @admin_required
def getCategories():
    category = db_utils.get_entry(Category)
    response = make_response(jsonify(GetCategory(many=True).dump(category)))
    response.status_code = 200
    return response


@api_blueprint.route('/category', methods=["POST"])
@auth.login_required()
def create_category():
    try:
        category_data = CreateCategory().load(request.json)
        for key in category_data:
            if key == 'title':
                if db_utils.get_entry_by_title_scalar(Category, category_data[key]) is not None:
                    response = make_response(jsonify(message="Title duplicate", status=400))
                    response.status_code = 400
                    return response
        category = db_utils.create_entry(Category, **category_data)
        response = make_response(jsonify(UpdateCategory().dump(category)))
        response.status_code = 200
        return response
    except sqlalchemy.exc.IntegrityError:
        response = make_response(jsonify(message="Invalid data input", status=400))
        response.status_code = 400
    except ValidationError as err:
        response = dict({"Incorrect fields": err.normalized_messages()})
        return response, 400
    return response


@api_blueprint.route('/category/<int:category_id>', methods=['GET'])
@auth.login_required()
# @admin_required
def get_category_by_id(category_id):
    try:
        category = db_utils.get_entry_by_id(Category, category_id)

        response = make_response(jsonify(CategoryData().dump(category)))
        response.status_code = 200
    except sqlalchemy.exc.NoResultFound:
        response = make_response(jsonify(message="Invalid ID input", status=400))
        response.status_code = 400
    return response


@api_blueprint.route("/category/<int:category_id>", methods=["PUT"])
@auth.login_required()
def update_category(category_id):
    try:
        category_data = CreateCategory().load(request.json)
        for key in category_data:
            if key == 'title':
                if db_utils.get_entry_by_title_scalar(Category, category_data[key]) is not None:
                    response = make_response(jsonify(message="Category type duplicate", status=400))
                    response.status_code = 400
                    return response

        db_utils.get_entry_by_id(Category, category_id)
        db_utils.update_entry(Category, category_id, **category_data)
        response = make_response(jsonify(message="Category data updated", status=200))
        response.status_code = 200
    except sqlalchemy.exc.IntegrityError:
        response = make_response(jsonify(message="Invalid data input", status=400))
        response.status_code = 400
    except sqlalchemy.exc.NoResultFound:
        response = make_response(jsonify(message="Invalid ID input", status=400))
        response.status_code = 400
    except ValidationError as err:
        response = dict({"Incorrect fields": err.normalized_messages()})
        return response, 400
    return response


@api_blueprint.route("/category/<int:category_id>", methods=["DELETE"])
@auth.login_required()
def delete_category(category_id):
    if db_utils.delete_entry(Category, category_id) == 405:
        response = make_response(jsonify(message="Invalid input id", status=405))
        response.status_code = 405
        return response
    try:
        db_utils.delete_entry(Category, category_id)
        response = make_response(jsonify(message="Category deleted", status=200))
        response.status_code = 200
    except sqlalchemy.exc.NoResultFound:
        response = make_response(jsonify(message="Invalid ID input", status=400))
        response.status_code = 400
    return response

