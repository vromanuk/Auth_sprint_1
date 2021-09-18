import uuid
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
    login = str(uuid.uuid4())
    password = str(uuid.uuid4())

    resp = register(client, login, password)
    assert resp.status_code == HTTPStatus.CREATED

    return login, password
