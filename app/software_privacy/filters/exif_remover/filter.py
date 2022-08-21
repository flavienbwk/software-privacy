from dataclasses import dataclass
from PIL import Image

from software_privacy.filters.filter import Filter


@dataclass(init=True)
class FilterParameters:
    pass


class FilterExifRemover(Filter):

    parameters_dc = FilterParameters

    def __init__(self) -> None:
        super().__init__(__name__)
        self.handled_extensions = [
            "jpg",
            "jpeg",
            "png",
            "jp2",
            "gif",
            "mp4",
            "mp3",
            "wav",
            "mov",
            "m4v",
            "3gp",
            "mkv",
        ]

    def process_file(self, file_path: str, parameters: FilterParameters) -> None:
        self.system_command(
            ["exiftool", "-overwrite_original", "-all=", file_path], timeout=30
        )
