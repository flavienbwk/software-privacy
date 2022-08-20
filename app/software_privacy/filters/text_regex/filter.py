import re
from dataclasses import dataclass
from typing import Optional

from software_privacy.filters.filter import Filter


@dataclass(init=True)
class FilterParameters:
    match: Optional[str] = ""
    replace: Optional[str] = ""


class FilterTextRegex(Filter):

    parameters_dc = FilterParameters

    def __init__(self) -> None:
        super().__init__(__name__)

    def process_file(self, file_path: str, parameters: FilterParameters) -> None:
        with open(file_path, 'r') as source_file :
            filedata = source_file.read()
        filedata = re.sub(parameters.match, parameters.replace, filedata, flags = re.M)
        with open(file_path, 'w') as destination_file:
            destination_file.write(filedata)
