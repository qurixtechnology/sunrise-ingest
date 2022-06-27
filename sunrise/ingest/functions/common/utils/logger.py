import logging


def init_logger(azure: bool = False) -> None:
    logging.basicConfig(level=logging.INFO)
    if azure:
        logging.getLogger("azure")
    else:
        logging.getLogger("main")
