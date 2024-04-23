import json

def read_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def analyze_process_lifecycle(data, excluded_commands):
    all_processes = set()
    process_lifecycle = []

    for user_id, user_data in data.items():
        for session_id, session_data in user_data.items():
            current_processes = {proc['PID']: proc for proc in session_data.get("processes", [])}
            opened_processes = set(current_processes.keys()) - all_processes
            closed_processes = all_processes - set(current_processes.keys())

            for pid in opened_processes:
                process = current_processes[pid]
                if process['Command'] not in excluded_commands:
                    process_lifecycle.append({
                        "Event": "Opened",
                        "PID": process['PID'],
                        "Command": process['Command'],
                        "User": process['User'],
                        "Time": process['SnapTime']
                    })

            for pid in closed_processes:
                process_lifecycle.append({
                    "Event": "Closed",
                    "PID": pid,
                    "Time": session_data["processes"][0]['SnapTime']  # Assuming the first process's snap time as the closing time
                })

            all_processes = set(current_processes.keys())

    return process_lifecycle

def format_process_lifecycle(process_lifecycle):
    for event in process_lifecycle:
        if event["Event"] == "Opened":
            print(f"Process Opened - PID: {event['PID']}, Command: {event['Command']}, "
                  f"User: {event['User']}, Time: {event['Time']}")
        elif event["Event"] == "Closed":
            print(f"Process Closed - PID: {event['PID']}, Time: {event['Time']}")

def analyze_processes(file_path, excluded_commands):
    data = read_json_file(file_path)
    process_lifecycle = analyze_process_lifecycle(data, excluded_commands)
    format_process_lifecycle(process_lifecycle)

# Replace 'your_json_file.json' with the path to your JSON file
# Specify the commands you want to exclude as a list
excluded_commands = ['xprop', 'xfwm4','xwininfo','WindowMonitor']  # Replace with actual commands to exclude



# Replace 'your_json_file.json' with the path to your JSON file
analyze_processes('process_example.json',excluded_commands)
