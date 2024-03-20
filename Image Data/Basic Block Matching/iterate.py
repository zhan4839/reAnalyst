import idautils
import idaapi
import idc
import os

# Set the output filename
output_file = "basic_block_database.txt"

# Get the output file path
output_path = r"C:\Users\tabti\Desktop\Part2\part2\{}".format(output_file)


# Open the output file
with open(output_path, "w") as f:
    # Iterate through all basic blocks in the program
    for func_ea in idautils.Functions():
        for bb in idaapi.FlowChart(idaapi.get_func(func_ea)):
            # Get the starting and ending addresses of the basic block
            bb_start = bb.start_ea
            bb_end = bb.end_ea

            # Rename loc_ addresses using the prefix my_loc_
            if idc.get_name(bb_start) == "" and idc.set_name(bb_start, "my_loc_{:X}".format(bb_start)):
                print("Renamed address {:X} to my_loc_{:X}".format(bb_start, bb_start))

            # Get the function name and basic block index
            func_name = idc.get_func_name(bb_start)
            bb_index = bb.id

            # Get the instructions in the basic block
            instrs = []
            for ea in idautils.Heads(bb_start, bb_end):
                instr = idc.generate_disasm_line(ea, 0)

                # Add a location tag to the start of the basic block
                if ea == bb_start:
                    loc_name = idc.get_name(bb_start)
                    if loc_name == "":
                        loc_name = "my_loc_{:X}".format(bb_start)
                    instr = loc_name + ":\n" + instr.lstrip()

                instrs.append(instr)

            # Write the basic block to the output file
            f.write("Function: {}\n".format(func_name))
            f.write("Basic Block @ 0x{:X}:\n".format(bb_start))
            f.write("\n".join(instrs))
            f.write("\n----\n")

# Print the path of the output file
print("Output file saved to: {}".format(output_path))
