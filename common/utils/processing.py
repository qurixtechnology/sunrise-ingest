import json
from abc import ABC, abstractclassmethod
from pathlib import Path
from typing import Callable, Dict, Iterable, List, Optional, Protocol

import pyodbc

from common.utils.datatable import DataTable


class DataclassProtocol(Protocol):
    __dataclass_fields__: Dict
    __dataclass_params__: Dict
    __post_init__: Optional[Callable]


def batch(iterable: Iterable, size: int = 1) -> Iterable:
    for j in range(0, len(iterable), size):
        yield iterable[j: j + size]


class BaseProcessor(ABC):
    @abstractclassmethod
    def run(self):
        raise NotImplementedError


class DeltaProcessor(BaseProcessor):
    def __init__(self, table: DataTable):
        self._table = table

    def load_local_json(self, file_path: Path) -> List[Dict]:
        with open(file_path, "r", encoding="utf-8") as f:
            content = json.load(f)
        return content

    def load_dict_to_sql(
        self, content: List, import_cols: bool = True
    ) -> List[str]:
        sql_list = []
        for content_dict in content:
            placeholders = ", ".join(
                [
                    f"""'{str(element).replace("'", "''")}'"""
                    for element in content_dict.values()
                ]
            )
            columns = ", ".join(content_dict.keys())
            if import_cols:
                columns = ", ".join(
                    [
                        x.name
                        for x in self._table.columns
                        if x.default_value == ""
                    ]
                )
            sql = (
                f"INSERT INTO {self._table.db_name} ( {columns} )"
                + f"VALUES ( N'{placeholders}' )"
            )
            sql_list.append(sql)
        return sql_list

    @staticmethod
    def filter_columns(content: List[Dict], keep_cols: List) -> List[Dict]:
        final_table = []
        for row in content:
            final_table.append({k: v for k, v in row.items()
                                if k in keep_cols})
        return final_table

    def load_sql_table(self, connection: pyodbc.Connection) -> List[Dict]:
        sql = f"SELECT * FROM {self._table.db_name}"
        with connection as conn:
            cursor = conn.cursor().execute(sql)
            columns = [column[0] for column in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]

    def run(
        self, content: List[Dict], connection: pyodbc.Connection
    ) -> List[DataclassProtocol]:
        pass
