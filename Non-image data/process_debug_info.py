import re
import os
from datetime import datetime

def str_to_datetime(date_str):
    return datetime.strptime(date_str, '%b %d, %Y, %I:%M:%S %p')

def get_seconds(time_str):
    dt_obj = str_to_datetime(time_str)
    return int(dt_obj.timestamp())

def gdb_ranges(data_tuples_gdb):
    ranges = []
    start_entry = {}

    for entry in data_tuples_gdb:
        index, pid, stat = entry

        if stat in ["RUNNING", "SLEEPING"]:
            if pid not in start_entry:
                start_entry[pid] = index
        elif stat == "DIED":
            if pid in start_entry:
                ranges.append((get_seconds(start_entry[pid]), get_seconds(index)))
                del start_entry[pid]
    return ranges

def merge_periods(periods):
    if not periods:  # Check if the list is empty
        return []  # Return an empty list if it is

    merged = []
    periods.sort(key=lambda x: x[0])
    current_start, current_end, current_source = periods[0]

    for start, end, source in periods[1:]:
        if start <= current_end and source == current_source:
            current_end = max(current_end, end)
        else:
            merged.append((current_start, current_end, current_source))
            current_start, current_end, current_source = start, end, source
    merged.append((current_start, current_end, current_source))
    return merged


def process_file(file_name):
    with open(file_name, "r") as file:
        data = file.read().replace("}", "}\n")
        lines = data.split("\n")

    filtered_lines_veriT = [line for line in lines if "veriT" in line and "ida" not in line and "gdb" not in line]
    filtered_lines_gdb = [line for line in lines if "gdb" in line]

    pattern = re.compile(r'"Index":"(.*?)".*?"PID":"(.*?)".*?"Stat":"(.*?)"')
    data_tuples_veriT = [pattern.search(line).groups() for line in filtered_lines_veriT if line.strip() and pattern.search(line)]
    data_tuples_gdb = [pattern.search(line).groups() for line in filtered_lines_gdb if line.strip() and pattern.search(line)]

    gdb_ranges_list = gdb_ranges(data_tuples_gdb)

    # Process the extracted information and print the output
    periods = []
    first_other_entry = {}

    for entry in data_tuples_veriT:
        index, pid, stat = entry
        index_datetime = str_to_datetime(index)

        if stat == "OTHER":
            if pid not in first_other_entry:
                first_other_entry[pid] = index
        elif stat == "DIED":
            if pid in first_other_entry:
                start_datetime = str_to_datetime(first_other_entry[pid])
                if any(start_datetime.timestamp() >= gdb_start and index_datetime.timestamp() <= gdb_end for gdb_start, gdb_end in gdb_ranges_list):
                    periods.append((get_seconds(first_other_entry[pid]), get_seconds(index), "GDB"))
                else:
                    periods.append((get_seconds(first_other_entry[pid]), get_seconds(index), "IDA"))
                del first_other_entry[pid]

    # Merge periods
    merged_periods = merge_periods(periods)

    # Write to file
    with open("debugging_summary.txt", "a") as file:
        for start, end, source in merged_periods:
            start_str = datetime.utcfromtimestamp(start).strftime('%b %d, %Y, %I:%M:%S %p')
            end_str = datetime.utcfromtimestamp(end).strftime('%b %d, %Y, %I:%M:%S %p')
            duration = end - start
            file.write(f"{file_name}: {start_str} - {end_str} ({source}, {duration} seconds)\n")

    # Print to console
    for start, end, source in merged_periods:
        start_str = datetime.utcfromtimestamp(start).strftime('%b %d, %Y, %I:%M:%S %p')
        end_str = datetime.utcfromtimestamp(end).strftime('%b %d, %Y, %I:%M:%S %p')
        duration = end - start
        print(f"{file_name}: {start_str} - {end_str} ({source}, {duration} seconds)")

    # Summaries
    total_time = sum(end - start for start, end, _ in merged_periods)
    ida_time = sum(end - start for start, end, source in merged_periods if source == "IDA")
    gdb_time = total_time - ida_time

    # Store the summary information for this file
    summary_info[file_name] = (len(merged_periods), total_time, ida_time, gdb_time)

    summary = f"""
    Summary for {file_name}:
    Total Debugging Sessions: {len(merged_periods)}
    Total Debugging Time: {total_time} seconds
    Total IDA Debugging Time: {ida_time} seconds
    Total GDB Debugging Time: {gdb_time} seconds
    """
    print(summary)
    with open("debugging_summary.txt", "a") as file:
        file.write(summary + '\n' + '-'*50 + '\n')

# Create a dictionary to store summary information for each file
summary_info = {}

# Get all json files in the current directory
json_files = [f for f in os.listdir('.') if os.path.isfile(f) and f.endswith('.json')]

# Process each file
for file_name in json_files:
    process_file(file_name)

# New summary section for all files
all_file_summary = f"""
Overall Summary:
Total Files Processed: {len(json_files)}
"""
for file_name, info in summary_info.items():
    all_file_summary += f"\n{file_name},{info[0]},{info[1]},{info[2]},{info[3]}"

print(all_file_summary)
with open("debugging_summary.txt", "a") as file:
    file.write(all_file_summary)