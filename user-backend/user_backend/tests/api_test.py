import pytest
import os

import app
from flask import json


class Header:
    token = None


def test_register_invalid_mail():
    response = app.app.test_client().post(
        '/api/auth/register',
        data=json.dumps({'email': "shadrachde", 'password': "testtest123"}),
        content_type='application/json',
        follow_redirects=True
    )

    data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 400
    assert data["message"] == {'email': ['Not a valid email address.']}


def test_register_no_input():
    response = app.app.test_client().post(
        '/api/auth/register',
        data=json.dumps({'email': "", 'password': ""}),
        content_type='application/json',
        follow_redirects=True
    )

    data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 400
    assert data["message"] == {'email': ['Not a valid email address.']}


def test_register_no_mail():
    test_email = ""
    password = "hjwdfbjwd"
    response = app.app.test_client().post(
        '/api/auth/register',
        data=json.dumps({'email': test_email, 'password': password}),
        content_type='application/json',
        follow_redirects=True
    )

    data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 400
    assert data["status"] == "error"
    assert data["message"] == {'email': ['Not a valid email address.']}


def test_register_no_password():
    response = app.app.test_client().post(
        '/api/auth/register',
        data=json.dumps({'email': "shadrach@check.de", 'password': ""}),
        content_type='application/json',
        follow_redirects=True
    )

    # TODO handle empty password input
    data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 400
    assert data["message"] == {'email': ['Not a valid email address.']}


@pytest.mark.skip("Account already exist")
def test_register_correctly():
    test_email = "shadrach@live.de"
    response = app.app.test_client().post(
        '/api/auth/register',
        data=json.dumps({'email': test_email, 'password': "testest"}),
        content_type='application/json',
        follow_redirects=True
    )

    data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    assert data["message"] == "Successfully created account"
    assert data["email"] == test_email


def test_login():
    test_email = "shadrach@live.de"
    password = "testest"
    response = app.app.test_client().post(
        '/api/auth/login',
        data=json.dumps({'email': test_email, 'password': password}),
        content_type='application/json',
        follow_redirects=True
    )

    data = json.loads(response.get_data(as_text=True))
    Header.token = data["token"]

    assert response.status_code == 200
    assert data["status"] == "success"


def test_put_player_uuid():
    response = app.app.test_client().put(
        '/api/users/kjshds',
        content_type='application/json',
        follow_redirects=True
    )

    data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    assert data["status"] == "success"


@pytest.mark.skip("TODO: implement header")
def test_logout():
    test_email = "shadrach@live.de"
    password = "testest"
    # TODO implement header in test
    response = app.app.test_client().post(
        '/api/auth/logout',
        content_type='application/json',
        follow_redirects=True,
        **{"x-access-tokens": Header.token}
    )

    data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    assert data["status"] == "success"
    assert data["message"] == "Successfully logged out"


def test_login_wrong_password():
    test_email = "shadrach@live.de"
    password = "testestest"
    response = app.app.test_client().post(
        '/api/auth/login',
        data=json.dumps({'email': test_email, 'password': password}),
        content_type='application/json',
        follow_redirects=True
    )

    data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 400
    assert data["status"] == "error"
    assert data["message"] == "Invalid Input"


def test_login_no_password():
    test_email = "shadrach@live.de"
    password = ""
    response = app.app.test_client().post(
        '/api/auth/login',
        data=json.dumps({'email': test_email, 'password': password}),
        content_type='application/json',
        follow_redirects=True
    )

    data = json.loads(response.get_data(as_text=True))
    # TODO handle empty password input

    assert response.status_code == 400
    assert data["status"] == "error"
    assert data["message"] == "Invalid Input"


def test_login_no_mail():
    test_email = ""
    password = "hjwdfbjwd"
    response = app.app.test_client().post(
        '/api/auth/login',
        data=json.dumps({'email': test_email, 'password': password}),
        content_type='application/json',
        follow_redirects=True
    )

    data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 400
    assert data["status"] == "error"
    assert data["message"] == {'email': ['Not a valid email address.']}


def test_login_wrong_mail():
    test_email = "kjwaden@jkdnf.de"
    password = "hjwdfbjwd"
    response = app.app.test_client().post(
        '/api/auth/login',
        data=json.dumps({'email': test_email, 'password': password}),
        content_type='application/json',
        follow_redirects=True
    )

    data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 404
    assert data["status"] == "error"
    assert data["message"] == "User not found"
