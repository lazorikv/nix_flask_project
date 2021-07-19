"""Testing module for film"""

import requests
from flask import json
import pytest
from services.web.project.app import create_app


def test_film_get_film_id():
    mock_request_data = {
        "title": "North Korean won",
        "release": "1988-11-04",
        "genre": ["drama"],
        "director": "Tanya Phillips",
        "description": "These star page military interesting involve their. Her get strategy many people over walk. "
        "Forward build wall model yeah affect rule still. High consumer join nature great outside "
        "where. Away list movie decade reach avoid.",
        "rating": 3,
        "poster": "https://placekitten.com/965/131",
        "user": "Emily",
    }
    url = "http://0.0.0.0:5000/api/v1/films/get/1"
    response = requests.get(url)
    response_text = response.text
    data = json.loads(response_text)
    assert data == mock_request_data


def test_err_film_get_film_id():
    mock_request_data = {"Error": "Film was not found"}
    url = "http://0.0.0.0:5000/api/v1/films/get/1500"
    response = requests.get(url)
    response_text = response.text
    data = json.loads(response_text)
    assert data == mock_request_data


def test_film_search():
    url = "http://0.0.0.0:5000/api/v1/films/get/?start=1&limit=10&search=Lesotho"
    response = requests.get(url)
    response_text = response.text
    data = json.loads(response_text)
    assert data["count"] == 1


def test_film_pagination():
    url = "http://0.0.0.0:5000/api/v1/films/get/?start=1&limit=17"
    response = requests.get(url)
    response_text = response.text
    data = json.loads(response_text)
    assert len(data["results"]) == 17


def test_film_filtr_genre():
    url = "http://0.0.0.0:5000/api/v1/films/get/?start=1&limit=10&genre_film=fighting"
    response = requests.get(url)
    response_text = response.text
    data = json.loads(response_text)
    assert data["count"] == 40


def test_film_filtr_years_release():
    url = "http://0.0.0.0:5000/api/v1/films/get/?start=1&limit=10&from=1999-01-01&to=2015-01-01"
    response = requests.get(url)
    response_text = response.text
    data = json.loads(response_text)
    assert data["count"] == 48


def test_film_filtr_director():
    url = "http://0.0.0.0:5000/api/v1/films/get/?start=1&limit=10&Director=Bradley%20Raymond"
    response = requests.get(url)
    response_text = response.text
    data = json.loads(response_text)
    assert data["count"] == 5


def test_film_sort_rating():
    url = "http://0.0.0.0:5000/api/v1/films/get/?start=1&limit=10&sort_data=Rating"
    response = requests.get(url)
    response_text = response.text
    data = json.loads(response_text)
    assert data["results"][0]["title"] == "Cuban peso"


@pytest.fixture
def app_test():
    app_t = create_app()
    return app_t


@pytest.fixture
def client():
    with app_test.test_client() as client:
        yield client


def test_add_film(client):

    mimetype = "application/json"
    headers = {"Content-Type": mimetype, "Accept": mimetype}

    data = {
        "title": "Forsage",
        "year_release": "2005-01-01",
        "director_name": "Dominic Torreto",
        "genres": ["action"],
        "description": "Rasing on cars and tanks",
        "rating": "2",
        "poster": "some_poster",
    }
    url = "http://0.0.0.0:5000/api/v1/films/post"

    response = client.post(url, data=json.dumps(data), headers=headers)
    resp_text = response.data.decode("utf-8")
    print(resp_text)
    data_out = json.loads(resp_text)
    expect_text = {"Message": "Film added to database"}
    assert data_out == expect_text


def test_put_film(client):

    mimetype = "application/json"
    headers = {"Content-Type": mimetype, "Accept": mimetype}

    data = {
        "title": "Forsage",
        "year_release": "2005-01-01",
        "director_name": "Dominic Torreto",
        "genres": ["action"],
        "description": "Rasing on cars and tanks",
        "rating": "2",
        "poster": "some_poster",
    }
    url = "http://0.0.0.0:5000/api/v1/films/put/5"

    response = client.put(url, data=json.dumps(data), headers=headers)
    resp_text = response.data.decode("utf-8")
    print(resp_text)
    data_out = json.loads(resp_text)
    expect_text = {"Message": "Data updated"}
    assert data_out == expect_text


def test_delete_film(client):
    expect_data = {"Message": "Data deleted successfully"}
    url = "http://0.0.0.0:5000/api/v1/films/delete/6"
    response = client.delete(url)
    response_text = response.text
    data = json.loads(response_text)
    assert data == expect_data
