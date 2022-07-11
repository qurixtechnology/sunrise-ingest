import json
import logging
import posixpath
from datetime import datetime

import azure.functions as func

from common.constants import AZURE_FUNCTION_APP_NAME
from common.services.datalake import DataLakeClient
from common.services.phantom_buster import PhantomBusterClient
from common.sources.phantombuster import LINKEDIN_FOLLOWERS_SOURCE
from common.utils.logger import init_logger
from common.utils.source import PhantomBusterSource
from configs.settings import config

__FUNCTION_NAME__ = "ingest_linkedin"


def main(req: func.timer.TimerRequest) -> func.HttpResponse:
    """Ingest Linkedin

    Args:
        timer (func.TimerRequest): an Azure Timer Request

    Returns:
        func.HttpResponse: an Azure response object
    """
    init_logger(azure=True)

    logging.info(
        f"Starting function {__FUNCTION_NAME__} from {AZURE_FUNCTION_APP_NAME}"
    )

    datalake_client: DataLakeClient = DataLakeClient.create_with_az_aad_auth(
        container_name=config.STORAGE_ACCOUNT_CONTAINER,
        account_name=config.STORAGE_ACCOUNT_NAME,
    )
    source: PhantomBusterSource = LINKEDIN_FOLLOWERS_SOURCE
    linkedin_raw_path = config.RAW_LINKEDIN_DIR_PATH

    try:
        client = PhantomBusterClient(
            api_key=config.PHANTOM_BUSTER_API_KEY,
            api_version="v2",
            organization_id=source.organization_folder,
        )

        logging.info("Launching Phantom Buster Job")
        result = client.launch(agent_id=source.agent)

        logging.info(
            f"Downloading {source.name} data from PB container: " +
            f"{result['containerId']}"
        )

        result_json = client.fetch_json_result(
            container_id=result["containerId"],
            organization_folder=source.storage,
            result_blob=source.result_file)

        now = datetime.strftime(datetime.now(), "%Y-%m-%d")

        document_name = f"{source.name}_{now}.json"

        file_path_upload = posixpath.join(
            linkedin_raw_path,
            document_name,)
        logging.info(f"Uploading document with id {document_name}" +
                     " to data lake")
        datalake_client.upload_file_content(
            content=json.dumps(result_json, default=str, ensure_ascii=False),
            file_path=file_path_upload,
        )

        return func.HttpResponse(
            status_code=200,
            body=f"Document {document_name} was uploaded!",
        )

    except Exception as e:
        return func.HttpResponse(
            f"Error: {e}",
            status_code=500
        )
