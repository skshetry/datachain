import contextlib
import itertools
import os
import sqlite3
from typing import TYPE_CHECKING, Any, Optional, Union

import sqlalchemy

if TYPE_CHECKING:
    from collections.abc import Iterator, Mapping, Sequence

    from sqlalchemy.orm import FromStatement
    from sqlalchemy.orm import Session as SQLAlchemySession

    from datachain.lib.dc.utils import OutputType
    from datachain.query import Session

    from .datachain import DataChain


QueryType = Union[
    str,
    "sqlalchemy.TextClause",
    "sqlalchemy.Selectable",
    "sqlalchemy.Select",
    "FromStatement",
]
ConnectionType = Union[
    str,
    "sqlalchemy.URL",
    "sqlalchemy.engine.Connectable",
    "sqlite3.Connection",
    "SQLAlchemySession",
]


@contextlib.contextmanager
def _connect(
    connection: ConnectionType,
) -> "Iterator[Union[sqlalchemy.engine.Connection, SQLAlchemySession]]":
    import sqlalchemy.orm

    with contextlib.ExitStack() as stack:
        engine_kwargs = {"echo": bool(os.environ.get("DEBUG_SHOW_SQL_QUERIES"))}
        if isinstance(connection, (str, sqlalchemy.URL)):
            engine = sqlalchemy.create_engine(connection, **engine_kwargs)
            stack.callback(engine.dispose)
            yield stack.enter_context(engine.connect())
        elif isinstance(connection, sqlite3.Connection):
            engine = sqlalchemy.create_engine(
                "sqlite://", creator=lambda: connection, **engine_kwargs
            )
            # do not close the connection, as it is managed by the caller
            yield engine.connect()
        elif isinstance(connection, sqlalchemy.Engine):
            yield stack.enter_context(connection.connect())
        elif isinstance(connection, (sqlalchemy.Connection, sqlalchemy.orm.Session)):
            # do not close the connection, as it is managed by the caller
            yield connection
        else:
            raise TypeError(f"Unsupported connection type: {type(connection).__name__}")


def read_database(
    query: QueryType,
    connection: ConnectionType,
    params: Union["Sequence[Mapping[str, Any]]", "Mapping[str, Any]", None] = None,
    *,
    output: Optional["OutputType"] = None,
    session: Optional["Session"] = None,
    settings: Optional[dict] = None,
    in_memory: bool = False,
    infer_schema_length: int = 100,
) -> "DataChain":
    """
    Generate chain from the database query.

    Args:
        query: SQL query to execute.
        connection : SQLAlchemy connectable, str, or a sqlite3 connection
            Using SQLAlchemy makes it possible to use any DB supported by that
            library. If a DBAPI2 object, only sqlite3 is supported. The user is
            responsible for engine disposal and connection closure for the
            SQLAlchemy connectable; str connections are closed automatically.

    Example:
        ```py
        import datachain as dc

        query = "SELECT key, value FROM table"
        connection = "sqlite:///example.db"
        dc.read_database(query, connection)
        ```
    """

    from datachain.lib.convert.values_to_tuples import values_to_tuples
    from datachain.lib.dc.records import read_records

    if isinstance(query, str):
        query = sqlalchemy.text(query)
    kw = {"execution_options": {"stream_results": True}}  # use server-side cursors
    with _connect(connection) as conn, conn.execute(query, params, **kw) as result:  # type: ignore[arg-type, union-attr]
        rows = list(itertools.islice(result, infer_schema_length))
        cols = result.keys()
        if rows:
            values = {col: [row[idx] for row in rows] for idx, col in enumerate(cols)}
            _, output, _ = values_to_tuples("", output, **values)

        result = itertools.chain(rows, result)  # type: ignore[assignment]
        return read_records(
            (row._asdict() for row in result),
            session=session,
            settings=settings,
            in_memory=in_memory,
            schema=output,  # type: ignore[arg-type]
        )
