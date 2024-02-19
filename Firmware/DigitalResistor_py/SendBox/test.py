# #
# # # This is a sample Python script.
# # import AD5235
# # import machine
# # import rp2
# # import time
# # machine.freq()          # get the current frequency of the CPU
# # machine.freq(240000000) # set the CPU frequency to 240 MHz
# #
# #
# # def test():
# #     # Use a breakpoint in the code line below to debug your script.
# #     print(f'Hi, rp2040')  # Press Ctrl+F8 to toggle the breakpoint.
# #     dig_res = AD5235.AD9235_class(0,1,2,3,4,4)
# #     for i in range(8):
# #         dig_res.set_buffer(i,i#     test()
# #
#
# def convert_to_8bits(input):
#     '''
#     converting array of 24bits back into 8 bit for SPI send register
#     :return: array of 3 values by 8 bits each
#     '''
#     cmd = []
#     for value in input:
#         cmd.append( (value >> 16) & 0xFF)
#         cmd.append((value >> 8) & 0xFF)
#         cmd.append( value & 0xFF)
#         # cmd.append(byte1, byte2, byte3)
#     return cmd
#
# # self.buf1_cmd_spi = [item for array in cmd for item in array]
# # cmd = [11534340, 11599876, 11534340, 11599876, 11534340, 11599876, 11534340, 11599876]
# # cmd1 = []
# # cmd2 = []
# # cmd1 = cmd[0::2]
# # cmd2 = cmd[1::2]
#
#
# # cmd = [[177, 0, 0], [177, 0, 0], [177, 0, 0], [177, 0, 0]]
# # cmd1 = bytearray(cmd)
# # print(cmd)
# print(convert_to_8bits([11534340, 11599876, 11534340, 11599876, 11534340, 11599876, 11534340, 11599876]))
# # print(cmd2)
# while True:
#     cmd = input()
#     print(bytearray(cmd.encode()))
#     if bool(cmd):  # Check if there's any data available to read
#         cmd_with_params = cmd.strip()  # Read the command with parameters from UART and decode it
#         print(cmd_with_params)
#         # cli.process_command(cmd_with_params)  # Process the command

a = '\n'
a.remove('\n')