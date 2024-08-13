import edgedb
import svcs
from edgedb.asyncio_client import AsyncIOClient
from starlette.applications import Starlette


async def _lifespan(app: Starlette, registry: svcs.Registry):
    # EdgeDB client
    db_client = edgedb.create_async_client()

    async def create_db_client():
        yield db_client

    registry.register_factory(AsyncIOClient, create_db_client)

    yield
    await registry.aclose()


def make_lifespan(_lifespan):
    return svcs.starlette.lifespan(_lifespan)


lifespan = make_lifespan(_lifespan)
