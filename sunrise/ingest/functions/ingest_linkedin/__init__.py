import logging
import azure.functions as func
from common.constants import AZURE_FUNCTION_APP_NAME
from common.services.datalake import DataLakeClient
from common.utils.logger import init_logger
from common.services.phantom_buster import PhantomBusterClient
from configs.settings import config
from configs.phantom_buster import (
    PHANTOM_ORG_FOLDER,
    PHANTOM_RESULT_BLOB,
    PhantomStorageFolder,
    PhantomsAgent,
)
import json
import posixpath

__FUNCTION_NAME__ = "ingest_linkedin"


def main(req: func.HttpRequest) -> func.HttpResponse:
    """Health Function

    Args:
        req (func.HttpRequest): an Azure request

    Returns:
        func.HttpResponse: an Azure response object
    """
    init_logger()
    logging.info(f"Starting function {__FUNCTION_NAME__} from {AZURE_FUNCTION_APP_NAME}")

    datalake_client = DataLakeClient.create_with_az_aad_auth(
        container_name=config.STORAGE_ACCOUNT_CONTAINER, account_name=config.STORAGE_ACCOUNT_NAME
    )

    try:
        client = PhantomBusterClient(
            api_key=config.PHANTOM_BUSTER_API_KEY,
            api_version="v2",
            organization_id=PHANTOM_ORG_FOLDER,
        )
        logging.info("Launching Phantom Buster Job")
        result = client.launch(agent_id=PhantomsAgent.LINKEDIN_FOLLOWERS.value)
    except Exception as e:
        raise Exception(f"Error: {e}") from e

    result_json = client.fetch_json_result(
        result["containerId"], PhantomStorageFolder.LINKEDIN_FOLLOWERS, PHANTOM_RESULT_BLOB
    )

    # Write result to datalake
    document_id = ""
    file_path_upload = posixpath.join(config.RAW_LINKEDIN_DIR_PATH, f"{document_id}.json")
    logging.info(f"Uploading document with id {document_id} to data lake")
    datalake_client.upload_file_content(
        content=json.dumps(result_json, default=str, ensure_ascii=False), file_path=file_path_upload
    )

    logging.info("Function succeeded")
