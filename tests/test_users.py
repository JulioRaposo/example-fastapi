import pytest
from jose import jwt
from app.config import settings
from app import schemas


# def test_root(client):
#     res = client.get('/')
#     print(res.json().get('message'))
#     assert res.json().get('message') == 'hello world!!!'
#     assert res.status_code == 200


def test_create_user(client):
    res = client.post('/users/', json={
        'email': 'john@gmail.com',
        'password': '123'
    })
    new_user = schemas.UserOut(**res.json())
    assert res.status_code == 201

# é bom clc o -x n comando d pytest p ver o estd d db n hora q deu o erro


def test_login_user(client, test_user):
    res = client.post('/login', data={
        'username': test_user['email'],
        'password': test_user['password']
    })
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token,
                         settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get("user_id")
    assert id == test_user['id']
    assert login_res.token_type == 'bearer'
    assert res.status_code == 200


@pytest.mark.parametrize('email,password,status_code', [
    ('emailErrado', '123', 403),
    ('oie@gmail.com', 'senhaErrado', 403),
    ('emailErrado', 'senhaErrada', 403),
    (None, '123', 422),
    ('oie@gmail.com', None, 422)
])
def test_incorrect_login(test_user, client, email, password, status_code):
    res = client.post(
        '/login', data={'username': email, 'password': password})
    assert res.status_code == status_code
    #assert res.json().get('detail') == 'Invalid Credentials'
