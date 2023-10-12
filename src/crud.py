from sqlalchemy.orm import Session
from . import models, schemas
from .services import get_random_image, generate_unique_link


def create_image_metadata(db: Session, image_data: schemas.ImageCreate):
    # Call the service to get a random image
    image_url = get_random_image(**image_data.dict())
    unique_link = generate_unique_link(image_data, image_url)

    if image_url:
        # Store the image metadata in the database
        db_image = models.ImageMetadata(
            **image_data.dict(), image_original_url=image_url, unique_link=unique_link
        )
        db.add(db_image)
        db.commit()
        db.refresh(db_image)

        return db_image  # Return the database record

    return None
