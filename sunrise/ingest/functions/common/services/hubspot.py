from typing import Dict

from common.services.rest import RestClient


class HubspotClient(RestClient):
    _BASE_URL = "https://api.hubapi.com/crm/v3/"

    def __init__(self, api_key: str, api_version: str):
        super().__init__(api_key, api_version)

    def _get_headers() -> Dict:
        return {}
