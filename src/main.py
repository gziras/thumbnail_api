from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from . import models, schemas, crud
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Endpoint to create image metadata and store it in the database
@app.post("/search/random_image/", response_model=schemas.ImageResponse)
def search_random_image(image_data: schemas.ImageCreate, db: Session = Depends(get_db)):
    image_metadata = crud.create_image_metadata(db, image_data)

    if not image_metadata:
        raise HTTPException(status_code=404, detail="No image found")

    return image_metadata


# Define a route to get the image thumbnail by its unique link
@app.get("/image/thumbnail/{unique_link}")
def get_image_thumbnail(unique_link: str):
    # Implement code to locate the thumbnail file by unique_link
    # You should specify the path to the directory where the thumbnails are stored
    thumbnail_path = f"thumbnails/{unique_link}"

    try:
        # Try to return the thumbnail as a file response
        return FileResponse(thumbnail_path, media_type="image/jpeg")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Thumbnail not found")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
