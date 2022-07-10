import os

from pydantic import BaseSettings


class LocalConfig(BaseSettings):
    HUBSPOT_API_KEY: str
    PHANTOM_BUSTER_API_KEY: str
    STORAGE_ACCOUNT_NAME: str
    STORAGE_ACCOUNT_CONTAINER: str
    RAW_LINKEDIN_DIR_PATH: str

    class Config:
        env_file = ".env"


class Config(BaseSettings):
    HUBSPOT_API_KEY: str = os.environ.get(
        "HUBSPOT_API_KEY"
    )
    PHANTOM_BUSTER_API_KEY: str = os.environ.get(
        "PHANTOM_BUSTER_API_KEY"
    )

    # Datalake Connection Config
    STORAGE_ACCOUNT_NAME: str = os.environ.get(
        "STORAGE_ACCOUNT_NAME"
    )
    STORAGE_ACCOUNT_CONTAINER: str = os.environ.get(
        "STORAGE_ACCOUNT_CONTAINER"
    )

    # Directory Configs
    RAW_LINKEDIN_DIR_PATH: str = os.environ.get(
        "RAW_LINKEDIN_DIR_PATH"
    )
