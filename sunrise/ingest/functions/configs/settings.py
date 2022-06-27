from configs.base import LocalConfig, Config
from enum import Enum


class Environment(str, Enum):
    DEV = "dev"
    TEST = "test"
    PROD = "prod"


ENV = Environment.DEV

if ENV == Environment.DEV:
    config = LocalConfig()
else:
    config = Config()
