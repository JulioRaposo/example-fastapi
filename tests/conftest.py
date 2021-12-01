from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app import models
from app.main import app
from app.config import settings
from app.database import get_db, Base
from app.oauth2 import create_access_token
import pytest
from alembic import command
# SQLALCHEMY_DATABASE_URL="postgresql://postgres:Raposo14@localhost:5432/fastapi_test"
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'
engine = create_engine(SQLALCHEMY_DATABASE_URL)
# objt d session q ns dx conectar ao db
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)
# Base.metadata.create_all(bind=engine)
# #Base = declarative_base()


# def override_get_db():
#     db = TestingSessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


#client = TestClient(app)


@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):

    # roda o cod antes d rodar nss teste
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db

    # command.upgrade('head')
    yield TestClient(app)  # yield é o msm q return
    # command.downgrade('base')
    # roda o cod dps d rodar nss teste


@pytest.fixture
def test_user(client):
    user_data = {
        "email": "oie@gmail.com",
        "password": "123"
    }
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user


@pytest.fixture
def test_user2(client):
    user_data = {
        "email": "oiee@gmail.com",
        "password": "123"
    }
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token({'user_id': test_user['id']})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client


@pytest.fixture
def test_posts(test_user, session, test_user2):
    posts_data = [{
        "title": "first title",
        "content": "first content",
        "owner_id": test_user['id']
    }, {
        "title": "2nd title",
        "content": "2nd content",
        "owner_id": test_user['id']
    },
        {
        "title": "3rd title",
        "content": "3rd content",
        "owner_id": test_user['id']
    }, {
        "title": "3rd title",
        "content": "3rd content",
        "owner_id": test_user['id']
    }, {
        "title": "4rd title",
        "content": "4rd content",
        "owner_id": test_user2['id']
    }]

    def create_post_model(post):
        return models.Post(**post)
    post_map = map(create_access_token, posts_data)
    posts = list(post_map)
    session.add_all(posts)
    session.commit()
    posts = session.query(models.Post).all()
    return posts
