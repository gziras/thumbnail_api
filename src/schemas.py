from pydantic import BaseModel
from typing import Optional
from .models import ColorEnum, OrientationEnum
from datetime import datetime


class ImageCreate(BaseModel):
    search_term: str
    color: Optional[ColorEnum] = None
    orientation: Optional[OrientationEnum] = None


class ImageResponse(ImageCreate):
    image_original_url: str
    unique_link: str  # Include unique_link in the response
    created_at: datetime
