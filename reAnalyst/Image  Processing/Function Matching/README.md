# Function Matching Feature for reAnalyst

The Function Matching (FM) feature of reAnalyst is designed to enhance the analysis of reverse engineering activities by matching symbols extracted from OCR-processed screenshots to their corresponding functions. This document outlines how to generate the necessary symbol-function mappings and use the `fm.py` script to perform function matching.

## Overview

Before using `fm.py`, you must first run a separate script within your disassembler (e.g., IDA Pro, Ghidra) to generate a symbol-function map for each binary you're analyzing. This step is crucial for the function matching process, as it provides the mappings that `fm.py` relies on to match symbols to functions based on OCR text extracted from screenshots.

## Generating Symbol-Function Mappings

1. **Prepare Your Disassembler Script**: Use the provided `symbols.py` script as a template for generating symbol-function mappings. This script should be executed within the context of your disassembler to access its internal databases.

2. **Run the Script in Your Disassembler**: 
   - For IDA Pro: Load your binary, then run `symbols.py` via the `File > Script file...` menu option.
   - For Ghidra: Load your binary, then use the Script Manager to run a modified version of `symbols.py` tailored for Ghidra.

3. **Export the Mappings**: The script will generate a symbol-function mapping file (`function_symbols.txt` and `function_tags.txt`). Ensure these files are accessible to the `fm.py` script, typically by placing them in a known directory.

## Using fm.py

`fm.py` compares symbols found in OCR-processed text files against the symbol-function mappings to identify the most likely function matches.

### Prerequisites

- Python 3.x
- FuzzyWuzzy Python library
- Python-Levenshtein (for performance improvement in FuzzyWuzzy)

### Setup

1. Install the required Python packages:

   ```bash
   pip install fuzzywuzzy python-Levenshtein
   
2. Place your OCR-processed text files in a directory that fm.py can access. These text files should contain the OCR output from screenshots of disassembled code.

### Configuration

Ensure fm.py is configured to point to the directory containing your OCR text files and the symbol-function mapping files.

### Running Function Matching

    ```bash
    python fm.py
    ```
    
### Contributing
Your contributions to improve or extend the function matching feature are welcome. Please follow standard practices for submitting issues and pull requests to this project.


