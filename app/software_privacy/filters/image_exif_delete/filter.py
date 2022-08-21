from dataclasses import dataclass
from PIL import Image

from software_privacy.filters.filter import Filter


@dataclass(init=True)
class FilterParameters:
    pass


class FilterImageExifDelete(Filter):

    parameters_dc = FilterParameters

    def __init__(self) -> None:
        super().__init__(__name__)
        self.handled_extensions = ["jpg", "jpeg", "png", "jp2", "gif"]

    def process_file(self, file_path: str, parameters: FilterParameters) -> None:
        image = Image.open(file_path)
        data = list(image.getdata())
        image_without_exif = Image.new(image.mode, image.size)
        image_without_exif.putdata(data)
        image_without_exif.save(file_path)
