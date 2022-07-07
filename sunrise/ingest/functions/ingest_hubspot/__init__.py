import logging

import azure.functions as func
from common.constants import AZURE_FUNCTION_APP_NAME
from common.utils.logger import init_logger

__FUNCTION_NAME__ = "ingest_hubspot"


def main(timer: func.TimerRequest) -> func.HttpResponse:
    """Ingest Hubspot

    Args:
        timer (func.TimerRequest): an Azure Timer Request

    Returns:
        func.HttpResponse: an Azure response object
    """
    init_logger()
    logging.info(
        f"Starting function {__FUNCTION_NAME__} from {AZURE_FUNCTION_APP_NAME}"
    )
    return func.HttpResponse(
        status_code=200,
        body=f"The Service {AZURE_FUNCTION_APP_NAME} is healthy!",
    )
