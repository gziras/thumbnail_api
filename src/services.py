import requests
import random
from .models import ColorEnum, OrientationEnum
from PIL import Image
from io import BytesIO
import os
import uuid
from .config import settings
from fastapi import HTTPException


def build_unsplash_request_params(search_term, orientation, color):
    # Validate orientation and color parameters using ENUMs
    if orientation and orientation in OrientationEnum:
        unsplash_orientation = orientation.value
    else:
        unsplash_orientation = None
    if color and color in ColorEnum:
        unsplash_color = color.value
    else:
        unsplash_color = None

    params = {
        "client_id": settings.unsplash_access_key,
        "query": search_term,
    }
    if unsplash_orientation:
        params["orientation"] = unsplash_orientation
    if unsplash_color:
        params["color"] = unsplash_color

    return params


def get_total_count(search_term, orientation=None, color=None):
    params = build_unsplash_request_params(search_term, orientation, color)

    try:
        response = requests.get(settings.unsplash_api_url, params=params)
        response.raise_for_status()
        data = response.json()

        total_count = data.get("total", 0)
        return total_count

    except requests.exceptions.RequestException as e:
        raise Exception(f"API request failed: {e}")


def get_random_image(search_term, orientation=None, color=None):
    total_count = get_total_count(search_term, orientation, color)

    if total_count == 0:
        return None

    # Choose a random page number between 1 and the minimun of 200, total_count.
    # Over 200 seems to return an empty json.
    random_page = random.randint(1, min(total_count, 200))
    params = build_unsplash_request_params(search_term, orientation, color)
    params["page"] = random_page
    params["per_page"] = 1

    try:
        response = requests.get(settings.unsplash_api_url, params=params)
        response.raise_for_status()
        data = response.json()

        # Extract the image URL from the API response
        if data.get("results"):
            image_url = data["results"][0]["urls"]["regular"]
            return image_url

        return None  # No results found

    except requests.exceptions.RequestException as e:
        raise Exception(f"API request failed: {e}")


def create_thumbnail(image_url, thumbnail_path, thumbnail_size=(100, 100)):
    try:
        # Send a GET request to the image URL
        response = requests.get(image_url)
        response.raise_for_status()

        # Open the image and create a PIL Image object
        image = Image.open(BytesIO(response.content))

        # Create a thumbnail
        image.thumbnail(thumbnail_size)

        # Save the thumbnail locally
        image.save(thumbnail_path, "JPEG")

        return True  # Success
    except Exception as e:
        print(f"Error creating thumbnail: {e}")
        return False


def generate_unique_link(image_data, image_url):
    if image_url:
        # Create a unique link
        unique_link = f"{image_data.search_term}_{uuid.uuid4()}.jpg"
        thumbnail_path = os.path.join(settings.thumbnail_directory, unique_link)

        # Attempt to create and save the thumbnail using the services function
        if create_thumbnail(image_url, thumbnail_path):
            return unique_link
        else:
            raise Exception("Failed to create the unique link")
    else:
        raise HTTPException(
            status_code=404, detail="No image found for the provided search term"
        )
