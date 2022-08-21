import glob
import json
import os
from distutils.dir_util import copy_tree
from typing import List

import tqdm

from software_privacy.filters.exif_remover.filter import FilterExifRemover
from software_privacy.filters.filter import Filter
from software_privacy.filters.image_similarity_ssim.filter import (
    FilterImageSimilaritySsim,
)
from software_privacy.filters.text_full.filter import FilterTextFull
from software_privacy.filters.text_regex.filter import FilterTextRegex
from software_privacy.logger import Logger

INPUT_FILES_PATH = "/usr/input_files"
OUTPUT_FILES_PATH = "/usr/output_files"
RULES_PATH = "/usr/rules/rules.json"
PERFORM_COPY = True if os.environ.get("PERFORM_COPY", "true") == "true" else False

LOGGER = Logger()

AVAILABLE_RULES = {
    "text-full": FilterTextFull,
    "text-regex": FilterTextRegex,
    "image-similarity-ssim": FilterImageSimilaritySsim,
    "exif-remover": FilterExifRemover,
}


def get_rules(rules_path: str) -> List[dict]:
    if not os.path.exists(rules_path):
        return []
    with open(rules_path, "r") as rules_file:
        rules = json.loads(rules_file.read())
        if not isinstance(rules, list):
            return []
        for rule in rules:
            if "filter" not in rule:
                LOGGER.error(f"No filter property in rule={rule}")
                return []
            if rule["filter"] not in AVAILABLE_RULES:
                LOGGER.error(
                    f"Filter {rule['filter']} was not found in available filters"
                )
                return []
        return rules


def perform_validations(rules: List[dict]) -> int:
    LOGGER.debug("Validating rules...")
    if len(rules) == 0:
        LOGGER.error("Invalid rules file. Stopping.")
        return 1
    LOGGER.debug("Valid rules found.")

    LOGGER.debug("Validating input files path...")
    if not os.path.exists(INPUT_FILES_PATH):
        LOGGER.error(f"Invalid files path={INPUT_FILES_PATH}")
        return 1
    LOGGER.debug("Valid files path found.")

    LOGGER.debug("Validating output files path...")
    if not os.path.exists(OUTPUT_FILES_PATH):
        LOGGER.error(f"Invalid files path={OUTPUT_FILES_PATH}")
        return 1
    LOGGER.debug("Valid files path found.")
    return 0


def get_files_from_filter(filter: Filter) -> List:
    handled_extensions = []
    for handled_extension in filter.handled_extensions:
        handled_extensions.append(f"{OUTPUT_FILES_PATH}/**/*.{handled_extension}")
    files_grabbed = []
    for files in handled_extensions:
        files_grabbed.extend(glob.glob(files, recursive=True))
    LOGGER.debug(
        f"Will process {len(files_grabbed)} file{'s' if len(files_grabbed) > 1 else ''}."
    )
    return files_grabbed


def main() -> int:
    """Performs software-privacy strategy.

    Returns:
        int: Exit code
    """
    LOGGER.info("Welcome to software-privacy !")

    rules = get_rules(RULES_PATH)
    validations_rc = perform_validations(rules)
    if validations_rc > 0:
        return validations_rc

    # Perform full files copy
    if PERFORM_COPY:
        LOGGER.info("Starting full copy...")
        copy_tree(INPUT_FILES_PATH, OUTPUT_FILES_PATH)
        LOGGER.info("Finished full copy.")

    # Applying rules one after the other for each file
    for i, rule in enumerate(rules):
        filter_name = rule["filter"]
        LOGGER.info(f"Processing rule {i+1} (filter: {filter_name})...")
        LOGGER.debug(f"Computing files for filter {filter_name}...")
        filter = AVAILABLE_RULES[filter_name]()
        filter_parameters = (
            filter.parameters_dc(**rule["parameters"])
            if "parameters" in rule
            else filter.parameters_dc()
        )
        files = get_files_from_filter(filter)
        for file_path in tqdm.tqdm(files, unit="files"):
            LOGGER.debug(f"Processing file {file_path}...")
            filter.process_file(file_path, filter_parameters)
        LOGGER.info(f"Rule {i+1} (filter: {filter_name}) done.")

    LOGGER.debug(f"Reached program end.")
    return 0
