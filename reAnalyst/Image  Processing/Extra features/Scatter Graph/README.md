# Scatter Plot Generator for Function Matching Results

This Python script takes JSON output from function matching (or other similar) features and generates scatter plots. These plots visualize the occurrences of specific functions over time, based on timestamps extracted from filenames in the JSON data.

## Prerequisites

- Python 3.x
- Matplotlib installed (`matplotlib` library)
- JSON file containing the output from function matching (or other similar) features

## Installation

1. Ensure Python 3.x is installed on your system.
2. Install Matplotlib if you haven't already:

    ```bash
    pip install matplotlib
    ```

3. Obtain the JSON output file from your function matching tool. This file should contain entries with at least a "file" field (indicating the filename, which should contain a timestamp) and a "function" field (indicating the function name).

## Usage

1. Place the JSON output file from your function matching tool in a directory accessible by the script. Let's assume the file is named `example_function_matching_output.json`.

2. Modify the script to specify the path to your JSON file, adjust any flags for controlling functionality, and, if necessary, customize the list of included functions or the modification of function names for readability:

    - **`INCLUDE_Y_VALUES`**: Set to `True` to filter the scatter plot by specific function names listed in `included_values`.
    
    - **`MODIFY_Y_VALUES`**: Set to `True` to apply custom naming to the function names for readability.

    - **`included_values`**: Modify this list to include the specific function names you want to visualize on the scatter plot.

3. Run the script:

    ```bash
    python scatter_plot_generator.py
    ```

4. The script will generate a scatter plot visualizing the occurrences of functions over time. Each point on the plot corresponds to a function occurrence, with the x-axis representing time (in seconds since the start of the data collection) and the y-axis representing functions.

## Customization

- To customize which functions to include in the plot or to modify the way function names are displayed, adjust the `included_values` list and the `modify_y_value` function within the script.

- The plot appearance can be customized by modifying the Matplotlib `plt.scatter` call within the script. Refer to the [Matplotlib documentation](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.scatter.html) for more details on customization options.

## Contributing

Contributions to enhance or extend the functionality of this scatter plot generator are welcome. If you have improvements or encounter any issues, please submit a pull request or an issue through GitHub.


