from common.utils.datatable import DataTable, DataColumn
from common.data_tables.sales_navigator import STAGE_SALES_NAVIGATOR
from common.data_tables.linkedin_followers import STAGE_LINKEDIN_FOLLOWERS
from typing import Any, Dict


def utility_test_table(target_table: Any, input_dict: Dict[str, Any]):
    assert isinstance(target_table, DataTable)
    assert all([isinstance(x, DataColumn) for x in target_table.columns])
    assert target_table.db_name == input_dict["table_name"]
    assert len(target_table.columns) == input_dict["columns"]
    assert len([x for x in target_table.columns if x.type == "INT"]) == input_dict["int_cols"]
    assert (
        len([x for x in target_table.columns if "VARCHAR" in x.type]) == input_dict["varchar_cols"]
    )
    assert len([x for x in target_table.columns if x.type == "DATETIME"]) == input_dict["date_cols"]
    assert (
        len([x for x in target_table.columns if x.default_value != ""])
        == input_dict["default_cols"]
    )
    assert len(target_table.import_columns) == input_dict["amount_imported_cols"]


def test_stage_sales_navigator_table():
    input_dict = {
        "table_name": "[SOURCE].SALES_NAVIGATOR",
        "columns": 19,
        "int_cols": 1,
        "varchar_cols": 15,
        "date_cols": 3,
        "default_cols": 1,
        "amount_imported_cols": 18,
    }
    utility_test_table(STAGE_SALES_NAVIGATOR, input_dict)


def test_stage_linkedin_followers():
    input_dict = {
        "table_name": "[SOURCE].LINKEDIN_FOLLOWERS",
        "columns": 7,
        "int_cols": 1,
        "varchar_cols": 4,
        "date_cols": 2,
        "default_cols": 1,
        "amount_imported_cols": 5,
    }
    utility_test_table(STAGE_LINKEDIN_FOLLOWERS, input_dict)
