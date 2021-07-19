"""Test model Genre"""

import requests
from flask import json
import pytest


def test_genre():
    mimetype = "application/json"
    headers = {"Content-Type": mimetype, "Accept": mimetype}
    data = {
        "genre_name": "Indian"
    }
    url = "http://0.0.0.0:5000/api/v1/genres/post"

    response = requests.post(url, data=json.dumps(data), headers=headers)
    resp_text = response.text
    data = json.loads(resp_text)
    expect_text = {
        "Message": "Genre added to database"
    }
    assert data == expect_text


def test_genre_exist():
    mimetype = "application/json"
    headers = {"Content-Type": mimetype, "Accept": mimetype}
    data = {
        "genre_name": "Indian"
    }
    url = "http://0.0.0.0:5000/api/v1/genres/post"

    response = requests.post(url, data=json.dumps(data), headers=headers)
    resp_text = response.text
    data = json.loads(resp_text)
    expect_text = {"Error": "Genre is already exist"}
    assert data == expect_text
