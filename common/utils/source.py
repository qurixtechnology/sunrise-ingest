from dataclasses import dataclass

from configs.phantom_buster import PHANTOM_ORG_FOLDER, PHANTOM_RESULT_BLOB


@dataclass
class PhantomBusterSource:
    name: str
    agent: str
    storage: str
    organization_folder: str = PHANTOM_ORG_FOLDER
    result_file: str = PHANTOM_RESULT_BLOB


@dataclass
class HubSpotSource:
    name: str
