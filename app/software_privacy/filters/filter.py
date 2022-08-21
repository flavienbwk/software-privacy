import asyncio
import sys
from dataclasses import dataclass
from typing import List

from software_privacy.subprocess import run_command
from software_privacy.logger import Logger


@dataclass(init=True)
class FilterParameters:
    pass


class Filter:

    filter_name: str = None
    parameters: dict = {}
    handled_extensions: List[str] = ["txt", "json", "yaml", "yml", "js", "py", "md", ""]
    logger: Logger = None

    def __init__(self, filter_name: str) -> None:
        if not filter_name:
            raise ValueError("Invalid filter_name value provided")
        self.filter_name = filter_name
        self.logger = Logger()

    def system_command(self, cmd: List[str], timeout: int = None) -> int:
        return run_command(cmd, timeout, stdout_logger=self.logger.debug)

    def process_file(self, file_path: str, parameters: FilterParameters) -> None:
        raise NotImplementedError(
            "You must implement the process method for your filter"
        )
