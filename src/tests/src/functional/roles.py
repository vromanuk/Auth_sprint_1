from http import HTTPStatus

from flask_jwt_extended import create_access_token

ROLES_ENDPOINT = "/api/v1/roles"


def test_get_all_roles(client, registered_user):
    user_login, password = registered_user
    additional_claims = {"perm": 255}
    access_token = create_access_token(user_login, additional_claims=additional_claims)
    headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }

    resp = client.get(ROLES_ENDPOINT, headers=headers)
    assert resp.status_code == HTTPStatus.OK


def test_get_all_roles_forbidden(client, registered_user):
    user_login, password = registered_user
    additional_claims = {"perm": 0}
    access_token = create_access_token(user_login, additional_claims=additional_claims)
    headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }

    resp = client.get(ROLES_ENDPOINT, headers=headers)
    assert resp.status_code == HTTPStatus.FORBIDDEN


def test_get_all_roles_without_jwt(client):
    resp = client.get(ROLES_ENDPOINT)
    assert resp.status_code == HTTPStatus.UNAUTHORIZED
