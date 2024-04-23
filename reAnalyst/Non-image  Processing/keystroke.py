import json
from datetime import datetime

def analyze_keystrokes_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)

        # Extracting keystrokes from the nested structure
        keystrokes = []
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
        time_gap_threshold = 1.5  # Define the time gap threshold in seconds

        for keystroke in keystrokes:
            time = parse_time(keystroke.get("InputTime"))
            key = keystroke.get("Button")
            action = keystroke.get("Type")

            if action == "type":
                if not word_start_time:
                    word_start_time = time

                if current_word and (time - word_start_time).total_seconds() > time_gap_threshold:
                    # If time gap is large, print the current word and start a new word
                    print(f"Time: {word_start_time.strftime('%b %d, %Y, %I:%M:%S %p')}, Word: {current_word}")
                    current_word = key
                    word_start_time = time
                else:
                    # Otherwise, continue the current word
                    current_word += key

        # Print the last word if it exists
        if current_word:
            print(f"Time: {word_start_time.strftime('%b %d, %Y, %I:%M:%S %p')}, Word: {current_word}")

    except json.JSONDecodeError:
        return "Invalid JSON data"
    except FileNotFoundError:
        return "File not found"

# Example Usage
file_path = 'keystroke_example.json'
print(analyze_keystrokes_from_file(file_path))
