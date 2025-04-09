import contextlib
import itertools
import os
import sqlite3
from typing import TYPE_CHECKING, Optional, Union

import sqlalchemy

if TYPE_CHECKING:
    from collections.abc import Iterator, Sequence

    from sqlalchemy.orm import FromStatement
    from sqlalchemy.orm import Session as SQLAlchemySession

    from datachain.lib.dc.utils import OutputType
    from datachain.query import Session

    from .datachain import DataChain


@contextlib.contextmanager
def _execute(
    query: Union[
        str,
        "sqlalchemy.TextClause",
        "sqlalchemy.Selectable",
        "sqlalchemy.Select",
        "FromStatement",
    ],
    connection: Union[
        str,
        "sqlalchemy.URL",
        "sqlalchemy.engine.Connectable",
        "sqlite3.Connection",
        "SQLAlchemySession",
    ],
    params: Union["Sequence", dict] = (),
) -> "Iterator[sqlalchemy.Result]":
    with contextlib.ExitStack() as stack:
        engine_kwargs = {"echo": bool(os.environ.get("DEBUG_SHOW_SQL_QUERIES"))}
        if isinstance(connection, (str, sqlalchemy.URL)):
            engine = sqlalchemy.create_engine(connection, **engine_kwargs)
            stack.callback(engine.dispose)
            connection = stack.enter_context(engine.connect())
        elif isinstance(connection, sqlalchemy.Engine):
            connection = stack.enter_context(connection.connect())
        elif isinstance(connection, sqlite3.Connection):
            engine = sqlalchemy.create_engine(
                "sqlite://", creator=lambda: connection, **engine_kwargs
            )
            connection = engine.connect()

        if isinstance(query, str):
            query = sqlalchemy.text(query)
        execution_options = {"stream_results": True}  # use server-side cursors
        result = connection.execute(  # type: ignore[union-attr]
            query,  # type: ignore[arg-type]
            *(params or ()),
            execution_options=execution_options,
        )
        stack.enter_context(result)
        yield result


def read_database(
    query: Union[
        str,
        "sqlalchemy.TextClause",
        "sqlalchemy.Selectable",
        "sqlalchemy.Select",
        "FromStatement",
    ],
    connection: Union[
        str,
        "sqlalchemy.URL",
        "sqlalchemy.engine.Connectable",
        "sqlite3.Connection",
        "SQLAlchemySession",
    ],
    session: Optional["Session"] = None,
    settings: Optional[dict] = None,
    in_memory: bool = False,
    ds_name: str = "",
    *,
    output: Optional["OutputType"] = None,
    params: Union["Sequence", dict] = (),
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

    with _execute(query, connection, params) as result:
        # use first row to infer schema
        if first_row := result.fetchone():
            _, output, _ = values_to_tuples(
                ds_name,
                output,
                **{col: [v] for col, v in first_row._mapping.items()},
            )
            result = itertools.chain([first_row], result)  # type: ignore[assignment]

        # TODO: How to make this lazy
        return read_records(
            (row._asdict() for row in result),
            session=session,
            settings=settings,
            in_memory=in_memory,
            schema=output,  # type: ignore[arg-type]
        )
