from http import HTTPStatus

import pytest

from src import create_app
from src.tests.src.functional.auth import register


@pytest.fixture
def client():
    app = create_app()

    with app.test_client() as client:
        yield client


@pytest.fixture
def registered_user(client):
    login = "testing_user_acc"
    password = "testing_user_password"

    resp = register(client, login, password)
    assert resp.status_code == HTTPStatus.CREATED

    return login, password
