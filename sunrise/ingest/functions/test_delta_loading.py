import logging

from dataclasses import asdict
from common.utils.processing import DeltaProcessor
from common.services.sql import SqlServerClient
from common.utils.logger import init_logger
from common.data_tables.linkedin_followers import (
    STAGE_LINKEDIN_FOLLOWERS,
    ROW_STAGE_LINKEDIN_FOLLOWERS,
)
from typing import Union, Dict, List
from pathlib import Path
import json

sql_credentials = {
    "SQL_HOST": "sql-dev-sunrise-core.database.windows.net",
    "SQL_DB": "DEV_SUNRISE_DB",
    "SQL_USER": "sunrise_sql_manager",
    "SQL_PASS": "$qurix5070Mr",
}


def main():

    table_to_import = STAGE_LINKEDIN_FOLLOWERS
    processor = DeltaProcessor(table_to_import)

    db_client = SqlServerClient(
        host=sql_credentials["SQL_HOST"],
        db=sql_credentials["SQL_DB"],
        user=sql_credentials["SQL_USER"],
        pw=sql_credentials["SQL_PASS"],
    )
    table = processor.load_sql_table(connection=db_client.connection)
    final_table = processor.filter_columns(
        table, [x.name for x in table_to_import.scd]
    )
    unique_records_from_scd = [
        ROW_STAGE_LINKEDIN_FOLLOWERS(**row) for row in final_table
    ]

    logging.info(f"Existing records in database {len(unique_records_from_scd)}")

    content = processor.load_local_json(
        "local/linkedin_followers_2022-06-24.json"
    )

    logging.info(f"Possible new records from content {len(content)}")

    content = processor.filter_columns(
        content,
        [
            x.source_name
            for x in table_to_import.columns
            if x.slowly_changing_dimension
        ],
    )

    # Change names of imported content
    map_import_db_col = {
        x.source_name: x.name
        for x in table_to_import.columns
        if x.slowly_changing_dimension
    }

    new_content = []
    for element in content:
        new_dict = {}
        for key, value in element.items():
            new_dict[map_import_db_col[key]] = value
            new_content.append(new_dict)

    hashable_content = [
        ROW_STAGE_LINKEDIN_FOLLOWERS(**row) for row in new_content
    ]

    # Naive
    new_records = []
    for element in hashable_content:
        if element not in unique_records_from_scd:
            new_records.append(element)

    new_records_amount = len(new_records)
    if new_records_amount > 0:
        logging.info(f"New records found: {new_records_amount}")
    else:
        logging.info("No new records found. Skipping import")

    # Optimized: hashable dataclasses
    hashable_try_subset = set(unique_records_from_scd) - set(hashable_content)
    dump_file(
        [asdict(x) for x in hashable_try_subset], Path("local/hashable.json")
    )
    logging.info(f"Hashable try: {len(hashable_try_subset)}")

    return None


def dump_file(content: Union[Dict, List], file_path: Path) -> None:
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(json.dumps(content, ensure_ascii=False))


if __name__ == "__main__":
    init_logger()
    main()
    # res = main()
    # res_2 = main()
    # print(res[0:1])
    # print(res[0] == res_2[0])
    # test_dynamic_dataclasses()
