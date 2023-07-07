# -*- coding: ascii -*-
u"""
:Copyright:

 Copyright 2023
 Andr\xe9 Malo or his licensors, as applicable

:License:

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.

============
 Test setup
============

Test setup
"""
__author__ = u"Andr\xe9 Malo, Andr\xe9s Reyes Monge"

import time as _time

import docker as _docker
from pytest import fixture

POSTGRES_VERSION = 15
POSTGRES_PASSWORD = "supersecretpassword"
POSTGRES_PORT = 65432
POSTGRES_USER = "postgres"
POSTGRES_DB = "postgres"
POSTGRES_HOST = "127.0.0.1"


@fixture(name='postgres_docker')
def postgres_docker_fixture():
    """Start a postgres DB"""
    client = _docker.from_env()
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
    # (actually I'd use more complex check to wait for container to start but
    # it doesn't really matter)
    _time.sleep(5)

    yield

    container.stop()


@fixture()
def postgres_url(postgres_docker):
    """Return connection URL for DB"""
    # pylint: disable = unused-argument

    yield "postgresql+psycopg2://%s:%s@%s:%s/%s" % (
        POSTGRES_USER,
        POSTGRES_PASSWORD,
        POSTGRES_HOST,
        POSTGRES_PORT,
        POSTGRES_DB,
    )
