from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from src.database import Base
from src.main import app, get_db
from src.services import get_random_image
from src.models import OrientationEnum, ColorEnum
from src.config import settings
import pytest

SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_health_route():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_get_random_image():
    search_term = "dogs"
    orientation = OrientationEnum.portrait
    color = ColorEnum.blue

    # Call the get_random_image function
    image_url = get_random_image(search_term, orientation, color)

    # Ensure that image_url is either None (no image found) or a valid URL
    assert image_url is None or image_url.startswith("http")

def test_get_random_image_nonexistent():
    search_term = "asdfihoqwetgnoqgqweg"
    orientation = None
    color = None

    # Call the get_random_image function
    image_url = get_random_image(search_term, orientation, color)

    # Ensure that image_url is either None (no image found) or a valid URL
    assert image_url is None

def test_unsplash_is_down(monkeypatch):
    # Define a function to set an invalid API URL
    def set_invalid_api_url():
        settings.unsplash_api_url = "https://invalid-api-url.example.com"

    # Replace the API URL with an invalid one during the test
    monkeypatch.setattr(settings, "unsplash_api_url", "https://invalid-api-url.example.com")

    # Ensure that the test case uses the modified API URL
    set_invalid_api_url()

    search_term = "dogs"
    orientation = OrientationEnum.portrait
    color = ColorEnum.blue

    with pytest.raises(Exception, match="API request failed:"):
        get_random_image(search_term, orientation, color)

    # Reset the API URL to its original value after the test
    monkeypatch.undo()