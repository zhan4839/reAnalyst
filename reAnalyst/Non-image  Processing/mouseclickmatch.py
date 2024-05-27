import json
import re
import os
from bs4 import BeautifulSoup
from datetime import datetime

# Load JSON data
def load_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

# Function to recursively find the 'mouse' key in the JSON data
def find_mouse_events(data):
    if isinstance(data, dict):
        for key, value in data.items():
            if key == 'mouse':
                return value
            result = find_mouse_events(value)
            if result:
                return result
    return None

# Convert hOCR filename timestamp to JSON timestamp format
def convert_hocr_to_json_timestamp(hocr_filename):
    dt = datetime.strptime(hocr_filename.split('.')[0], "%Y-%m-%d_%H:%M:%S")
    return dt.strftime("%b %d, %Y, %-I:%M:%S %p")

# Parse hOCR file to extract bounding boxes and associated texts
def parse_hocr(path_to_hocr):
    with open(path_to_hocr, 'r') as file:
        content = file.read()
    soup = BeautifulSoup(content, 'html.parser')
    results = []
    for word in soup.find_all('span', class_='ocrx_word'):
        title = word.get('title', '')
        bbox_match = re.search(r'bbox (\d+) (\d+) (\d+) (\d+)', title)
        if bbox_match and len(bbox_match.groups()) == 4:
            x1, y1, x2, y2 = map(int, bbox_match.groups())
            text = word.get_text(strip=True)
            results.append((x1, y1, x2, y2, text))
    return results

# Extract the specific symbol that the clicked character belongs to
def extract_symbol(text, index):
    processed_text = re.sub(r'\bundefined\d*', '', text)
    pattern = r'\bFUN_[A-Za-z0-9_]+|\b0x[0-9A-Fa-f]+|[A-Za-z_][A-Za-z0-9_]*'
    matches = list(re.finditer(pattern, processed_text))
    all_symbols = [match.group(0) for match in matches]
    
    fun_symbols = [m.group(0) for m in matches if m.group(0).startswith('FUN_')]
    if fun_symbols:
        return fun_symbols[0]
    
    for match in matches:
        if match.start() <= index < match.end():
            return match.group(0)
    
    return "No symbol found"

# Find texts by scaled coordinates and estimate clicked character
def find_text_by_scaled_coordinates(x_click, y_click, bbox_data, scale_factor=2):
    x_click *= scale_factor
    y_click *= scale_factor
    for x1, y1, x2, y2, text in bbox_data:
        if x1 <= x_click <= x2 and y1 <= y_click <= y2:
            total_width = x2 - x1
            click_offset = x_click - x1
            relative_x_position = click_offset / total_width
            estimated_char_index = int(relative_x_position * len(text))
            estimated_char = text[estimated_char_index] if 0 <= estimated_char_index < len(text) else None
            symbol = extract_symbol(text, estimated_char_index)
            found_symbols = re.findall(r'\bFUN_[A-Za-z0-9_]+|\b0x[0-9A-Fa-f]+|[A-Za-z_][A-Za-z0-9_]*', text)
            if symbol == "No symbol found":
                return None
            print("All symbols found: ", ", ".join(found_symbols))
            return f"Text '{text}' at bbox ({x1, y1, x2, y2}), Character: {estimated_char}, Symbol: {symbol}", symbol
    return None

# Integrate the JSON and hOCR data processing for all hOCR files in the current directory
def process_all_hocr_files(json_path):
    data = load_json(json_path)
    mouse_events = find_mouse_events(data)

    hocr_files = [f for f in os.listdir() if f.endswith('.hocr')]
    results_summary = []

    double_click_threshold = 3000  # milliseconds
    previous_click = None

    for hocr_filename in hocr_files:
        print(f"Processing file: {hocr_filename}")
        # Convert hOCR filename to JSON timestamp
        json_timestamp = convert_hocr_to_json_timestamp(hocr_filename.split('_')[0] + '_' + hocr_filename.split('_')[1])

        # Find the first matching instance in the JSON data
        matching_event = None
        for event in mouse_events:
            if event['InputTime'].startswith(json_timestamp):
                x_click = int(event['XLoc'])
                y_click = int(event['YLoc'])
                event_time_ms = event['Index MS']
                matching_event = event
                break
        
        if not matching_event:
            print(f"No matching click event found for timestamp: {json_timestamp}")
            continue

        click_type = 'single click'
        if previous_click:
            interval = event_time_ms - previous_click['Index MS']
            if interval <= double_click_threshold and x_click == previous_click['XLoc'] and y_click == previous_click['YLoc']:
                click_type = 'double click'
                previous_click['click_type'] = 'double click'
        
        previous_click = {'XLoc': x_click, 'YLoc': y_click, 'Index MS': event_time_ms, 'click_type': click_type}

        # Parse the hOCR file
        try:
            bbox_data = parse_hocr(hocr_filename)
            if not bbox_data:
                print(f"No bounding box data found in hOCR file: {hocr_filename}")
                continue
            result = find_text_by_scaled_coordinates(x_click, y_click, bbox_data)
            if result:
                text_result, symbol = result
                print(f"File: {hocr_filename}, {matching_event['InputTime']}, {click_type}, {x_click}, {y_click}")
                print(text_result)
                results_summary.append((hocr_filename, matching_event['InputTime'], symbol, click_type))
        except FileNotFoundError:
            print(f"hOCR file not found: {hocr_filename}")
        except Exception as e:
            print(f"Error processing hOCR file: {e}")
    
    # Summary of all results by file names, ranked by orders (time)
    results_summary.sort(key=lambda x: datetime.strptime(x[1], "%b %d, %Y, %I:%M:%S %p"))
    print("\nSummary of all results by file names:")
    for result in results_summary:
        print(f"File: {result[0]}, Time: {result[1]}, Symbol: {result[2]}, Type: {result[3]}")

# Example usage
if __name__ == '__main__':
    json_path = 'mouse.json'
    process_all_hocr_files(json_path)

