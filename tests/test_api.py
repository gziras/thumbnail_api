from fastapi.testclient import TestClient
from fastapi import HTTPException

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import Session

from src.database import Base
from src.main import app, get_db
from src.services import get_random_image, generate_unique_link
from src.models import OrientationEnum, ColorEnum
from src.models import ImageMetadata
from src.config import settings
from src.schemas import ImageCreate
from src.crud import create_image_metadata


import pytest
import os

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

def test_service_get_random_image():
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

def test_thumbnail_generation_unique_link_creation(tmpdir):
    # Set up test parameters
    image_data = ImageCreate(search_term="example")  # Replace with actual data if needed
    image_url = "https://upload.wikimedia.org/wikipedia/commons/a/a9/Example.jpg"

    try:
        # Generate the unique link and the thumbnail path
        unique_link = generate_unique_link(image_data, image_url)
        thumbnail_path = os.path.join(settings.thumbnail_directory, unique_link)

        # Ensure that the unique_link is generated correctly
        expected_link = f"{image_data.search_term}_"  # Add the expected format here
        assert unique_link.startswith(expected_link)

        # Ensure that the unique_link contains the expected file extension (e.g., .jpg)
        expected_extension = ".jpg"
        assert unique_link.endswith(expected_extension)
    finally:
        # Delete the thumbnail file after the test
        if thumbnail_path and os.path.exists(thumbnail_path):
            os.remove(thumbnail_path)

def test_create_database_entry():

    db: Session = next(override_get_db())

    # Test data
    image_data = ImageCreate(search_term="dogs", orientation="portrait", color="blue")

    # Call the function with the test data and the test database session
    db_image = create_image_metadata(db, image_data)

    # Ensure that the function creates an entry in the database
    assert db.query(ImageMetadata).filter_by(id=db_image.id).first() is not None

def test_api_search_random_image():
    # Define the test data
    image_data = {
        "search_term": "cats",
        "orientation": "portrait",
        "color": "blue"
    }

    # Send a POST request to the search_random_image route
    response = client.post("/image/random/", json=image_data)

    # Check that the response status code is 200 (OK)
    assert response.status_code == 200

    # Parse the response JSON
    response_data = response.json()

    # Check that the response JSON has the expected structure
    assert "search_term" in response_data
    assert "image_original_url" in response_data
    assert "unique_link" in response_data

def test_get_image_thumbnail_not_found():
    unique_link = "nonexistent_image.jpg"  # Replace with the unique link for a non-existent thumbnail

    response = client.get(f"/image/thumbnail/{unique_link}")
    
    # Assert that the response status code is 404 and the detail message is as expected
    assert response.status_code == 404
    assert response.json() == {"detail": "Thumbnail not found"}