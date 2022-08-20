from dataclasses import dataclass
from typing import List


@dataclass(init=True)
class FilterParameters:
    pass


class Filter:

    filter_name: str = None
    parameters: dict = {}
    handled_extensions: List[str] = ["txt", "json", "yaml", "yml", "js", "py", "md", ""]

    def __init__(self, filter_name: str) -> None:
        if not filter_name:
            raise ValueError("Invalid filter_name value provided")
        self.filter_name = filter_name

    def process_file(self, file_path: str, parameters: FilterParameters) -> None:
        raise NotImplementedError(
            "You must implement the process method for your filter"
        )
