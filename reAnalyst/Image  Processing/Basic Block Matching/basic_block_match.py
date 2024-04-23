import re
import os
import json
from difflib import SequenceMatcher
from Levenshtein import distance as levenshtein_distance

# This function extracts basic blocks from functions specified in relevant_function_names
def extract_function_basic_blocks(input_text, relevant_function_names):
    # Initialize an empty dictionary for each function
    function_blocks = {name: {} for name in relevant_function_names}

    # Create an iterator for the lines in input_text
    lines = iter(input_text.split('\n'))
    current_function = None

    try:
        while True:
            line = next(lines)
            # If the line starts with "Function: ", it indicates the start of a new function
            if line.startswith("Function: "):
                function_name = line[len("Function: "):].strip()
                # Check if the function is one of the relevant functions
                if function_name in relevant_function_names:
                    current_function = function_name
                else:
                    current_function = None
            # If the current line is part of a relevant function
            elif current_function:
                # If the line starts with "Basic Block @ ", it indicates the start of a basic block
                if line.startswith("Basic Block @ "):
                    # Extract the block address
                    addr = re.search(r"Basic Block @ (0x[\da-fA-F]+):", line).group(1)
                    # Initialize an empty list to store the lines of the block
                    block = []

                    # Keep reading lines until the end of the block
                    while True:
                        line = next(lines)
                        if line.startswith("----"):
                            # When the end of the block is reached, store it in function_blocks
                            function_blocks[current_function][addr] = '\n'.join(block)
                            break
                        # If the line doesn't start with "my_loc_", add it to the block
                        elif not line.startswith("my_loc_"):
                            block.append(line)
    # The loop will raise a StopIteration exception when there are no more lines to read
    except StopIteration:
        pass

    # Return the extracted basic blocks
    return function_blocks

# This function tokenizes a block, splitting it into non-space characters and removing irrelevant ones
def tokenize_block(block, is_input=False):
    # Split the block into non-space characters
    tokens = re.findall(r'\S+', block)
    # Remove words that start with "my_loc_"
    tokens = [token for token in tokens if not token.startswith("my_loc_")]
    # Create a copy of the tokens to add to later
    new_tokens = tokens.copy()
    # For "loc_" tokens, remove the "loc_" part and keep both parts (with "loc_" and without) if it is input
    # If it is OCR text, we keep the token as is
    for token in tokens:
        if token.lower().startswith("loc_") and is_input:
            new_tokens.append(token.split('_')[1])
        elif 'loc' in token.lower() and is_input:
            # Handling the case where 'loc' and address are separate tokens
            new_tokens.append('_'.join(token.split()))
    return new_tokens

# This function computes the matching score between an OCR block and an input block
def block_matching_score(ocr_block, input_block, loc_tags_count):
    # Tokenize the blocks
    ocr_tokens = set(tokenize_block(ocr_block))
    input_tokens = set(tokenize_block(input_block, is_input=True))

    # Convert the tokens back into strings
    ocr_string = ' '.join(ocr_tokens)
    input_string = ' '.join(input_tokens)

    # Compute the Levenshtein distance between the OCR string and the input string
    levenshtein_dist = levenshtein_distance(ocr_string, input_string)

    # Compute the similarity score based on the Levenshtein distance
    matching_ratio = 1 - levenshtein_dist / max(len(ocr_string), len(input_string))

    # Compute the presence of location tags
    loc_tags_present = len([token for token in ocr_tokens if token.startswith("loc_")]) == loc_tags_count

    # Return the result of the matching, the matching ratio, the common tokens, and a flag indicating whether location tags are present
    return matching_ratio, ocr_tokens & input_tokens, loc_tags_present

def find_matching_basic_blocks(ocr_text, basic_blocks):
    ocr_tokens = tokenize_block(ocr_text)
    ocr_string = ' '.join(ocr_tokens)

    matching_blocks = []
    for addr, content in basic_blocks.items():
        block_tokens = tokenize_block(content, is_input=True)
        block_string = ' '.join(block_tokens)
        
        # Only consider loc_ tokens found in this block
        ocr_tokens_filtered = [token for token in ocr_tokens if not token.startswith('loc_') or token in block_tokens]

        common_tokens = set(ocr_tokens_filtered) & set(block_tokens)
        matching_ratio = SequenceMatcher(None, ocr_string, block_string).ratio()

        loc_tags_present = any(tag in ocr_string for tag in block_tokens if tag.startswith("loc_"))
        matching_blocks.append((addr, matching_ratio, common_tokens, loc_tags_present))

    return matching_blocks


