from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Enum as SQLAlchemyEnum
from enum import Enum

from .database import Base


# Define an Enum for valid colors
class ColorEnum(str, Enum):
    black_and_white = "black_and_white"
    black = "black"
    white = "white"
    yellow = "yellow"
    orange = "orange"
    red = "red"
    purple = "purple"
    magenta = "magenta"
    green = "green"
    teal = "teal"
    blue = "blue"


# Define an Enum for valid orientations
class OrientationEnum(str, Enum):
    landscape = "landscape"
    portrait = "portrait"
    squarish = "squarish"


class ImageMetadata(Base):
    __tablename__ = "image_metadata"

    id = Column(Integer, primary_key=True, index=True)
    unique_link = Column(String, unique=True, index=True, nullable=True)
    image_original_url = Column(String, nullable=True)
    search_term = Column(String, index=True)
    color = Column(SQLAlchemyEnum(ColorEnum, nullable=True), index=True)
    orientation = Column(SQLAlchemyEnum(OrientationEnum, nullable=True), index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
