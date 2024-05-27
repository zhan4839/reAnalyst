# OCR Script for Processing Reverse Engineering Screenshots

This OCR script is designed to automatically upscale images and extract text using Tesseract OCR. It's a part of the reAnalyst framework, aimed at facilitating the scalable analysis of reverse engineering activities. The script processes all `.jpg` images in a specified input directory, upscales them for better OCR accuracy, and outputs extracted text to a specified output directory.

We also provided a hOCR script to generate hOCR files instead of text files, which can be important to determine the exact location of each mouse click.

## Prerequisites

- Python 3.x
- Pillow (PIL Fork)
- Tesseract OCR

Ensure Tesseract OCR is installed on your system and accessible from the command line. You can download it from [Tesseract's GitHub repository](https://github.com/tesseract-ocr/tesseract).

## Installation

1. Clone the repository or download the script to your local machine.
2. Ensure Python 3.x is installed.
3. Install Pillow using pip:

    ```bash
    pip install Pillow
    ```

4. The script is pre-configured with example `input_directory` and `output_directory` paths that contain sample screenshots and their corresponding output text files for demonstration purposes. Feel free to examine these examples to understand the expected input and output format.

## Usage

1. Place all `.jpg` images you wish to process in your `input_directory`.
2. Run the script:

    ```bash
    python OCR.py
    ```

3. Processed text files will be saved in the `output_directory`, with each file named after the original image.

### Configurations

Before running the script, you may want to configure the `input_directory` and `output_directory` in the script to point to your desired folders for processing.

- **input_directory**: Set this variable to the path where your `.jpg` images are stored. An example directory with sample images is provided for quick testing.
- **output_directory**: Set this variable to the path where you want the extracted text files to be saved. An example output directory is included with sample outputs to show how the processed files will appear.


The script includes several Tesseract configurations:

- `--psm 1`: Sets the page segmentation mode to 1, assuming a single block of text.
- `--oem 1`: Uses LSTM OCR Engine.
- Custom configurations to disable dictionaries and set a whitelist for character recognition.

These settings are optimized for the analysis of reverse engineering activities but can be adjusted based on your specific needs.

## Contributing

Contributions to improve the script are welcome. Please follow standard GitHub pull request procedures to submit your improvements.


## Acknowledgments

This script is a part of the reAnalyst framework developed to support the scalable analysis of reverse engineering activities. We appreciate all contributions and feedback from the community.

