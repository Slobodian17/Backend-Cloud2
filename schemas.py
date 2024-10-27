from flask_bcrypt import generate_password_hash
from marshmallow import validate, Schema, fields, ValidationError


class CreatePerson(Schema):
    username = fields.String(required=True)
    firstname = fields.String(required=True)
    lastname = fields.String(required=True)
    phone_number = fields.Function(required=True,
                                   validate=validate.Regexp('^[+]*[(]{0,1}[0-9]{1,4}[)]{0,1}[\s0-9]{4,20}$'))
    email = fields.String(required=True, validate=validate.Email())
    password = fields.Function(required=True, deserialize=lambda obj: generate_password_hash(obj), load_only=True)
    isAdmin = fields.String(validate=validate.OneOf(choices=['0', '1']))


class PersonData(Schema):
    id = fields.Integer()
    username = fields.String()
    firstname = fields.String()
    lastname = fields.String()
    phone_number = fields.String()
    email = fields.String()
    password = fields.String()
    isAdmin = fields.String()


class UpdatePerson(Schema):
    username = fields.String()
    firstname = fields.String(validate=validate.Length(min=2))
    lastname = fields.String(validate=validate.Length(min=2))
    phone_number = fields.Function(validate=validate.Regexp('^[+]*[(]{0,1}[0-9]{1,4}[)]{0,1}[\s0-9]{4,20}$'))
    email = fields.String(validate=validate.Email())
    password = fields.Function(deserialize=lambda obj: generate_password_hash(obj), load_only=True)
    isAdmin = fields.String(validate=validate.OneOf(choices=['0', '1']))


class GetPerson(Schema):
    id = fields.Integer()
    username = fields.String()
    firstname = fields.String()
    lastname = fields.String()
    phone_number = fields.String()
    email = fields.String()
    password = fields.String()
    isAdmin = fields.String()


class CreateCalendar(Schema):
    type = fields.String()
    description = fields.String()
    time_zone = fields.String(validate=validate.OneOf(choices=['1', '2']))
    # person_id = fields.Integer(required=True)


class CalendarData(Schema):
    id = fields.Integer()
    type = fields.String()
    description = fields.String()
    time_zone = fields.String()
    person_id = fields.Integer(required=True)


class UpdateCalendar(Schema):
    type = fields.String()
    description = fields.String()
    time_zone = fields.String(validate=validate.OneOf(choices=['1', '2']))


class GetCalendar(Schema):
    id = fields.Integer()
    type = fields.String()
    description = fields.String()
    time_zone = fields.String()
    person_id = fields.Integer(required=True)


class CreateEvent(Schema):
    title = fields.String(required=True)
    description = fields.String()
    created_at = fields.DateTime(required=True)
    updated_at = fields.DateTime(default=created_at)
    content = fields.String()
    category_id = fields.Integer(required=True)


class EventData(Schema):
    title = fields.String()
    description = fields.String()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    content = fields.String()
    calendar_id = fields.Integer(required=True)
    category_id = fields.Integer(required=True)
    person_id = fields.Integer(required=True)


class UpdateEvent(Schema):
    title = fields.String()
    description = fields.String()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    content = fields.String()


class GetEvent(Schema):
    id = fields.Integer()
    title = fields.String()
    description = fields.String()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    content = fields.String()
    calendar_id = fields.Integer()
    category_id = fields.Integer()
    person_id = fields.Integer(required=True)


class CreateCategory(Schema):
    title = fields.String(required=True)


class CategoryData(Schema):
    id = fields.Integer(required=True)
    title = fields.String(required=True)


class UpdateCategory(Schema):
    title = fields.String(required=True)


class GetCategory(Schema):
    id = fields.Integer(required=True)
    title = fields.String(required=True)


class CreatePersonCalendar(Schema):
    person_id = fields.Integer()
    calendar_id = fields.Integer()


class PersonCalendarData(Schema):
    id = fields.Integer(required=True)
    person_id = fields.Integer()
    calendar_id = fields.Integer()


class DeletePersonCalendar(Schema):
    id = fields.Integer(required=True)
    person_id = fields.Integer()
    calendar_id = fields.Integer()


class UpdatePersonCalendar(Schema):
    person_id = fields.Integer()
    calendar_id = fields.Integer()

# {
#
#     "username": "user1",
#     "firstname": "user1f",
#     "lastname": "user1s",
#     "phone_number": "+380000000000",
#     "email": "me@gmail.com",
#     "password": "Pas123Qwerty"
# }
