# ![Logo of Software Privacy](./software-privacy.png)

[![Dev build](https://github.com/flavienbwk/software-privacy/actions/workflows/build.yaml/badge.svg)](https://github.com/flavienbwk/software-privacy/actions/workflows/build.yaml)
[![Release build](https://github.com/flavienbwk/software-privacy/actions/workflows/release.yaml/badge.svg)](https://github.com/flavienbwk/software-privacy/actions/workflows/release.yaml)
[![Release](https://github.com/flavienbwk/software-privacy/actions/workflows/release.yaml/badge.svg?event=release)](https://github.com/flavienbwk/software-privacy/actions/workflows/release.yaml)
[![MIT license](https://black.readthedocs.io/en/stable/_static/license.svg)](./LICENSE)
[![Code formatter black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Replace sensitive information and avoid personal data in any piece of software or content with programmable filters.

## Usage

```bash
git clone https://github.com/flavienbwk/software-privacy && cd software-privacy
docker pull flavienb/software-privacy:latest

INPUT_PATH=./examples/demo-app \
OUTPUT_PATH=./examples/demo-app-anonymized \
    docker-compose run privacy
```

For demo results, see the [`examples/demo-app-anonymized`](./examples/demo-app-anonymized) directory processed from [`examples/demo-app`](./examples/demo-app).

## Usage (development)

1. Clone the project

    ```bash
    git clone https://github.com/flavienbwk/software-privacy
    ```

2. Copy and edit your privacy filter rules file and build the app

    ```bash
    cp ./rules/rules.example.json ./rules/rules.json
    docker-compose build
    ```

3. Edit paths and run the privacy

    ```bash
    INPUT_PATH=./examples/demo-app \
    OUTPUT_PATH=./examples/demo-app-anonymized \
        docker-compose run privacy
    ```

    :information_source: For idempotence and avoiding any modification in input files, `INPUT_PATH` files are fully copied to `OUTPUT_PATH` before the privacy process starts.

    If you don't want to perform this copy, set the `INPUT_PATH` == `OUTPUT_PATH` and `PERFORM_COPY=false` in the compose configuration. Here's an examle :

    ```bash
    INPUT_PATH=./examples/demo-app \
    OUTPUT_PATH=./examples/demo-app \
    PERFORM_COPY=false \
        docker-compose run privacy
    ```

## Filters

These JSON elements are to be added to your `rules/rules.json` file.

### Text (full-text)

Replace a string in your files by another. Quicker than _regex_ match for full-text replace.

```jsonc
[
    {
        "filter": "text-full",
        "parameters": {
            "match": "myoriginaltext",
            "replace": "mytargettext"
        }
    }
]
```

### Text (regex)

Replace a string in your files by another.

```jsonc
[
    {
        "filter": "text-regex",
        "parameters": {
            "match": "[0-9]{3}",
            "replace": "999"
        }
    }
]
```

### Image similarity

Tries to recognize an image from source image in provided files, and replace it with the provided image at the same size.

This filter tries to guess if the image found is the same than `source_image` and tries to replace it with the same size by `replace_image`. Quality depends on `replace_image` resolution.

```jsonc
[
    {
        "filter": "image-similarity-ssim",
        "parameters": {
            "confidence_threshold": 0.8,
            "source_image": "/usr/inputs/mysourceimage.png",
            "replace_image": "/usr/inputs/myreplaceimage.png"
        }
    }
]
```

### Exif remover

Replace exif metadata in images, audios and videos with [exiftool](https://exiftool.org/).

```jsonc
[
    {
        "filter": "exif-remover"
    }
]
```

## Contributions

Contribute to this repository by optimizing it or adding your own useful filters. Some ideas might be :

- Smart image similarity filter with CLIP
- Smart filter blurrying faces in images
- Smart filter blurrying license plates in images
- Links obfuscator
