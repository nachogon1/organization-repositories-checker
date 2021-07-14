from pytest import fixture
from starlette.config import environ
from starlette.testclient import TestClient

# Set testing variables.
environ['TESTING'] = 'TRUE'
environ["DB_NAME"] = "yara-test-db"

from configs import DB_NAME
from db.mongodb import get_database


def drop_database():
    db = get_database()
    db.client.drop_database(DB_NAME)


@fixture(scope="function")
def test_client():
    from main import app

    with TestClient(app) as test_client:
        yield test_client
    # Drop the database for each test.
    drop_database()


@fixture
async def db_client():
    from app.core.config import MONGO_DB
    from app.db.mongodb import get_database, connect_database

    await connect_database()

    db = await get_database()
    yield db
    # Teardown
    db.client.drop_database(MONGO_DB)



