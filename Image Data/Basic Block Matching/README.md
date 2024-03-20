# Basic Block Analysis Feature for reAnalyst

The Basic Block Analysis feature is a comprehensive solution for extracting, analyzing, and matching basic blocks from binary analysis screenshots. This process involves creating a database of basic blocks, cropping relevant images for OCR, re-processing these images through OCR, and matching the OCR output against the basic block database.

## Overview

1. **`iterate.py`**: Generates a database of basic blocks from a binary, assigning names to unnamed blocks.
2. **`crop.py`**: Crops images to focus on the relevant areas for OCR.
3. **OCR Processing**: Processes the cropped images through OCR to extract text.
4. **`basic_block_match.py`**: Matches OCR text to basic blocks in the database.

## Prerequisites

- IDA Pro or another disassembler for running `iterate.py`.
- Python 3.x for running the scripts.
- OpenCV (`cv2` module) for image processing in `crop.py`.
- An OCR tool or library for processing images after cropping (we recommend using the OCR tool we provided in our framework, which has been configured to work with this type of screenshots)
- Fuzzy matching library (`difflib` or `python-Levenshtein`) for `basic_block_match.py`.
- Successful function matching data in JSON format, as a result of prior analysis stages. This data is crucial for mapping OCR outputs to specific functions within the binary analysis process.

## Installation

1. Ensure Python 3.x and IDA Pro (or another disassembler) are installed on your system.
2. Install necessary Python libraries:

    ```bash
    pip install opencv-python fuzzywuzzy python-Levenshtein
    ```

3. Clone this repository or download the scripts directly to your local machine.

## Step-by-Step Guide

### Step 1: Generate Basic Block Database

- Run `iterate.py` within IDA Pro on each binary file to create a basic block database. This script assigns unique names to unnamed blocks and saves the database to a text file.

    - Example command in IDA Pro's scripting console or environment:

        ```bash
        Python> exec(open("iterate.py").read())
        ```

- Output: A text file (`basicblockoutput.txt`) containing the basic block database.

### Step 2: Crop Images

- Place your binary analysis screenshots in a designated folder.
- Run `crop.py` to automatically crop these images, focusing on the areas containing basic blocks.

    ```bash
    python crop.py
    ```

- Output: Cropped images saved in a specified output directory.

### Step 3: OCR Processing

- Use an OCR tool (such as the OCR tool we provided) to process the cropped images and extract text. This step might vary based on the OCR tool or library you're using. The goal is to obtain text files containing the OCR output for each cropped image.

### Step 4: Match OCR Output to Basic Blocks

- Run `basic_block_match.py` to match the OCR text files to the basic blocks database generated in Step 1.

    ```bash
    python basic_block_match.py
    ```

- Output: Text or JSON files indicating the matching results between the OCR output and the basic blocks in your database.

## Contributing

We welcome contributions to improve the Basic Block Analysis feature. If you have suggestions for enhancements or have identified issues, please submit a pull request or issue through GitHub.

## License

This project is licensed under [Your License Choice]. See the LICENSE file for more details.

## Acknowledgments

This feature is part of the reAnalyst project, aimed at enhancing reverse engineering analysis methodologies. We thank all contributors and users for their support and feedback.

