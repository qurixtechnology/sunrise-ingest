from abc import ABC, abstractmethod
import requests
from typing import Dict, List, Optional, Union


class RestClientBase(ABC):
    @abstractmethod
    def __init__(self):
        raise NotImplementedError

    @abstractmethod
    def get(self):
        raise NotImplementedError

    @abstractmethod
    def post(self):
        raise NotImplementedError


class RestClient(RestClientBase):
    def get(self, url: str, headers: Dict, data: Optional[Dict] = None) -> Union[Dict, List]:
        response = requests.get(url, headers=headers, json=data)
        return response.json()

    def post(self, url: str, headers: Dict, data: Optional[Dict] = None) -> Dict:
        response = requests.post(url, headers=headers, json=data)
        return response.json()
