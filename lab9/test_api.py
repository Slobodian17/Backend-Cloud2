from base64 import b64encode
import base64
import pytest

import total
import pymysql
from lab9.conftest import *

pymysql.install_as_MySQLdb()


class TestPerson:
    def test_user_create(self, user_info3):
        # print(user_info3)
        response = total.app.app.test_client().post('/user/register', json=user_info3)
        assert response.status_code == 200

    def test_user_create_invalid_email(self, user_info4):
        response = total.app.app.test_client().post('/user/register', json=user_info4)
        assert response.json == {
            'Incorrect fields': {
                'email':
                    ['Not a valid email address.']
            }
        }

    def test_user_create_username_used(self, user_info1, user_info2):
        user_info2["username"] = "user1"
        total.app.app.test_client().post('/user/register', json=user_info1)
        response = total.app.app.test_client().post('/user/register', json=user_info2)
        assert response.status_code == 400
        assert response.data == b'{"message":"Username duplicate","status":400}\n'



