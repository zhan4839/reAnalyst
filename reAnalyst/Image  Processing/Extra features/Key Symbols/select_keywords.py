import os
import datetime

def parse_timestamp_from_filename(filename):
    try:
        return datetime.datetime.strptime(filename.split('.')[0], '%Y-%m-%d_%H_%M_%S')
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

def group_consecutive_timestamps(grouped_files, gap_seconds=30):
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

# Example usage
folder_path = 'Example Screenshots'  # Replace with your folder path
keywords_file_path = 'keywords.txt'  # Replace with the path to your keywords file

keywords_to_groups = read_keywords_and_groups(keywords_file_path)
grouped_files = search_keywords_in_files(folder_path, keywords_to_groups)
grouped_timestamps = group_consecutive_timestamps(grouped_files)

# Printing results
for group, intervals in grouped_timestamps.items():
    for start, end in intervals:
        start_str = start.strftime('%Y-%m-%d %H:%M:%S')
        end_str = end.strftime('%Y-%m-%d %H:%M:%S')
        print(f"{start_str} - {end_str}: {group}")
