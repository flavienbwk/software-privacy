import re
from dataclasses import dataclass
from typing import Optional
from PIL import Image
from skimage.metrics import structural_similarity as ssim

from software_privacy.filters.filter import Filter


@dataclass(init=True)
class FilterParameters:
    source_image: Optional[str] = ""
    replace_image: Optional[str] = ""


class FilterImageSimilaritySsim(Filter):

    parameters_dc = FilterParameters

    def __init__(self) -> None:
        super().__init__(__name__)
        self.handled_extensions = ["jpg", "jpeg", "png"]

    def process_file(self, file_path: str, parameters: FilterParameters) -> None:
        with Image.open(file_path) as user_image:
            user_image.resize(
                (256, 256), resample=Image.Resampling.NEAREST, box=None, reducing_gap=None
            )
        with Image.open(parameters.source_image) as source_image:
            source_image.resize(
                (256, 256), resample=Image.Resampling.NEAREST, box=None, reducing_gap=None
            )
        s = ssim(user_image, source_image)
        print(f"Similarity is s={s}")
