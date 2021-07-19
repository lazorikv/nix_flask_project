"""Test for module Director"""

import requests
from flask import json
import pytest


def test_director():
    mimetype = "application/json"
    headers = {"Content-Type": mimetype, "Accept": mimetype}
    data = {
        "director_name": "TAG"
    }
    url = "http://0.0.0.0:5000/api/v1/directors/post"

    response = requests.post(url, data=json.dumps(data), headers=headers)
    resp_text = response.text
    data = json.loads(resp_text)
    expect_text = {"Message": "Director added to database"}
    assert data == expect_text


def test_director_exist():
    mimetype = "application/json"
    headers = {"Content-Type": mimetype, "Accept": mimetype}
    data = {
        "director_name": "TAG"
    }
    url = "http://0.0.0.0:5000/api/v1/directors/post"

    response = requests.post(url, data=json.dumps(data), headers=headers)
    resp_text = response.text
    data = json.loads(resp_text)
    expect_text = {"Error": "Director is already exist"}
    assert data == expect_text
