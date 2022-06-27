from configs.settings import config
from common.utils.logger import init_logger
from common.services.phantom_buster import PhantomBusterClient
from datetime import datetime
import json
import logging
from common.sources.phantombuster import LINKEDIN_FOLLOWERS_SOURCE, SALES_NAVIGATOR_SOURCE

if __name__ == "__main__":
    init_logger(azure=False)
    logging.info("Starting import:")
    for source in (SALES_NAVIGATOR_SOURCE, LINKEDIN_FOLLOWERS_SOURCE):
        logging.info(f"Downloading table {source.name}")
        agent_id = source.agent
        storage_folder = source.storage
        org_folder = source.organization_folder

        client = PhantomBusterClient(
            api_key=config.PHANTOM_BUSTER_API_KEY, api_version="v2", organization_id=org_folder
        )
        try:
            result = client.launch(agent_id=agent_id)
        except Exception as e:
            raise e

        result_json = client.fetch_json_result(
            result["containerId"], storage_folder, source.result_file
        )

        document_id = datetime.strftime(datetime.now(), "%Y-%m-%d")

        with open(f"local/{source.name}_{document_id}.json", "w", encoding="utf-8") as f:
            json.dump(result_json, f, indent=4, ensure_ascii=False)

        logging.info(
            f"Document {document_id} was stored in local/{source.name}_{document_id}")
