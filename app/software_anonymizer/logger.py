import os
import logging
import logging.handlers


class Logger:
    def __init__(self) -> bool:
        formatter = logging.Formatter(
            "%(asctime)s [%(threadName)-12.12s] [%(levelname)s] %(message)s"
        )
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        file_handler = logging.handlers.WatchedFileHandler(
            "/usr/logs/software_privacy.log"
        )
        file_handler.setFormatter(formatter)
        root = logging.getLogger()
        root.setLevel(os.environ.get("LOG_LEVEL", "INFO"))
        root.addHandler(stream_handler)
        root.addHandler(file_handler)
        self.root = root

    def debug(self, message):
        self.root.debug(message)

    def info(self, message):
        self.root.info(message)

    def warning(self, message):
        self.root.warning(message)

    def error(self, message):
        self.root.error(message)

    def critical(self, message):
        self.root.critical(message)
