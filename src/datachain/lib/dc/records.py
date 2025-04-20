from collections.abc import Iterable
from typing import TYPE_CHECKING, Any, Optional, Union

import sqlalchemy

from datachain.lib.data_model import DataType
from datachain.lib.file import File
from datachain.lib.signal_schema import SignalSchema
from datachain.query import Session

if TYPE_CHECKING:
    from typing_extensions import ParamSpec

    from datachain.data_storage.warehouse import AbstractWarehouse
    from datachain.sql.types import SQLType

    from .datachain import DataChain

    P = ParamSpec("P")


def _adjust_records(
    warehouse: "AbstractWarehouse",
    records: list[Any],
    column_types: dict[str, "SQLType"],
) -> Iterable[dict[str, Any]]:
    for record in records:
        yield {
            k: col.default_value(warehouse.db.dialect)
            if v is None and (col := column_types.get(k))
            else v
            for k, v in record.items()
        }


def read_records(
    to_insert: Optional[Union[dict, Iterable[dict]]],
    session: Optional[Session] = None,
    settings: Optional[dict] = None,
    in_memory: bool = False,
    schema: Optional[dict[str, DataType]] = None,
) -> "DataChain":
    """Create a DataChain from the provided records. This method can be used for
    programmatically generating a chain in contrast of reading data from storages
    or other sources.

    Parameters:
        to_insert : records (or a single record) to insert. Each record is
                    a dictionary of signals and theirs values.
        schema : describes chain signals and their corresponding types

    Example:
        ```py
        import datachain as dc
        single_record = dc.read_records(dc.DEFAULT_FILE_RECORD)
        ```
    """
    from datachain.sql.types import SQLType

    from .datasets import read_dataset

    session = Session.get(session, in_memory=in_memory)
    catalog = session.catalog

    name = session.generate_temp_dataset_name()
    signal_schema = None
    columns: list[sqlalchemy.Column] = []

    if schema:
        signal_schema = SignalSchema(schema)
        columns = [
            sqlalchemy.Column(c.name, c.type)  # type: ignore[union-attr]
            for c in signal_schema.db_signals(as_columns=True)
        ]
    else:
        columns = [
            sqlalchemy.Column(name, typ)
            for name, typ in File._datachain_column_types.items()
        ]

    dsr = catalog.create_dataset(
        name,
        columns=columns,
        feature_schema=(
            signal_schema.clone_without_sys_signals().serialize()
            if signal_schema
            else None
        ),
    )

    session.add_dataset_version(dsr, dsr.latest_version)

    if isinstance(to_insert, dict):
        to_insert = [to_insert]
    elif not to_insert:
        to_insert = []

    warehouse = catalog.warehouse
    dr = warehouse.dataset_rows(dsr)
    table = dr.get_table()
    records = _adjust_records(
        warehouse,
        to_insert,  # type: ignore[arg-type]
        {c.name: c.type for c in columns if isinstance(c.type, SQLType)},
    )
    warehouse.insert_rows(table, records)
    warehouse.insert_rows_done(table)
    return read_dataset(name=dsr.name, session=session, settings=settings)
