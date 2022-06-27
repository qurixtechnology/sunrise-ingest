import logging


def init_logger(azure: bool = False) -> None:
    logging.basicConfig(level=logging.INFO)
    if azure:
        logger = logging.getLogger("azure")
    else:
        logger = logging.getLogger("main")
