# ![Logo of Software Privacy](./software-privacy.png)

[![Dev build](https://github.com/flavienbwk/software-privacy/actions/workflows/build.yaml/badge.svg)](https://github.com/flavienbwk/software-privacy/actions/workflows/build.yaml)
[![Release build](https://github.com/flavienbwk/software-privacy/actions/workflows/release.yaml/badge.svg)](https://github.com/flavienbwk/software-privacy/actions/workflows/release.yaml)
[![Release](https://github.com/flavienbwk/software-privacy/actions/workflows/release.yaml/badge.svg?event=release)](https://github.com/flavienbwk/software-privacy/actions/workflows/release.yaml)

Replace sensitive information and avoid personal data in any piece of software or content with programmable filters.

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

### Image

Tries to recognize an image from source image in all image files, and replace it with the provided image at the same size.

This filter tries [to guess](https://stackoverflow.com/questions/69338654/find-similar-image-if-resolution-was-changed) if the image found is the same than `source_image` and tries to replace it with the same size by `replace_image`. Quality depends on `replace_image` resolution.

```jsonc
[
    {
        "filter": "image",
        "parameters": {
            "confidence_threshold": 0.9,
            "source_image": "/inputs/mysourceimage.png",
            "replace_image": "/inputs/myreplaceimage.png"
        }
    }
]
```

## Contributions

Contribute to this repository by optimizing it or adding your own useful filters. Some ideas might be :

- Smart image similarity filter with CLIP
- Smart filter blurrying faces in images
- Smart filter blurrying license plates in images
- Links obfuscator
