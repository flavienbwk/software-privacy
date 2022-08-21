from dataclasses import dataclass, replace

import cv2
from software_privacy.filters.filter import Filter


@dataclass(init=True)
class FilterParameters:
    confidence_threshold: float = 0.9
    source_image: str = ""
    replace_image: str = ""


class FilterImageSimilaritySsim(Filter):

    parameters_dc = FilterParameters

    def __init__(self) -> None:
        super().__init__(__name__)
        self.handled_extensions = ["jpg", "jpeg", "png"]

    def process_file(self, file_path: str, parameters: FilterParameters) -> None:
        user_image = cv2.imread(file_path)
        user_image_compare = cv2.cvtColor(user_image, cv2.COLOR_BGR2GRAY)
        user_image_compare = cv2.resize(
            user_image_compare, (256, 256), interpolation=cv2.INTER_AREA
        )
        source_image = cv2.imread(parameters.source_image)
        source_image_compare = cv2.cvtColor(source_image, cv2.COLOR_BGR2GRAY)
        source_image_compare = cv2.resize(
            source_image_compare, (256, 256), interpolation=cv2.INTER_AREA
        )
        similarity = abs(
            cv2.matchTemplate(
                source_image_compare, user_image_compare, cv2.TM_CCOEFF_NORMED
            ).max()
        )
        if similarity >= parameters.confidence_threshold:
            user_image_height, user_image_width, _ = user_image.shape
            replace_image = cv2.imread(parameters.replace_image)
            replace_image = cv2.resize(
                replace_image,
                (user_image_height, user_image_width),
                interpolation=cv2.INTER_AREA,
            )
            cv2.imwrite(file_path, replace_image)
