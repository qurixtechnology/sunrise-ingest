from configs.base import Config
from enum import Enum


class Environment(str, Enum):
    DEV = "dev"
    TEST = "test"
    PROD = "prod"


config = Config()
