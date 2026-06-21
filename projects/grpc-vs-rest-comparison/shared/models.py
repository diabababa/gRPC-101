"""
SQLAlchemy models for the Location Management System.
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Location(Base):
    """Location database model."""

    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    description = Column(Text, nullable=True)
    type = Column(String(100), index=True, nullable=True)  # restaurant, hotel, museum, etc.
    rating = Column(Integer, default=0)
    review_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        """Convert model to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "description": self.description,
            "type": self.type,
            "rating": self.rating,
            "review_count": self.review_count,
        }

    def __repr__(self):
        return f"<Location(id={self.id}, name={self.name}, lat={self.latitude}, lon={self.longitude})>"
