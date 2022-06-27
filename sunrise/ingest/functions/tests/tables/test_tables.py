import pytest
from common.utils.datatable import DataTable, DataColumn


@pytest.fixture
def asset_table() -> DataTable:
    cols = [DataColumn("sample_col", "VARCHAR(100)")]
    test_table = DataTable(
        name="test_table", schema="test_schema", columns=cols
    )
    return test_table


def test_datatable_data(asset_table: DataTable):
    assert asset_table.name == "test_table"
    assert asset_table.schema == "test_schema"
    assert asset_table.columns[0].name == "sample_col"
    assert asset_table.columns[0].type == "VARCHAR(100)"


def test_table_get_name(asset_table: DataTable):
    assert asset_table.db_name == "test_schema.test_table"


def test_table_ddl(asset_table: DataTable):
    assert (
        asset_table.ddl
        == "IF OBJECT_ID('test_schema.test_table', 'U') IS NULL CREATE TABLE test_schema.test_table(sample_col VARCHAR(100))"
    )
