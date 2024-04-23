# Keyword Search and Grouping from OCR Outputs

This tool scans through text files generated from OCR outputs, searching for predefined keywords and grouping the occurrences based on categories. It's designed to help analyze and categorize segments of text by identifying specific keywords and their corresponding timestamps.

## Overview

The script operates in several steps:

1. **Reading Keywords and Groups**: Loads a list of keywords and their associated groups from a text file.
2. **Searching Keywords in OCR Outputs**: Scans through OCR output files, searching for keywords and noting their occurrence.
3. **Grouping Consecutive Timestamps**: Organizes the timestamps of keyword occurrences into groups based on the time gap between consecutive findings.

## Prerequisites

- Python 3.x
- A set of text files generated from OCR outputs, placed in a specific directory.
- A text file (`keywords.txt`) containing the keywords to search for, along with their group associations.

## Installation

1. Ensure Python 3.x is installed on your system.
2. Clone this repository or download the script directly to your local machine.
3. Prepare your OCR output files in a designated directory.
4. Create your keywords file, following the format `keyword,group` per line.

## Configuration

- Modify the `folder_path` variable in the script to point to the directory containing your OCR output files.
- Modify the `keywords_file_path` variable to point to your keywords file.

## Running the Script

    ```bash
    python script_name.py  # Replace script_name.py with the name of this script
    ```

