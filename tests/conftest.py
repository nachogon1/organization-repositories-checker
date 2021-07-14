from pytest import fixture
from starlette.config import environ
from starlette.testclient import TestClient
import socket


# Get a free port for our fake server.
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 0))
_, port = s.getsockname()
print("PORT", port)
s.close()


@fixture(scope="session")
def httpserver_listen_address():
    return ("localhost", port)

# Set testing variables.
environ['TESTING'] = 'TRUE'
environ["DB_NAME"] = "yara-test-db"
environ["GITHUB_URL"] = f"http://localhost:{port}"

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



