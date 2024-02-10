#
# # This is a sample Python script.
# import AD5235
# import machine
# import rp2
# import time
# machine.freq()          # get the current frequency of the CPU
# machine.freq(240000000) # set the CPU frequency to 240 MHz
#
#
# def test():
#     # Use a breakpoint in the code line below to debug your script.
#     print(f'Hi, rp2040')  # Press Ctrl+F8 to toggle the breakpoint.
#     dig_res = AD5235.AD9235_class(0,1,2,3,4,4)
#     for i in range(8):
#         dig_res.set_buffer(i,i#     test()
#
# cmd = [11534340, 11599876, 11534340, 11599876, 11534340, 11599876, 11534340, 11599876]
# cmd1 = []
# cmd2 = []
# for index, value in enumerate(cmd):
#     if index % 2 != 0:
#         cmd1.append(value)
#     else:
#         cmd2.append(value)
cmd = [[177, 0, 0], [177, 0, 0], [177, 0, 0], [177, 0, 0]]
cmd1 = bytearray(cmd)
print(cmd)
print(cmd1)
# print(cmd2)