import os
import re
from fuzzywuzzy import fuzz
import json
from fmconfig import COMMON_SYMBOLS, SEGMENTS

def load_symbol_function_map(filepath):
    symbol_function_map = {}
    with open(filepath, 'r', encoding='ISO-8859-1') as file:

        lines = file.readlines()
        for line in lines:
            parts = line.strip().split(',')
            if len(parts) == 2:
                symbol, function = parts
                symbol_function_map[symbol] = function
    return symbol_function_map

def load_ocr_files(directory):
    ocr_content = {}
    # Sort files by name while reading them
    for filename in sorted(os.listdir(directory)):
        if filename.endswith('.txt'):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r', encoding='ISO-8859-1') as file:
                content = file.read()
                ocr_content[filename] = content  # Store the entire content
    return ocr_content


def find_best_matches(symbol_function_map, ocr_content, score_threshold=80):
    best_matches = {}
    # Define the set of common assembly symbols
    common_symbols = set(COMMON_SYMBOLS)


    for ocr_file, content in ocr_content.items():
        print(f"Processing file: {ocr_file}")  # Debugging info
        best_function = None
        highest_score = 0
        content_lower = content.lower()  # Convert content to lowercase here

        # Split the content based on spaces and colons, as segments are followed by colons
        

        segments = SEGMENTS

        segment_count = {segment: 0 for segment in segments}
        for segment in segments:
            # Use regex to find all occurrences of the segment, regardless of its context
            segment_count[segment] = len(re.findall(re.escape(segment), content_lower))


        multiple_segments = [segment for segment, count in segment_count.items() if count > 7]

        if multiple_segments:
            print(f"File {ocr_file} contains these segments more than 7 times: {', '.join(multiple_segments)}, considering no match.")
            best_function = None
            # Add this match to the results with a note that it was invalidated due to multiple segments
            best_matches[ocr_file] = None
            continue  # Skip the rest of the loop and move to the next file
                   
        content = re.sub(r'[^ \n]{26,}', ' ', content)


        all_symbols = re.findall(r'[\da-fA-F]+h?', content)
        filtered_symbols = []
        
        

        for symbol in all_symbols:
            if symbol.islower():  # Check if the symbol contains only lowercase letters
                word_symbols = re.findall(r'\b' + re.escape(symbol) + r'\b', content)
                filtered_symbols.extend(word_symbols)
            else:
                filtered_symbols.append(symbol)

        symbols = filtered_symbols

        for symbol in symbols:
            if len(symbol) <= 3:
                continue  # Skip symbols that are 3 or fewer characters

            for map_symbol, function in symbol_function_map.items():
                score = fuzz.ratio(symbol.lower(), map_symbol.lower())
                if score > highest_score:
                    highest_score = score
                    best_function = function
                    print(f"    New highest score: {highest_score} for symbol: {symbol} matched with {map_symbol} for function: {function}")
                    if highest_score == 100:
                        break  # If we have a perfect match, no need to continue comparing
            if highest_score == 100:
                break  # If we have a perfect match, no need to continue with other symbols


        if highest_score >= score_threshold:
            # Check for common assembly symbols if the score is below 97
            if highest_score < 97:
                words = re.split(r'[ :\n]', content_lower)
                common_symbol_count = 0
                unique_common_symbol_count = 0  # Count of unique common symbols
                symbol_counts = {}  # Dictionary to hold counts of each symbol

                words = re.split(r'[ \t\n\r]+', content_lower)  # This splits on spaces, tabs, and new lines

                for asm_symbol in common_symbols:
                    symbol_count = words.count(asm_symbol)
                    if symbol_count > 0:
                        common_symbol_count += symbol_count
                        symbol_counts[asm_symbol] = symbol_count  # Store the count for each symbol

                # Count how many symbols have been found at least once
                unique_common_symbol_count = len([count for count in symbol_counts.values() if count > 0])

                # Debugging info
                for symbol, count in symbol_counts.items():
                    if count > 0:
                        print(f"Common symbol found: {symbol} - {count} times")

                # Check if conditions are met for valid match
                if common_symbol_count < 7 or unique_common_symbol_count < 3:
                    best_function = None  # No match due to lack of assembly symbols
                    print(f"No match for {ocr_file} due to insufficient common assembly symbols.\n")  # Debugging info

            if best_function:
                best_matches[ocr_file] = best_function
                print(f"Match found: {best_function} with score: {highest_score}\n")  # Debugging info
            else:
                best_matches[ocr_file] = None
                print(f"No confident match found for {ocr_file} (highest score: {highest_score})\n")  # Debugging info
        else:
            best_matches[ocr_file] = None  # or 'No confident match' or just skip this step
            print(f"No confident match found for {ocr_file} (highest score: {highest_score})\n")  # Debugging info

    return best_matches


def main():
    # Paths for easy access and modification
    function_tags_path = 'symbol_function_map_example.txt'  
    ocr_directory = 'Example Data'   

    # Extract the folder name from the ocr_directory path
    output_file_prefix = os.path.basename(os.path.normpath(ocr_directory))

    symbol_function_map = load_symbol_function_map(function_tags_path)
    ocr_content = load_ocr_files(ocr_directory)
    best_matches = find_best_matches(symbol_function_map, ocr_content)

    # Prepare data for JSON output
    json_output = {"data": []}
    count = 0

    output_txt = f'{output_file_prefix}_output.txt'
    output_json = f'{output_file_prefix}_output.json'

    # Open the text file for writing
    with open(output_txt, 'w') as text_file:
        for file, function in best_matches.items():
            if function:  # checks if function is not None or not an empty string
                print(f'{file}: {function}')
                text_file.write(f'{file}: {function}\n')  # Write to text file
            else:
                print(f'{file}:')  # prints the file name with no match
                text_file.write(f'{file}:\n')  # Write to text file

            # Add to JSON output
            json_output["data"].append({
                "file": file,
                "function": function if function else "",
                "count": count
            })
            count += 1

    # Write the results to the JSON file
    with open(output_json, 'w') as json_file:
        json.dump(json_output, json_file, indent=4)

if __name__ == "__main__":
    main()

