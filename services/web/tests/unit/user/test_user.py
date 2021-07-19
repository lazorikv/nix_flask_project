"""Test model User"""

import requests
from flask import json
import pytest


def test_user_add():
    mimetype = "application/json"
    headers = {"Content-Type": mimetype, "Accept": mimetype}
    data = {
        "username": "Vladyslav",
        "password": "12345",
        "is_admin": False
    }
    url = "http://0.0.0.0:5000/api/v1/users/post"

    response = requests.post(url, data=json.dumps(data), headers=headers)
    resp_text = response.text
    data = json.loads(resp_text)
    expect_text = {"Message": "User added to database"}
    assert data == expect_text


