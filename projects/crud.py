from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete
from . import models, schemas
import math


async def get_location(db: AsyncSession, location_id: int):
    result = await db.execute(
        select(models.Location).where(models.Location.id == location_id)
    )
    return result.scalars().first()


async def create_location(db: AsyncSession, location: schemas.LocationCreate):
    db_location = models.Location(**location.model_dump())
    db.add(db_location)
    await db.commit()
    await db.refresh(db_location)
    return db_location


async def delete_location(db: AsyncSession, location_id: int):
    await db.execute(delete(models.Location).where(models.Location.id == location_id))
    await db.commit()


async def search_locations(
    db: AsyncSession, latitude: float, longitude: float, radius: float
):
    # Proste filtrowanie "box" zamiast pełnej sferyki dla celów demo wydajności
    # W prawdziwej apce użylibyśmy PostGIS lub funkcji Haversine w SQL
    stmt = select(models.Location)
    result = await db.execute(stmt)
    all_locations = result.scalars().all()

    filtered = []
    for loc in all_locations:
        # Uproszczony dystans euklidesowy
        dist = math.sqrt(
            (loc.latitude - latitude) ** 2 + (loc.longitude - longitude) ** 2
        )
        if dist <= radius:
            filtered.append(loc)
            if len(filtered) >= 100:
                break

    return filtered
