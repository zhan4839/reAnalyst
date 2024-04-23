import json

def extract_windows_info(json_file):
    try:
        with open(json_file, 'r') as file:
            data = json.load(file)

        # Assuming the first level of keys is the user/session ID
        for user_id, user_data in data.items():
            # Assuming the second level of keys is some sort of session or experiment ID
            for session_id, session_data in user_data.items():
                windows = session_data.get('windows', [])
                for window in windows:
                    change_time = window.get('ChangeTime', 'No timestamp')
                    user = window.get('User', 'Unknown user')
                    name = window.get('Name', 'Unnamed window')
                    print(f"Timestamp: {change_time}, User: {user}, Window Name: {name}")

    except FileNotFoundError:
        print(f"File not found: {json_file}")
    except json.JSONDecodeError:
        print(f"Error decoding JSON in file: {json_file}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Replace 'path_to_your_json_file.json' with the actual file path
extract_windows_info('windows_example.json')
