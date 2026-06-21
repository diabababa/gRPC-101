from pydantic import BaseModel, ConfigDict
from typing import List, Optional


class ReviewBase(BaseModel):
    content: str
    rating: int


class LocationBase(BaseModel):
    name: str
    latitude: float
    longitude: float


class LocationCreate(LocationBase):
    pass


class Location(LocationBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class SearchResult(BaseModel):
    locations: List[Location]


class LocationUpdate(BaseModel):
    name: Optional[str] = None
