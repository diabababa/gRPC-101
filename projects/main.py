from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from shared.db import get_db_session
from shared import crud, schemas

app = FastAPI(title="Location Service REST API")


@app.get("/locations/search", response_model=List[schemas.Location])
async def search(
    latitude: float,
    longitude: float,
    radius: float = 10.0,
    db: AsyncSession = Depends(get_db_session),
):
    return await crud.search_locations(db, latitude, longitude, radius)


@app.get("/locations/{id}", response_model=schemas.Location)
async def get_one(id: int, db: AsyncSession = Depends(get_db_session)):
    loc = await crud.get_location(db, id)
    if not loc:
        raise HTTPException(status_code=404, detail="Location not found")
    return loc


@app.post(
    "/locations", response_model=schemas.Location, status_code=status.HTTP_201_CREATED
)
async def create(
    location: schemas.LocationCreate, db: AsyncSession = Depends(get_db_session)
):
    return await crud.create_location(db, location)


@app.delete("/locations/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove(id: int, db: AsyncSession = Depends(get_db_session)):
    await crud.delete_location(db, id)
    return None


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
