# reAnalyst: A Comprehensive Reverse Engineering Analysis Framework

reAnalyst is a versatile framework designed to automate and enhance the analysis of reverse engineering activities. This framework combines both image and non-image data processing tools to provide a detailed analysis of reverse engineering experiments. Its modular design allows for the analysis of function and basic block matching from binary screenshots, as well as the extraction and analysis of non-image data such as keystrokes and window interactions.

## Overview

reAnalyst is structured into two main categories:

- **Image Data**: Tools and scripts for processing screenshots from reverse engineering sessions, including function and basic block matching, and additional features such as scatter graph generation and key symbols extraction.
- **Non-image Data**: Scripts for analyzing non-visual data extracted during reverse engineering tasks, such as keystroke logs, process events, and window focus changes.

### Image Data
- **OCR**: Script for Optical Character Recognition (OCR) processing, converting screenshots into text for
- **Function Matching**: Identifies functions within binary analysis screenshots, using symbol mappings and OCR data.
- **Basic Block Matching**: Extracts and matches basic blocks from disassembler screenshots, facilitating detailed reverse engineering analysis.
- **Extra Features**: Additional tools for enhancing image data analysis, including scatter graph visualization and key symbols extraction.
 further analysis.

### Non-image Data

- Analysis tools for processing keystrokes, window changes, and process lifecycles, providing insights into the reverse engineering process beyond visual data.

## Getting Started

To get started with reAnalyst, clone this repository and navigate to the respective directory for image or non-image data analysis. Follow the `README.md` instructions within each subdirectory for specific setup and usage guidelines.

    ```bash
    git clone https://github.com/your-github-username/reAnalyst.git
    cd reAnalyst
    ```

## System Requirements

To effectively use the reAnalyst framework, ensure your system meets the following requirements:

- **Operating System**: Windows, Linux, or macOS. Specific tools and scripts within reAnalyst may have OS-specific instructions.
- **Python Version**: Python 3.x. Several scripts depend on Python 3 and will not work correctly with Python 2.x.
- **Disassembler**: IDA Pro, Ghidra, or similar, for scripts that interact with binary analysis.
- **Additional Software**:
  - Optical Character Recognition (OCR) tool for converting images to text. Tesseract OCR is recommended.
  - Matplotlib for generating scatter plots (for the Scatter Graph feature).
  - OpenCV for image processing tasks.

Ensure all required libraries and dependencies for Python scripts are installed by following the setup instructions in each component's README.

## Contributing

Contributions to reAnalyst are welcome! Whether it's adding new features, improving existing scripts, or reporting bugs, your input helps make reAnalyst better for the community. Please submit your contributions as pull requests or report issues through the GitHub issue tracker.







