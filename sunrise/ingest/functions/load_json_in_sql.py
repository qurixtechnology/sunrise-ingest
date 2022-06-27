from common.utils.logger import init_logger
from common.data_tables.sales_navigator import STAGE_SALES_NAVIGATOR
from common.data_tables.linkedin_followers import STAGE_LINKEDIN_FOLLOWERS
from common.services.sql import SqlServerClient
from common.utils.processing import batch, DeltaProcessor
import logging


sql_credentials = {
    "SQL_HOST": "sql-dev-sunrise-core.database.windows.net",
    "SQL_DB": "DEV_SUNRISE_DB",
    "SQL_USER": "sunrise_sql_manager",
    "SQL_PASS": "$qurix5070Mr",
}

SOURCES = {
    "LINKEDIN_FOLLOWERS": {
        "file_path": "local/linkedin_followers_2022-06-16.json"
    },
    "SALES_NAVIGATOR": {"file_path": "local/sales_navigator_2022-06-16.json"},
    "COMPANY_FOLLOWERS": {"file_path": ""},
}


if __name__ == "__main__":
    init_logger(azure=False)

    for table in [STAGE_SALES_NAVIGATOR, STAGE_LINKEDIN_FOLLOWERS]:
        file_path = SOURCES[table.name]["file_path"]
        ddl = table.ddl

        db_client = SqlServerClient(
            host=sql_credentials["SQL_HOST"],
            db=sql_credentials["SQL_DB"],
            user=sql_credentials["SQL_USER"],
            pw=sql_credentials["SQL_PASS"],
        )
        db_client.execute_sql(ddl)

        processor = DeltaProcessor(table)
        content = processor.load_local_json(file_path)
        # Execute delta check: load only records that are not in set of slowly changing dimensions in current table

        sql_list = processor.load_dict_to_sql(content)
        for sql_batch in batch(sql_list, 50):
            sql = "; ".join(sql_batch)
            # delta loading
            logging.info(f"{sql[0:10]}[...]")
            db_client.execute_sql(sql)
