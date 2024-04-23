import json
import matplotlib.pyplot as plt
import datetime

# Load data from file
with open("example_function_matching_output.json", "r") as f:
    data = json.load(f)["data"]

# Flags to control functionality
INCLUDE_Y_VALUES = False   # Set to True to apply include_y_value functionality
MODIFY_Y_VALUES = True   # Set to True to apply modify_y_value functionality

# Function to parse timestamp from the file field
def parse_timestamp(file_name):
    timestamp_str = file_name.split(".")[0]  # Removes the '.txt' part
    return datetime.datetime.strptime(timestamp_str, "%Y-%m-%d_%H_%M_%S")

# Get the start time (first timestamp)
start_time = parse_timestamp(data[0]["file"])

# Function to modify y values for better readability
def modify_y_value(y):
    if y == "":
        return "No function"  

    #if y == "sub_E60":
    #    return "bridge"
    # Add more conditions here if needed
    return y

# Function to determine if a y value should be included
def include_y_value(y, included_values):
    return y in included_values

# Define y values to be included
included_values = ["sub_E08", "sub_E60", "main"] # Add your specific function names here

# Extract x (time in seconds) and y values
xy_values = []
for d in data:
    y_value = d["function"]
    if MODIFY_Y_VALUES:
        y_value = modify_y_value(y_value)
    if INCLUDE_Y_VALUES and include_y_value(y_value, included_values):
        x_value = int((parse_timestamp(d["file"]) - start_time).total_seconds())
        xy_values.append((x_value, y_value))
    elif not INCLUDE_Y_VALUES:
        x_value = int((parse_timestamp(d["file"]) - start_time).total_seconds())
        xy_values.append((x_value, y_value))

# Sort the (x, y) pairs based on y values
xy_values_sorted = sorted(xy_values, key=lambda pair: pair[1])

# Separate the sorted x and y values
x_values, y_values = zip(*xy_values_sorted) if xy_values_sorted else ([], [])

# Create scatter plot
plt.scatter(x_values, y_values)
plt.xlabel("Time (seconds)")
plt.ylabel("Function")
plt.show()
