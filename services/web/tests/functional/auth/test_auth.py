"""Module for testing login, signup, logout"""
import requests
from flask import json
import pytest
from services.web.project.app import create_app


@pytest.fixture
def app_test():
    app_t = create_app()
    return app_t


@pytest.fixture
def client():
    with app_test.test_client() as client:
        yield client


def test_signup():
    mimetype = "application/json"
    headers = {"Content-Type": mimetype, "Accept": mimetype}
    data = {"username": "ret", "password": "ret", "is_admin": False}
    url = "http://0.0.0.0:5000/api/v1/auth/signup"

    response = requests.post(url, data=json.dumps(data), headers=headers)
    resp_text = response.text
    data = json.loads(resp_text)
    expect_text = {"Message": "User ret has been created successfully"}
    assert data == expect_text


def test_login():
    mimetype = "application/json"
    headers = {"Content-Type": mimetype, "Accept": mimetype}
    data = {"username": "admin", "password": "admin"}
    url = "http://0.0.0.0:5000/api/v1/auth/login"

    response = requests.post(url, data=json.dumps(data), headers=headers)
    resp_text = response.text
    data = json.loads(resp_text)
    expect_text = {"Message": "User admin has been login successfully"}
    assert data == expect_text


def test_err_logout(client):
    mock_request_data = {"Message": "The method is not allowed for the requested URL."}
    url = "http://0.0.0.0:5000/api/v1/auth/logout"
    response = client.get(url)
    response_text = response.text
    data = json.loads(response_text)
    assert data == mock_request_data
