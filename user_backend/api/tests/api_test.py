import requests

from .. import app
from flask import json


def test_register_invalid_mail():
    response = app.app.test_client().post(
        '/api/auth/register',
        data=json.dumps({'email': "shadrachde", 'password': "testtest123"}),
        content_type='application/json',
    )

    data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 400


def test_register_invalid_input():
    response = app.app.test_client().post(
        '/api/auth/register',
        data=json.dumps({}),
        content_type='application/json',
    )

    data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 400


def test_register_correctly():
    test_email = "shadrach@live.de"
    response = app.app.test_client().post(
        '/api/auth/register',
        data=json.dumps({'email': test_email, 'password': "testest"}),
        content_type='application/json',
    )

    data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    assert data["email"] == test_email
