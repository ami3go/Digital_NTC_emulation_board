# def set_buffer(dev, val):
#
#     temp = [0]*8
#     temp[dev] = val
#     return temp
#
#
# print(set_buffer(4, 100))
temp  = [0,1] * 4
print(len(temp)-1)
print(temp[0])
print(temp[1])
print(temp[2])

# def get_adc_val_from_res_val(res_Ohm):
#     Rw = 50 # wiper resistance, datasheet
#     Rab = 250000 # full scale resistance 250k -> in Ohm
#     cnt = 1024*(res_Ohm-Rw)/Rab
#     cnt = int(round(cnt, 0))
#     return cnt
# check_values =     [0,250, 500, 750, 1000, 10000, 249900]
# for val in check_values:
#     print(get_adc_val_from_res_val(val))
