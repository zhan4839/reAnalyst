from idautils import *
from ida_funcs import *
from ida_bytes import *
from ida_name import *
from ida_idaapi import BADADDR
import idc

# List of registers and common assembly instructions to exclude
# Anything that is at most 4 character will already be excluded
excluded_symbols = {symbol.lower() for symbol in [
    # General purpose registers
    "movzx", "setbe","movzx","aTrue","my_error","movups","setbe","strstr","malloc","fseek","strlen","lseek",
    "fprintf","fflush","abort","strcpy","sprintf","MOVLT","ANDLS","RETEQ","MOVS","printf","STRBNE","MOVNE",
    "POPEQ","UMULL","ADDNE","fclose","MOVEQ","MOVHI","comisd","ucomisd",
    "flags", "eflags", "rflags", "rdtsc", "cpuid", "syscall", "fread","strcat",
    "minsd","aFalse","aUnsupported","setnz","movdqu", "fputs",
    "movdqu","movsx","movsxd","addsd","divsd","cmova","_exit","movaps","cmovz","strcmp","write"
]}

def is_excluded_symbol(symbol):
    # Convert symbol to lower case for case-insensitive comparison
    symbol = symbol.lower()

    # Exclude symbols that are at most 4 characters long
    if len(symbol) <= 4:
        return True

    return symbol in excluded_symbols


def sanitize_symbol(symbol):
    # Directly return if the symbol matches a hex pattern like "0x1234", "-0x1234", etc.
    if re.match(r'^-?0x[0-9A-Fa-f]+$', symbol):
        return symbol

    # Exclude symbols that start with specific characters or contain certain patterns
    if symbol.startswith(("#", "=", "[", "{","sub_")) or ' ' in symbol or ',' in symbol:
        return None

    # If the symbol is a hexadecimal number, we return it immediately
    if re.match(r'^(0x)?[0-9A-Fa-f]+$', symbol):  # matches "0x1234", "ABCD", etc.
        return symbol

    # Remove patterns like '=dword_XXXXX', '=byte_XXXXX', etc.
    symbol = re.sub(r'=[a-z]+_\w+', '', symbol, flags=re.IGNORECASE)

    # Remove segment registers and associated ':'
    symbol = re.sub(r'\bcs:|ds:|es:|ss:|fs:|gs:\b', '', symbol, flags=re.IGNORECASE)
    
    # Remove pointer and offset information
    symbol = re.sub(r'\bbyte ptr|word ptr|dword ptr|qword ptr|xmmword ptr|ymmword ptr\b', '', symbol, flags=re.IGNORECASE)
    symbol = re.sub(r'\[\w+\+.*?\]', '', symbol)  # remove [register+offset]
    
    # Remove addition/subtraction symbols and the following digits or hex numbers
    symbol = re.sub(r'[+-]\s*[\da-fA-Fh]+', '', symbol)
    
    # Remove leading and trailing whitespaces that might have been created during the replacements
    symbol = symbol.strip()

    # Remove patterns like '[R9,#(dword_3BFCC x3BF98)]'
    symbol = re.sub(r'\[\w+,#\(\w+ \w+\)\]', '', symbol)

    # Remove patterns like "=(loc_8B88 x8E58)"
    symbol = re.sub(r'=\(.*?\)', '', symbol)
    # Remove memory access patterns with scaled indexing, e.g., "0[rcx*8]", "8[rcx*8]", etc.
    symbol = re.sub(r'\d+\[\w+\*\d+\]', '', symbol)
        # Remove array-like accesses or specific pointer dereferences in operands
    symbol = re.sub(r'\[.*?\]', '', symbol)

    # If the symbol starts with certain characters, remove them
    symbol = re.sub(r'^[_\.]+', '', symbol)
    # If after all replacements we have an empty string, return None
    if not symbol:
        return None

    return symbol


def get_function_symbols(func):
    symbols = set()

    # Iterate over the items (instructions/data) in the function
    for head in Heads(func.start_ea, func.end_ea):
        # Check if it's an instruction
        if is_code(get_full_flags(head)):
            # Get the mnemonic
            mnem = print_insn_mnem(head)
            if mnem and not is_excluded_symbol(mnem):
                symbols.add(mnem)

            # Get the operands
            for i in range(0, 6):  # IDA supports up to 6 operands
                opnd = print_operand(head, i)
                if opnd:
                    # Sanitize the operand
                    opnd = sanitize_symbol(opnd)

                    # If the operand is still meaningful after sanitization, add it
                    if opnd and not is_excluded_symbol(opnd):
                        symbols.add(opnd)



    return symbols




def universalize_symbol(symbol):
    """
    Universalizes a symbol by removing common tool-specific prefixes,
    keeping only the unique identifier part.
    """
    # This regular expression pattern matches 'dword_', 'byte_', 'loc_', 'LAB_', 'data_', etc., 
    # followed by one or more hexadecimal digits (the address part).
    pattern = re.compile(r'\b(dword_|byte_|loc_|LAB_|data_|off_|qword_)\w+', re.IGNORECASE)

    # If the symbol matches the pattern, remove the prefix, keeping only the address part.
    match = pattern.match(symbol)
    if match:
        # The unique identifier is the last part of the matched string.
        symbol = match.group().split('_')[-1]

    return symbol

def main():
    # Get the current working directory
    cwd = os.getcwd()

    # Construct the file paths
    file_path = os.path.join(cwd, "function_symbols.txt")
    func_tag_file_path = os.path.join(cwd, "function_tags.txt")

    print(f"Script started. Saving data to {file_path} and {func_tag_file_path}")

    # Open files to write the output
    with open(file_path, "w") as f, open(func_tag_file_path, "w") as f_tags:
        # Write header for the new file
        f_tags.write("symbol,tag\n")
        
        # Dictionary to store the unique symbols and their corresponding function
        unique_symbols = {}
        # Set to store symbols that appear in more than one function
        duplicate_symbols = set()

        # Iterate through all the functions in the IDA database
        for func in Functions():
            func_name = get_func_name(func)
            func_symbols = get_function_symbols(get_func(func))

            # Write the function name and the associated symbols to the file
            f.write("{}: {}\n".format(func_name, ', '.join(func_symbols)))

            # Process each symbol
            for symbol in func_symbols:
                universal_symbol = universalize_symbol(symbol)

                if universal_symbol in unique_symbols:
                    # If the symbol is already associated with another function, mark it as duplicate
                    if unique_symbols[universal_symbol] != func_name:
                        duplicate_symbols.add(universal_symbol)
                else:
                    # Otherwise, store it as a unique symbol
                    unique_symbols[universal_symbol] = func_name

        # Write entries to the function_tags file, excluding duplicates
        for symbol, func_name in unique_symbols.items():
            if symbol not in duplicate_symbols:
                f_tags.write(f"{symbol},{func_name}\n")

    print(f"Script finished. Data saved to {file_path} and {func_tag_file_path}")

# Check if the script is being run as the main module
if __name__ == "__main__":
    main()


