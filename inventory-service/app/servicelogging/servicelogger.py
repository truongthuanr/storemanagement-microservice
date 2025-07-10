import logging
import sys

def setup_logger(name: str = "inventory-service") -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Tránh tạo nhiều handler nếu gọi nhiều lần
    if not logger.handlers:
        formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] | %(module)s.%(funcName)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        console_handler.flush = sys.stdout.flush

        logger.addHandler(console_handler)

    return logger

logger = setup_logger()
