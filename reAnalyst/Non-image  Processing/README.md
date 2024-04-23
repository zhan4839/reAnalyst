# Non-Image Data Processing Scripts for reAnalyst

This suite of Python scripts is designed to analyze non-image data collected during reverse engineering (RE) activities as part of the reAnalyst framework. It includes tools for processing keystrokes, analyzing process lifecycles, extracting debug information, and summarizing window usage data.

## Scripts Overview

- `keystroke.py`: Analyzes keystroke data to identify typed words and their corresponding timestamps.
- `process.py`: Analyzes the lifecycle of system processes, identifying when processes are opened and closed.
- `process_debug_info.py`: Extracts information about debugging sessions.
- `windows.py`: Extracts information about window focus changes during RE tasks.

## Prerequisites

- Python 3.x
- JSON-formatted data files generated from RE activities, compatible with each script's expected input format.

## Installation

1. Clone this repository or download the desired scripts.
2. Ensure you have Python 3.x installed on your system.

## Usage

Each script is designed for standalone operation. Below are the general usage instructions for each script. Replace the placeholder file paths with your actual data file paths.

    ```bash
    python keystroke.py
    python process.py
    python process_debug_info.py
    python windows.py
    
    ```
