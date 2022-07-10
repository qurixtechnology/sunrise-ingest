from enum import Enum

from configs.base import Config


class Environment(str, Enum):
    DEV = "dev"
    TEST = "test"
    PROD = "prod"


config = Config()
