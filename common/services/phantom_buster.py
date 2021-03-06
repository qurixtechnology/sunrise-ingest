import logging
import time
from typing import Dict, Optional
from urllib.parse import urljoin

from common.services.rest import RestClient


class PhantomBusterClient(RestClient):
    """Client to make http calls to Phantom Buster"""

    _BASE_URL = "https://api.phantombuster.com/api"
    _BASE_BUCKET_URL = "https://phantombuster.s3.amazonaws.com"

    def __init__(self, api_key: str, api_version: str, organization_id: str):
        self._api_key = api_key
        self._api_version = api_version
        self._organization_id = organization_id
        self._base_url = self._BASE_URL + "/" + api_version
        self.log = logging.getLogger(self.__class__.__name__)

    def _get_headers(self) -> Dict:
        return {
            "Content-Type": "application/json",
            "X-Phantombuster-Key": self._api_key,
            "Accept": "application/json",
        }

    def launch(self, agent_id: str) -> Dict:
        agent_data = {"id": agent_id}
        url = f"{self._base_url}/agents/launch"
        result = self.post(
            url=url, headers=self._get_headers(), data=agent_data
        )
        self.log.debug(result)
        if result and result.get("status") != "error":
            self.log.info("Authentication successful")
        else:
            self.log.error("Error: something happened.")
            raise Exception(f"See {result.get('error', 'key error')}")
        return result

    def get_container_output(self, container_id: str) -> Optional[Dict]:
        url = (
            f"{self._base_url}/containers/"
            + f"fetch-output?id={container_id}&mode=json"
        )
        result = self.get(url, self._get_headers())
        return result

    def get_container_result_object(self, container_id: str) -> Dict:
        url = urljoin(self._base_url, f"fetch-result-object?id={container_id}")
        response = self.get(url, headers=self._get_headers())
        return response

    def get_result(self, organization_folder: str, result_blob: str) -> Dict:
        url = (
            f"{self._BASE_BUCKET_URL}/{self._organization_id}"
            + f"/{organization_folder}/{result_blob}"
        )
        result = self.get(url, self._get_headers())
        return result

    def fetch_json_result(
        self, container_id: str, organization_folder: str, result_blob: str
    ) -> Dict:
        attempts = 0
        wait = 45
        while attempts <= 4:
            try:
                self.log.debug(f"Attempt: {attempts+1}")
                output = self.get_container_output(container_id)["output"]
                if output in (None, "output"):
                    raise KeyError("Phantom Buster results are not yet ready")
                result = self.get_result(organization_folder, result_blob)
                return result
            except KeyError as e:
                attempts += 1
                self.log.debug(
                    f"Client Error: {e}. Phantom is running. Waiting {wait}"
                    + "seconds"
                )
                time.sleep(wait)
