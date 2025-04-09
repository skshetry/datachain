import os
import sqlite3
from contextlib import closing

import pytest
import sqlalchemy
from sqlalchemy.orm import Session

from datachain import read_database


@pytest.fixture
def db_path(tmp_dir):
    return tmp_dir / "main.db"


@pytest.fixture
def db_uri(db_path):
    return "sqlite:///" + os.fspath(db_path)


@pytest.fixture
def db_engine(db_uri):
    engine = sqlalchemy.create_engine(db_uri)
    try:
        yield engine
    finally:
        engine.dispose()


@pytest.fixture
def db_connection(db_engine):
    with closing(db_engine.connect()) as conn:
        yield conn


@pytest.fixture
def db_session(db_engine):
    with Session(bind=db_engine) as session:
        yield session


@pytest.fixture
def sqlite3_connection(db_path):
    with sqlite3.connect(db_path) as conn:
        yield conn


@pytest.fixture
def connection(request):
    return request.getfixturevalue(request.param)


@pytest.mark.parametrize(
    "connection",
    (
        "db_uri",
        "db_connection",
        "db_engine",
        "db_session",
        "sqlite3_connection",
    ),
    indirect=True,
)
def test(sqlite3_connection, connection, test_session):
    sqlite3_connection.execute("CREATE TABLE tbl (id INTEGER PRIMARY KEY, value TEXT)")
    sqlite3_connection.executemany(
        "INSERT INTO tbl(value) VALUES(?)", [(str(i),) for i in range(1, 5)]
    )
    sqlite3_connection.commit()

    chain = read_database("select * from tbl", connection, session=test_session)
    assert chain.to_records() == [{"id": i, "value": str(i)} for i in range(1, 5)]
