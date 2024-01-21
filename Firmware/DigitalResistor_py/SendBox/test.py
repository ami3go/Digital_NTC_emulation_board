# from micropython import const

def range_check(val, min, max):
    if val > max:
        # print(f"Wrong {val_name}: {val}. Max output should be less then {max} V")
        val = max
    if val < min:
        # print(f"Wrong {val_name}: {val}. Should be >= {min}")
        val = min
    return val

def get_command( cmd="nop", ch=0, data=0):
    cmd_nop = 0x00
    cmd_wrt_rdac = 0b10110000  # cmd 11 datasheet
    cmd_store_wiper_eemem = 0b00100000
    cmd_rd_rdac = 0b10100000
    data = int(range_check(data, 0, 1024))
    ch = int(range_check(ch, 0, 1))
    # set cmd then
    cmd_var = 0
    if cmd == "wrt":
        cmd_var = cmd_wrt_rdac
    elif cmd == "rd":
        cmd_var = cmd_rd_rdac
    elif cmd == "srt_wiper":
        cmd_var = cmd_store_wiper_eemem
    else:
        cmd_var = cmd_nop
    adc_value = (cmd_var << 16) | (ch << 16) | data
    return adc_value


cmd_array = [0xb10100,0xb00100,0xb10100,0xb00100,0xb10100,0xb00100,0xb10100,0xb00100]

# Example array of 24-bit values
# array_of_24_bits = [0x123456, 0xAABBCC, 0xDEADBEEF]
array_of_24_bits = cmd_array
# Function to convert 24-bit values to 8-bit values
def convert_to_bytes(value):
    byte1 = (value >> 16) & 0xFFFF
    byte3 = value & 0xFFFF
    return [byte1, byte3]

# Convert each 24-bit value to an array of 8-bit values
array_of_8_bits = [convert_to_bytes(value) for value in array_of_24_bits]

# Flatten the list of lists into a single list
flat_array_of_8_bits = [hex(byte) for sublist in array_of_8_bits for byte in sublist]

# Print the result
print("Original array of 24 bits:", array_of_24_bits)
print("Converted array of 8 bits:", flat_array_of_8_bits)
array = [0]*8
print(array)