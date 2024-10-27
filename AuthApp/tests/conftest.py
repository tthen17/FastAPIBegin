import pytest
import uuid
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient
from app.main import app, get_db
from app import models
from app.database import Base

SQLALCHEMY_DATABASE_URL = "postgresql://abdulrahmanalthenayan:postgres@localhost:5432/auth_test" #connecting to postgresdb

engine = create_engine(
    SQLALCHEMY_DATABASE_URL 
)

Base = declarative_base()
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
models.Base.metadata.create_all(bind=engine)

@pytest.fixture(scope="function") #DB connection test fixture
def test_client():
    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture() #generate mock user entry fixture
def user_payload():
    return {
        "username": "pytestusername",
        "email": "testemail@test.com",
        "password": "Testapp@123",
    }

@pytest.fixture() #generate mock update password fixture
def user_payload_updated(user_id):
    return {
        "password": "App@123",
    }