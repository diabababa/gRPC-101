"""
gRPC server with async operations.
"""
import logging
import asyncio
from math import radians, cos, sin, asin, sqrt
from datetime import datetime

import grpc
from sqlalchemy import select

from shared import locations_pb2, locations_pb2_grpc
from shared.models import Location
from shared.db import AsyncSessionLocal, init_db, close_db
from shared.config import settings

# Setup logging
logging.basicConfig(level=settings.LOG_LEVEL)
logger = logging.getLogger(__name__)


def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate distance between two points in kilometers."""
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    return c * 6371


def location_to_proto(location: Location) -> locations_pb2.Location:
    """Convert SQLAlchemy Location model to protobuf Location."""
    return locations_pb2.Location(
        id=location.id,
        name=location.name,
        latitude=location.latitude,
        longitude=location.longitude,
        description=location.description,
        type=location.type,
        rating=location.rating,
        review_count=location.review_count,
    )


class LocationServiceServicer(locations_pb2_grpc.LocationServiceServicer):
    """Implementation of LocationService gRPC server."""

    async def SearchLocations(self, request, context):
        """Search locations within a radius (unary RPC)."""
        try:
            async with AsyncSessionLocal() as session:
                result = await session.execute(select(Location))
                locations = result.scalars().all()

                nearby = []
                for loc in locations:
                    distance = haversine_distance(
                        request.latitude,
                        request.longitude,
                        loc.latitude,
                        loc.longitude,
                    )
                    if distance <= request.radius_km:
                        nearby.append((loc, distance))

                nearby.sort(key=lambda x: x[1])
                nearby = nearby[: request.limit]

                reply = locations_pb2.SearchLocationsReply(
                    locations=[location_to_proto(loc) for loc, _ in nearby],
                    total=len(nearby),
                )
                return reply
        except Exception as e:
            logger.error(f"Error in SearchLocations: {e}")
            await context.abort(
                grpc.StatusCode.INTERNAL, f"Internal error: {str(e)}"
            )

    async def GetLocation(self, request, context):
        """Get a single location by ID (unary RPC)."""
        try:
            async with AsyncSessionLocal() as session:
                result = await session.execute(
                    select(Location).where(Location.id == request.id)
                )
                location = result.scalar_one_or_none()

                if not location:
                    await context.abort(
                        grpc.StatusCode.NOT_FOUND, "Location not found"
                    )

                return location_to_proto(location)
        except Exception as e:
            logger.error(f"Error in GetLocation: {e}")
            await context.abort(
                grpc.StatusCode.INTERNAL, f"Internal error: {str(e)}"
            )

    async def CreateLocation(self, request, context):
        """Create a new location (unary RPC)."""
        try:
            async with AsyncSessionLocal() as session:
                location = Location(
                    name=request.name,
                    latitude=request.latitude,
                    longitude=request.longitude,
                    description=request.description,
                    type=request.type,
                )
                session.add(location)
                await session.commit()
                await session.refresh(location)
                return location_to_proto(location)
        except Exception as e:
            logger.error(f"Error in CreateLocation: {e}")
            await context.abort(
                grpc.StatusCode.INTERNAL, f"Internal error: {str(e)}"
            )

    async def UpdateLocation(self, request, context):
        """Update a location (unary RPC)."""
        try:
            async with AsyncSessionLocal() as session:
                result = await session.execute(
                    select(Location).where(Location.id == request.id)
                )
                location = result.scalar_one_or_none()

                if not location:
                    await context.abort(
                        grpc.StatusCode.NOT_FOUND, "Location not found"
                    )

                location.name = request.name
                location.description = request.description
                location.type = request.type

                await session.commit()
                await session.refresh(location)
                return location_to_proto(location)
        except Exception as e:
            logger.error(f"Error in UpdateLocation: {e}")
            await context.abort(
                grpc.StatusCode.INTERNAL, f"Internal error: {str(e)}"
            )

    async def DeleteLocation(self, request, context):
        """Delete a location (unary RPC)."""
        try:
            async with AsyncSessionLocal() as session:
                result = await session.execute(
                    select(Location).where(Location.id == request.id)
                )
                location = result.scalar_one_or_none()

                if not location:
                    await context.abort(
                        grpc.StatusCode.NOT_FOUND, "Location not found"
                    )

                await session.delete(location)
                await session.commit()
                return locations_pb2.Empty()
        except Exception as e:
            logger.error(f"Error in DeleteLocation: {e}")
            await context.abort(
                grpc.StatusCode.INTERNAL, f"Internal error: {str(e)}"
            )

    async def StreamNearbyLocations(self, request, context):
        """Stream nearby locations (server streaming RPC)."""
        try:
            async with AsyncSessionLocal() as session:
                result = await session.execute(select(Location))
                locations = result.scalars().all()

                for loc in locations:
                    distance = haversine_distance(
                        request.latitude,
                        request.longitude,
                        loc.latitude,
                        loc.longitude,
                    )
                    if distance <= request.radius_km:
                        update = locations_pb2.LocationUpdate(
                            location=location_to_proto(loc),
                            timestamp=int(datetime.utcnow().timestamp() * 1000),
                            distance_km=distance,
                        )
                        yield update
                        await asyncio.sleep(0.01)
        except Exception as e:
            logger.error(f"Error in StreamNearbyLocations: {e}")
            await context.abort(
                grpc.StatusCode.INTERNAL, f"Internal error: {str(e)}"
            )

    async def BatchUploadLocations(self, request_iterator, context):
        """Upload multiple locations (client streaming RPC)."""
        try:
            uploaded_count = 0
            failed_count = 0

            async with AsyncSessionLocal() as session:
                async for location_proto in request_iterator:
                    try:
                        location = Location(
                            name=location_proto.name,
                            latitude=location_proto.latitude,
                            longitude=location_proto.longitude,
                            description=location_proto.description,
                            type=location_proto.type,
                        )
                        session.add(location)
                        uploaded_count += 1
                    except Exception as e:
                        logger.warning(f"Failed to process location: {e}")
                        failed_count += 1

                await session.commit()

            return locations_pb2.UploadResponse(
                uploaded_count=uploaded_count,
                failed_count=failed_count,
                message=f"Uploaded {uploaded_count} locations",
            )
        except Exception as e:
            logger.error(f"Error in BatchUploadLocations: {e}")
            await context.abort(
                grpc.StatusCode.INTERNAL, f"Internal error: {str(e)}"
            )

    async def RealTimeLocationSync(self, request_iterator, context):
        """Bidirectional streaming of locations (bidirectional streaming RPC)."""
        try:
            async for location_data in request_iterator:
                try:
                    async with AsyncSessionLocal() as session:
                        # Find nearby locations
                        result = await session.execute(select(Location))
                        locations = result.scalars().all()

                        recommendations = []
                        for loc in locations:
                            distance = haversine_distance(
                                location_data.latitude,
                                location_data.longitude,
                                loc.latitude,
                                loc.longitude,
                            )
                            if distance <= 5.0 and distance > 0:  # Within 5km, exclude self
                                recommendations.append(location_to_proto(loc))
                                if len(recommendations) >= 5:
                                    break

                        response = locations_pb2.SyncResponse(
                            acknowledged=True,
                            message="Location synced",
                            nearby_recommendations=recommendations,
                        )
                        yield response
                except Exception as e:
                    logger.error(f"Error processing sync: {e}")
                    continue
        except Exception as e:
            logger.error(f"Error in RealTimeLocationSync: {e}")
            await context.abort(
                grpc.StatusCode.INTERNAL, f"Internal error: {str(e)}"
            )


async def serve():
    """Start gRPC server."""
    await init_db()

    server = grpc.aio.server()
    locations_pb2_grpc.add_LocationServiceServicer_to_server(
        LocationServiceServicer(), server
    )
    listen_addr = f"{settings.GRPC_HOST}:{settings.GRPC_PORT}"
    server.add_insecure_port(listen_addr)

    logger.info(f"Starting gRPC server on {listen_addr}")
    await server.start()

    try:
        await server.wait_for_termination()
    except KeyboardInterrupt:
        logger.info("Shutting down gRPC server...")
        await server.stop(0)
    finally:
        await close_db()


if __name__ == "__main__":
    asyncio.run(serve())
