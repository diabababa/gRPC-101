"""
REST API FastAPI server with async operations.
"""
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Query, Body
from fastapi.responses import StreamingResponse
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
import json
import asyncio
from math import radians, cos, sin, asin, sqrt

from shared.models import Location
from shared.db import get_session, init_db, close_db, AsyncSessionLocal
from shared.config import settings

# Setup logging
logging.basicConfig(level=settings.LOG_LEVEL)
logger = logging.getLogger(__name__)


def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees) in kilometers.
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371  # Radius of earth in kilometers
    return c * r


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    logger.info("Starting REST API server...")
    await init_db()
    yield
    # Shutdown
    logger.info("Shutting down REST API server...")
    await close_db()


app = FastAPI(title="REST API - Locations", lifespan=lifespan)


# ==================== UNARY OPERATIONS ====================


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok"}


@app.get("/locations/search")
async def search_locations(
    latitude: float = Query(...),
    longitude: float = Query(...),
    radius_km: float = Query(default=10.0),
    limit: int = Query(default=100),
):
    """
    Search locations within a radius.
    
    Args:
        latitude: Center latitude
        longitude: Center longitude
        radius_km: Search radius in kilometers
        limit: Maximum number of results
    
    Returns:
        List of locations within radius
    """
    async with AsyncSessionLocal() as session:
        try:
            result = await session.execute(select(Location))
            locations = result.scalars().all()

            # Filter by distance
            nearby = []
            for loc in locations:
                distance = haversine_distance(
                    latitude, longitude, loc.latitude, loc.longitude
                )
                if distance <= radius_km:
                    loc_dict = loc.to_dict()
                    loc_dict["distance_km"] = round(distance, 2)
                    nearby.append(loc_dict)

            # Sort by distance and limit
            nearby.sort(key=lambda x: x["distance_km"])
            nearby = nearby[:limit]

            return {"locations": nearby, "total": len(nearby)}
        except Exception as e:
            logger.error(f"Error searching locations: {e}")
            raise HTTPException(status_code=500, detail=str(e))


@app.get("/locations/{location_id}")
async def get_location(location_id: int):
    """Get a single location by ID."""
    async with AsyncSessionLocal() as session:
        try:
            result = await session.execute(
                select(Location).where(Location.id == location_id)
            )
            location = result.scalar_one_or_none()

            if not location:
                raise HTTPException(status_code=404, detail="Location not found")

            return location.to_dict()
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error getting location: {e}")
            raise HTTPException(status_code=500, detail=str(e))


@app.post("/locations")
async def create_location(
    name: str = Body(...),
    latitude: float = Body(...),
    longitude: float = Body(...),
    description: str = Body(default=""),
    type: str = Body(default=""),
):
    """Create a new location."""
    async with AsyncSessionLocal() as session:
        try:
            location = Location(
                name=name,
                latitude=latitude,
                longitude=longitude,
                description=description,
                type=type,
            )
            session.add(location)
            await session.commit()
            await session.refresh(location)
            return location.to_dict()
        except Exception as e:
            await session.rollback()
            logger.error(f"Error creating location: {e}")
            raise HTTPException(status_code=500, detail=str(e))


@app.put("/locations/{location_id}")
async def update_location(
    location_id: int,
    name: str = Body(default=None),
    description: str = Body(default=None),
    type: str = Body(default=None),
):
    """Update a location."""
    async with AsyncSessionLocal() as session:
        try:
            result = await session.execute(
                select(Location).where(Location.id == location_id)
            )
            location = result.scalar_one_or_none()

            if not location:
                raise HTTPException(status_code=404, detail="Location not found")

            if name is not None:
                location.name = name
            if description is not None:
                location.description = description
            if type is not None:
                location.type = type

            await session.commit()
            await session.refresh(location)
            return location.to_dict()
        except HTTPException:
            raise
        except Exception as e:
            await session.rollback()
            logger.error(f"Error updating location: {e}")
            raise HTTPException(status_code=500, detail=str(e))


@app.delete("/locations/{location_id}")
async def delete_location(location_id: int):
    """Delete a location."""
    async with AsyncSessionLocal() as session:
        try:
            result = await session.execute(
                select(Location).where(Location.id == location_id)
            )
            location = result.scalar_one_or_none()

            if not location:
                raise HTTPException(status_code=404, detail="Location not found")

            await session.delete(location)
            await session.commit()
            return {"message": "Location deleted"}
        except HTTPException:
            raise
        except Exception as e:
            await session.rollback()
            logger.error(f"Error deleting location: {e}")
            raise HTTPException(status_code=500, detail=str(e))


# ==================== STREAMING OPERATIONS ====================


@app.get("/locations/stream/nearby")
async def stream_nearby_locations(
    latitude: float = Query(...),
    longitude: float = Query(...),
    radius_km: float = Query(default=10.0),
):
    """
    Server-Sent Events (SSE) streaming of nearby locations.
    """

    async def location_generator():
        try:
            async with AsyncSessionLocal() as session:
                result = await session.execute(select(Location))
                locations = result.scalars().all()

                for loc in locations:
                    distance = haversine_distance(
                        latitude, longitude, loc.latitude, loc.longitude
                    )
                    if distance <= radius_km:
                        loc_dict = loc.to_dict()
                        loc_dict["distance_km"] = round(distance, 2)
                        yield f"data: {json.dumps(loc_dict)}\n\n"
                        await asyncio.sleep(0.01)  # Small delay for streaming effect

                # Send completion marker
                yield f"data: {json.dumps({'type': 'completed'})}\n\n"
        except Exception as e:
            logger.error(f"Error in SSE stream: {e}")
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    return StreamingResponse(location_generator(), media_type="text/event-stream")


@app.post("/locations/batch-upload")
async def batch_upload_locations(locations_data: list = Body(...)):
    """Batch upload multiple locations."""
    async with AsyncSessionLocal() as session:
        try:
            uploaded_count = 0
            failed_count = 0

            for loc_data in locations_data:
                try:
                    location = Location(
                        name=loc_data.get("name"),
                        latitude=loc_data.get("latitude"),
                        longitude=loc_data.get("longitude"),
                        description=loc_data.get("description", ""),
                        type=loc_data.get("type", ""),
                    )
                    session.add(location)
                    uploaded_count += 1
                except Exception as e:
                    logger.warning(f"Failed to add location: {e}")
                    failed_count += 1

            await session.commit()
            return {
                "uploaded_count": uploaded_count,
                "failed_count": failed_count,
                "message": f"Uploaded {uploaded_count} locations",
            }
        except Exception as e:
            await session.rollback()
            logger.error(f"Error in batch upload: {e}")
            raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host=settings.REST_HOST,
        port=settings.REST_PORT,
        workers=4,
    )
