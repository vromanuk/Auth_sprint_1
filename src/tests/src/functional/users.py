from http import HTTPStatus

USERS_ENDPOINT = "/api/v1/users"


def test_update_user_info_without_jwt(client):
    resp = client.put(USERS_ENDPOINT)
    assert resp.status_code == HTTPStatus.UNAUTHORIZED
