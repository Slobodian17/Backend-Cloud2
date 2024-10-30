from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import exists
from datetime import datetime



engine = create_engine("mysql+pymysql://root:root1234@cloud2db.cbgywims63dz.eu-north-1.rds.amazonaws.com:3306/cloud2db", echo=False, pool_size=20, max_overflow=40)
SessionFactory = sessionmaker(bind=engine)


def create_entry(model_class, commit=True, **kwargs):
    session = SessionFactory()
    entry = model_class(**kwargs)
    session.add(entry)
    if commit:
        session.commit()
    return (session.query(model_class).filter_by(**kwargs)).one()


def create_entry_calendar(model_class, commit=True, **kwargs):
    session = SessionFactory()
    entry = model_class(**kwargs)
    session.add(entry)
    if commit:
        session.commit()
    list = (session.query(model_class).filter_by(**kwargs)).all()
    return list[len(list)-1]


# def update_entry(entry, *, commit=True, **kwargs):
#     session = SessionFactory()
#     for key, value in kwargs.items():
#         setattr(entry, key, value)
#     if commit:
#         session.commit()
#     return entry

def get_entry_by_username_scalar(model_class, username):
    session = SessionFactory()
    return session.query(model_class).filter_by(username=username).scalar()

# def get_entry_by_name(model_class, user_name, **kwargs):
#     session = Session()
#     return session.query(model_class).filter_by(username=user_name, **kwargs).one()

def get_entry_by_name(model_class, username, **kwargs):
    session = SessionFactory()
    if session.query(model_class).filter_by(username=username).all() == []:
        return 404
    return session.query(model_class).filter_by(username=username, **kwargs).one()
# def get_entry_by_name(model_class, name):
#     return model_class.query.filter_by(username=name).first()




def get_entry_by_email_scalar(model_class, email):
    session = SessionFactory()
    return session.query(model_class).filter_by(email=email).scalar()


def get_entry_by_type_scalar(model_class, type):
    session = SessionFactory()
    return session.query(model_class).filter_by(type=type).scalar()


def get_entry_by_title_scalar(model_class, title):
    session = SessionFactory()
    return session.query(model_class).filter_by(title=title).scalar()


def update_entry(model_class, id, commit=True, **kwargs):
    session = SessionFactory()
    entry = session.query(model_class).filter_by(id=id).one()
    for key, value in kwargs.items():
        setattr(entry, key, value)
    if commit:
        session.commit()
    return entry


def delete_entry(model_class, input_id, *, commit=True, **kwargs):
    session = SessionFactory()
    if not session.query(model_class).filter_by(id=input_id).all():
        return 405
    session.query(model_class).filter_by(id=input_id).delete()
    if commit:
        session.commit()


# def delete_entry(model_class, id, *, commit=True, **kwargs):
#     session = SessionFactory()
#     session.query(model_class).filter_by(id=id, **kwargs).delete()
#     if commit:
#         session.commit()


def get_entry(model_class):
    session = SessionFactory()
    # entry =session.query(model_class).all()
    # print(entry)
    return session.query(model_class).all()


def get_entry_by_id(model_class, uid, **kwargs):
    session = SessionFactory()
    if session.query(model_class).filter_by(id=uid, **kwargs).all() == []:
        return 400
    return session.query(model_class).filter_by(id=uid, **kwargs).one()


def create_entry_two_id(model_class, user_id, calendar_id, commit=True):
    session = SessionFactory()
    entry = model_class(person_id=user_id, calendar_id=calendar_id)
    session.add(entry)
    if commit:
        session.commit()
    return session.query(model_class).filter_by(person_id=user_id, calendar_id=calendar_id).one()


def delete_entry_two_id(model_class, user_id, calendar_id, commit=True):
    session = SessionFactory()
    session.query(model_class).filter_by(person_id=user_id, calendar_id=calendar_id).delete()
    if commit:
        session.commit()


def get_entry_by_two_id_oneSec(model_class, user_id, calendar_id):
    session = SessionFactory()
    if session.query(model_class).filter_by(person_id=user_id, id=calendar_id).all() == []:
        return 400
    return session.query(model_class).filter_by(person_id=user_id, id=calendar_id).one()


def get_entry_by_two_id_one(model_class, user_id, calendar_id):
    session = SessionFactory()
    if session.query(model_class).filter_by(person_id=user_id, calendar_id=calendar_id).all() == []:
        return 400
    return session.query(model_class).filter_by(person_id=user_id, calendar_id=calendar_id).one()


def get_entry_by_two_id(model_class, user_id, calendar_id):
    session = SessionFactory()
    return session.query(model_class).filter_by(person_id=user_id, calendar_id=calendar_id).scalar()


def get_entry_id(model_class, user_id):
    session = SessionFactory()
    return session.query(model_class).filter_by(id=user_id).scalar()
    # return session.query(exists().where(model_class.id == user_id)).scalar()


def get_entry_personCalendar(model_class, calendar_id, person_id):
    session = SessionFactory()
    return session.query(model_class).filter_by(calendar_id=calendar_id, person_id=person_id).scalar()


def get_entry_userCreator(model_class,calendar_id, person_id):
    session = SessionFactory()
    return session.query(model_class).filter_by(id=calendar_id, person_id=person_id).scalar()
