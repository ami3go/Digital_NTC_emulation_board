# # from micropython import const
#
# def range_check(val, min, max):
#     if val > max:
#         # print(f"Wrong {val_name}: {val}. Max output should be less then {max} V")
#         val = max
#     if val < min:
#         # print(f"Wrong {val_name}: {val}. Should be >= {min}")
#         val = min
#     return val
#
# def get_command( cmd="nop", ch=0, data=0):
#     cmd_nop = 0x00
#     cmd_wrt_rdac = 0b10110000  # cmd 11 datasheet
#     cmd_store_wiper_eemem = 0b00100000
#     cmd_rd_rdac = 0b10100000
#     data = int(range_check(data, 0, 1024))
#     ch = int(range_check(ch, 0, 1))
#     # set cmd then
#     cmd_var = 0
#     if cmd == "wrt":
#         cmd_var = cmd_wrt_rdac
#     elif cmd == "rd":
#         cmd_var = cmd_rd_rdac
#     elif cmd == "srt_wiper":
#         cmd_var = cmd_store_wiper_eemem
#     else:
#         cmd_var = cmd_nop
#     adc_value = (cmd_var << 16) | (ch << 16) | data
#     return adc_value
#
#
# cmd_array = [0xb10100,0xb00100,0xb10100,0xb00100,0xb10100,0xb00100,0xb10100,0xb00100]
#
# # Example array of 24-bit values
# # array_of_24_bits = [0x123456, 0xAABBCC, 0xDEADBEEF]
# array_of_24_bits = cmd_array
# # Function to convert 24-bit values to 8-bit values
# def convert_to_bytes(value):
#     byte1 = (value >> 16) & 0xFFFF
#     byte3 = value & 0xFFFF
#     return [byte1, byte3]
#
# # Convert each 24-bit value to an array of 8-bit values
# array_of_8_bits = [convert_to_bytes(value) for value in array_of_24_bits]
#
# # Flatten the list of lists into a single list
# flat_array_of_8_bits = [hex(byte) for sublist in array_of_8_bits for byte in sublist]
#
# # Print the result
# print("Original array of 24 bits:", array_of_24_bits)
# print("Converted array of 8 bits:", flat_array_of_8_bits)
# array = [0]*8
# print(array)

import cmd, sys
from turtle import *

class TurtleShell(cmd.Cmd):
    intro = 'Welcome to the turtle shell.   Type help or ? to list commands.\n'
    prompt = '(turtle) '
    file = None

    # ----- basic turtle commands -----
    def do_forward(self, arg):
        'Move the turtle forward by the specified distance:  FORWARD 10'
        forward(*parse(arg))
    def do_right(self, arg):
        'Turn turtle right by given number of degrees:  RIGHT 20'
        right(*parse(arg))
    def do_left(self, arg):
        'Turn turtle left by given number of degrees:  LEFT 90'
        left(*parse(arg))
    def do_goto(self, arg):
        'Move turtle to an absolute position with changing orientation.  GOTO 100 200'
        goto(*parse(arg))
    def do_home(self, arg):
        'Return turtle to the home position:  HOME'
        home()
    def do_circle(self, arg):
        'Draw circle with given radius an options extent and steps:  CIRCLE 50'
        circle(*parse(arg))
    def do_position(self, arg):
        'Print the current turtle position:  POSITION'
        print('Current position is %d %d\n' % position())
    def do_heading(self, arg):
        'Print the current turtle heading in degrees:  HEADING'
        print('Current heading is %d\n' % (heading(),))
    def do_color(self, arg):
        'Set the color:  COLOR BLUE'
        color(arg.lower())
    def do_undo(self, arg):
        'Undo (repeatedly) the last turtle action(s):  UNDO'
    def do_reset(self, arg):
        'Clear the screen and return turtle to center:  RESET'
        reset()
    def do_bye(self, arg):
        'Stop recording, close the turtle window, and exit:  BYE'
        print('Thank you for using Turtle')
        self.close()
        bye()
        return True

    # ----- record and playback -----
    def do_record(self, arg):
        'Save future commands to filename:  RECORD rose.cmd'
        self.file = open(arg, 'w')
    def do_playback(self, arg):
        'Playback commands from a file:  PLAYBACK rose.cmd'
        self.close()
        with open(arg) as f:
            self.cmdqueue.extend(f.read().splitlines())
    def precmd(self, line):
        line = line.lower()
        if self.file and 'playback' not in line:
            print(line, file=self.file)
        return line
    def close(self):
        if self.file:
            self.file.close()
            self.file = None

def parse(arg):
    'Convert a series of zero or more numbers to an argument tuple'
    return tuple(map(int, arg.split()))

if __name__ == '__main__':
    TurtleShell().cmdloop()