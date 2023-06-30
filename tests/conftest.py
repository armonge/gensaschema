# conftest.py
import time

import docker
import pytest

POSTGRES_VERSION = 15
POSTGRES_PASSWORD = "supersecretpassword"
POSTGRES_PORT = 65432
POSTGRES_USER = "postgres"
POSTGRES_DB = "postgres"
POSTGRES_HOST = "127.0.0.1"


@pytest.fixture()
def psql_docker():
    client = docker.from_env()
    container = client.containers.run(
        image="postgres:{version}".format(version=POSTGRES_VERSION),
        auto_remove=True,
        environment=dict(
            POSTGRES_PASSWORD=POSTGRES_PASSWORD,
        ),
        name="test_postgres",
        ports={"5432/tcp": (POSTGRES_HOST, POSTGRES_PORT)},
        detach=True,
        remove=True,
    )

    # Wait for the container to start
    # (actually I use more complex check to wait for container to start but it doesn't really matter)
    time.sleep(5)

    yield

    container.stop()


@pytest.fixture()
def docker_postgres_string(psql_docker):
    yield "postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}".format(
        **{
            "user": POSTGRES_USER,
            "password": POSTGRES_PASSWORD,
            "host": POSTGRES_HOST,
            "port": POSTGRES_PORT,
            "db": POSTGRES_DB,
        }
    )
