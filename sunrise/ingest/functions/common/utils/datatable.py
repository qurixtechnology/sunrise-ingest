from dataclasses import dataclass
from typing import List, Optional, Dict, Callable, Protocol
from dataclasses import make_dataclass


class DataclassProtocol(Protocol):
    __dataclass_fields__: Dict
    __dataclass_params__: Dict
    __post_init__: Optional[Callable]


@dataclass
class DataColumn:
    name: str
    type: str
    slowly_changing_dimension: bool = False
    soft_scd: bool = False
    source_name: Optional[str] = None
    imported: bool = True
    default_value: str = ""


@dataclass
class DataTable:
    name: str
    schema: str
    columns: List[DataColumn]

    @property
    def db_name(self) -> str:
        return f"{self.schema}.{self.name}"

    @property
    def ddl(self) -> str:
        sql = (
            f"IF OBJECT_ID('{self.db_name}', 'U')"
            + f"IS NULL CREATE TABLE {self.db_name}"
        )
        col_sql = [
            f"{col.name} {col.type}"
            if col.default_value == ""
            else f"{col.name} {col.type} DEFAULT {col.default_value}"
            for col in self.columns
        ]
        return sql + "(" + ", ".join(col_sql) + ")"

    @property
    def import_columns(self) -> List[DataColumn]:
        return [x for x in self.columns if x.imported]

    @property
    def scd(self) -> List[DataColumn]:
        return [x for x in self.columns if x.slowly_changing_dimension]

    @property
    def row_dataclass(self) -> DataclassProtocol:
        """We need to compare immutable objects. For that we use the
        sdc columns to create a row dataclass."""
        name = self.name + "_ROW"
        return make_dataclass(
            cls_name=name,
            fields=[(element.name, element.type) for element in self.scd],
            # unsafe_hash=True,
            frozen=True,
        )
