import os
import datetime
from datetime import datetime, timedelta
import json

# Code A functions
def parse_timestamp_from_filename(filename):
    try:
        return datetime.strptime(filename.split('.')[0], '%Y-%m-%d_%H:%M:%S')
    except ValueError:
        return None

def read_keywords_and_groups(file_path):
    keywords_to_groups = {}
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split(',')
            if len(parts) == 2:
                keyword, group = parts
                keywords_to_groups[keyword.strip().lower()] = group.strip()
    return keywords_to_groups

def search_keywords_in_files(folder_path, keywords_to_groups):
    results = {}
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read().lower()
            except UnicodeDecodeError:
                try:
                    with open(file_path, 'r', encoding='latin-1') as file:
                        content = file.read().lower()
                except Exception:
                    continue
            except Exception:
                continue

            for keyword, group in keywords_to_groups.items():
                if keyword in content:
                    if group not in results:
                        results[group] = []
                    results[group].append(parse_timestamp_from_filename(filename))
                    break

    return results

def group_consecutive_timestamps(grouped_files, gap_seconds=10):
    final_groups = {}
    for group, timestamps in grouped_files.items():
        sorted_timestamps = sorted(timestamps)
        current_group = []
        last_timestamp = None

        for timestamp in sorted_timestamps:
            if timestamp is None:
                continue

            if last_timestamp is None or (timestamp - last_timestamp).total_seconds() > gap_seconds:
                if current_group:
                    if group not in final_groups:
                        final_groups[group] = []
                    final_groups[group].append((current_group[0], current_group[-1]))
                current_group = [timestamp]
            else:
                current_group.append(timestamp)

            last_timestamp = timestamp

        if current_group:
            if group not in final_groups:
                final_groups[group] = []
            final_groups[group].append((current_group[0], current_group[-1]))

    return final_groups

# Code B function (updated)
def analyze_keystrokes_from_file(file_path):
    keystrokes = []
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)

        # Extracting keystrokes from the nested structure
        for outer_key, outer_value in data.items():
            for inner_key, inner_value in outer_value.items():
                if "keystrokes" in inner_value:
                    keystrokes.extend(inner_value["keystrokes"])

        def parse_time(time_str):
            # Adjust the format according to your timestamp format
            return datetime.strptime(time_str, "%b %d, %Y, %I:%M:%S %p")

        # Process keystrokes and combine them into words
        current_word = ""
        word_start_time = None
        time_gap_threshold = 2  # Define the time gap threshold in seconds
        keystroke_data = []

        for keystroke in keystrokes:
            time = parse_time(keystroke.get("InputTime"))
            key = keystroke.get("Button")
            action = keystroke.get("Type")

            if action == "type":
                if not word_start_time:
                    word_start_time = time

                if current_word and (time - word_start_time).total_seconds() > time_gap_threshold:
                    # If time gap is large, store the current word and start a new word
                    if any(char.isprintable() and not char.isspace() for char in current_word):
                        keystroke_data.append((word_start_time, current_word.strip()))
                    current_word = key
                    word_start_time = time
                else:
                    # Otherwise, continue the current word
                    if key.isprintable():
                        current_word += key

        # Store the last word if it exists
        if any(char.isprintable() and not char.isspace() for char in current_word):
            keystroke_data.append((word_start_time, current_word.strip()))

        return keystroke_data

    except json.JSONDecodeError:
        print("Invalid JSON data")
        return []
    except FileNotFoundError:
        print("File not found")
        return []

# Combining and filtering results
def combine_and_filter_results(grouped_timestamps, keystroke_data):
    final_results = []

    for group, intervals in grouped_timestamps.items():
        for start, end in intervals:
            matching_keystrokes = []
            for keystroke_time, word in keystroke_data:
                if start <= keystroke_time <= end and word and word != "�":
                    matching_keystrokes.append(word)

            if matching_keystrokes:
                start_str = start.strftime('%Y-%m-%d %H:%M:%S')
                end_str = end.strftime('%Y-%m-%d %H:%M:%S')
                words = ', '.join([f"Word: {word}" for word in matching_keystrokes if word and word != "�" and word.strip()])
                if words.strip():
                    final_results.append(f"{start_str} - {end_str}: {group}, {words}")

    return final_results

# Example usage
folder_path = 'screenshots'  # Replace with your folder path
keywords_file_path = 'feature.txt'  # Replace with the path to your keywords file
keystroke_file_path = 'key.json'  # Replace with the path to your keystroke file

# Code A execution
keywords_to_groups = read_keywords_and_groups(keywords_file_path)
grouped_files = search_keywords_in_files(folder_path, keywords_to_groups)
grouped_timestamps = group_consecutive_timestamps(grouped_files)

# Code B execution
keystroke_data = analyze_keystrokes_from_file(keystroke_file_path)

# Combine and filter results
filtered_results = combine_and_filter_results(grouped_timestamps, keystroke_data)

# Printing final filtered results
for result in filtered_results:
    print(result)