# This function reads the function data from a JSON file and returns a dictionary mapping file names to function names
def read_function_data(json_file):
    with open(json_file, "r") as f:
        data = json.load(f)
    return {entry["file"]: entry["function"] for entry in data["data"]}

# This function sorts and filters the matching blocks based on their matching ratio
def filter_matching_blocks(matching_blocks):
    filtered_matching_blocks = []

    # Sort the blocks by matching ratio in descending order
    sorted_matching_blocks = sorted(matching_blocks, key=lambda x: x[1], reverse=True)

    # Add the sorted blocks to the filtered list
    for block, matching_ratio, common_tokens, loc_tags_present in sorted_matching_blocks:
        filtered_matching_blocks.append((block, matching_ratio, common_tokens, loc_tags_present))

    return filtered_matching_blocks

def process_files(input_folder, basic_blocks, function_data):
    results = []
    highest_match_results = {}

    # Iterate over each file in the input folder
    for file_name in os.listdir(input_folder):
        print(f"Processing {file_name}")  # Debugging line
        # If the file_name ends with '_1', '_2', etc., remove this ending
        if re.search(r'_\d+\.txt$', file_name):
            function_name_file = re.sub(r'_\d+(\.txt)$', r'\1', file_name)
        else:
            function_name_file = file_name
        # Check if the file is in function_data
        if function_name_file not in function_data:
            results.append(f"{file_name} not found in the function matching json.\n")
            continue

        # Get the name of the function associated with the file
        function_name = function_data[function_name_file]

        # If the function name is empty, add a note to the results and continue to the next file
        if not function_name:
            results.append(f"{file_name} has an empty associated function.\n")
            continue

        # Read the OCR text from the file
        with open(os.path.join(input_folder, file_name), "r") as f:
            ocr_text = f.read()

        # Find the matching basic blocks for the function in the OCR text
        matching_blocks = find_matching_basic_blocks(ocr_text, basic_blocks[function_name])
        # Filter the matching blocks
        filtered_matching_blocks = filter_matching_blocks(matching_blocks)

        # Add the results for the file to the results list
        results.append(f"Matching Basic Blocks for {file_name} in function {function_name}:\n")
        
        # Initialize the highest matching block for this file
        highest_matching_block = None

        for block, matching_ratio, common_tokens, loc_tags_present in filtered_matching_blocks:
            results.append(f"{block}\n")
            results.append(f"Matching Ratio: {matching_ratio}\n")
            results.append(f"Common Tokens: {common_tokens}\n")
            results.append(f"Loc Tags Present: {loc_tags_present}\n")
            results.append("\n")

            # Update the highest matching block for this file
            if highest_matching_block is None or matching_ratio > highest_matching_block[1]:
                highest_matching_block = (block, matching_ratio, common_tokens, loc_tags_present)
        
        highest_match_results[file_name] = highest_matching_block

    return results, highest_match_results


def main():
    # Load the input text from a file
    with open("basic_block_database.txt", "r") as f:
        input_text = f.read()

    # Load the function data from a JSON file
    function_data = read_function_data("function_matching_results.json")

    # Get the unique list of relevant function names
    relevant_function_names = set(function_data.values())

    # Extract basic blocks only for relevant functions
    basic_blocks = extract_function_basic_blocks(input_text, relevant_function_names)

    # Process the files in the input folder and get the results
    results, highest_match_results = process_files("Example Cropped Output", basic_blocks, function_data)

    # Write the results to an output file
    with open("output.txt", "w") as f:
        f.writelines(results)

    # Group highest match results by the base file name without numeric endings
    combined_results = {}
    for file_name, result in highest_match_results.items():
        base_name = re.sub(r'(_\d+)?\.txt$', '', file_name)
        if base_name not in combined_results:
            combined_results[base_name] = []
        if result:
            combined_results[base_name].append(result[0])  # Append block address

    # Write the highest match results to result.txt
    with open("result.txt", "w") as f:
        for file_name, match_result in highest_match_results.items():
            if match_result:
                block, matching_ratio, common_tokens, loc_tags_present = match_result
                f.write(f"Highest matching block for {file_name}:\n")
                f.write(f"{block}\n")
                f.write(f"Matching Ratio: {matching_ratio}\n")
                f.write(f"Common Tokens: {common_tokens}\n")
                f.write(f"Loc Tags Present: {loc_tags_present}\n\n")
        
        # Write the combined results for files with the same name but different endings
        f.write("Combined Results:\n")
        for base_name, blocks in combined_results.items():
            f.write(f"{base_name}: {', '.join(blocks)}\n")

if __name__ == "__main__":
    main()
