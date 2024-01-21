def set_buffer( dev, val):

    temp = [0]*8
    temp[dev] = val
    return temp


print(set_buffer(4, 100))
