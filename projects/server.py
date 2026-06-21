import asyncio
import grpc
from shared import locations_pb2, locations_pb2_grpc
from shared.db import async_session_factory
from shared import crud
from shared.config import settings


class LocationService(locations_pb2_grpc.LocationServiceServicer):
    async def SearchLocations(self, request, context):
        async with async_session_factory() as db:
            locations = await crud.search_locations(
                db,
                latitude=request.latitude,
                longitude=request.longitude,
                radius=request.radius,
            )

            reply = locations_pb2.SearchLocationsReply()
            for loc in locations:
                reply.locations.add(
                    id=str(loc.id),
                    name=loc.name,
                    latitude=loc.latitude,
                    longitude=loc.longitude,
                )
            return reply

    # Metody streamingowe zostaną zaimplementowane w Fazie 4


async def serve():
    server = grpc.aio.server()
    locations_pb2_grpc.add_LocationServiceServicer_to_server(LocationService(), server)
    server.add_insecure_port(settings.GRPC_SERVER_ADDR)
    print(f"gRPC server starting on {settings.GRPC_SERVER_ADDR}")
    await server.start()
    await server.wait_for_termination()


if __name__ == "__main__":
    try:
        asyncio.run(serve())
    except KeyboardInterrupt:
        pass
