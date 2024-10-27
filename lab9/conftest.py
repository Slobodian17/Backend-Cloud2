import pytest
from base64 import b64encode
import base64
import pytest
from total.app import app
from total.models import *
import pymysql
from flask_bcrypt import generate_password_hash


pymysql.install_as_MySQLdb()
@pytest.fixture
def user_info1():
    user_info = {
        "username": "user1",
        "firstname": "user1",
        "lastname": "user1",
        "phone_number": "+380000000200",
        "email": "1@gmail.com",
        "password": "123",
        "isAdmin": "0"
    }
    return user_info


@pytest.fixture
def user_info2():
    user_info = {
        "username": "user2",
        "firstname": "user2",
        "lastname": "user2",
        "phone_number": "+380000000200",
        "email": "2@gmail.com",
        "password": "123",
        "isAdmin": "0"
    }
    return user_info


@pytest.fixture(scope='function')
def user_info3():
    user_info3 = {
        "username": "user777",
        "firstname": "user2177f",
        "lastname": "user217s",
        "phone_number": "+381000000200",
        "email": "us61111@gmail.com",
        "password": "123",
        "isAdmin": "0"
    }
    return user_info3


@pytest.fixture
def user_info4():
    user_info = {
        "username": "1",
        "firstname": "1",
        "lastname": "1",
        "email": "wrong",
        "password": "admin123",
        "phone_number": "+380689098277",
        "isAdmin": "1"
    }
    return user_info


@pytest.fixture
def user_info5():
    user_info = {
        "username": "5",
        "firstname": "1",
        "lastname": "1",
        "email": "5@gmail.com",
        "password": "admin123",
        "phone_number": "+380689098277",
        "isAdmin": "0"
    }
    return user_info


@pytest.fixture
def user_info6():
    user_info = {
        "username": "6",
        "firstname": "1",
        "lastname": "1",
        "email": "6@gmail.com",
        "password": "admin123",
        "phone_number": "+380689098277",
        "isAdmin": "0"
    }
    return user_info


@pytest.fixture(scope='function')
def wrapper(request):
    session.close()
    Base.metadata.drop_all(sql_engine)
    Base.metadata.create_all(sql_engine)