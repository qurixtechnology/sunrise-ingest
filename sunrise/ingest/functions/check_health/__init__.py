import azure.functions as func
from common.constants import AZURE_FUNCTION_APP_NAME


def main(req: func.HttpRequest) -> func.HttpResponse:
    """Health Function

    Args:
        req (func.HttpRequest): an Azure request

    Returns:
        func.HttpResponse: an Azure response object
    """
    return func.HttpResponse(
        status_code=200,
        body=f"The service {AZURE_FUNCTION_APP_NAME} is healthy!",
    )
