# import sys
# sys.path.append('..')  # Add the parent directory to the path
import AD5235m
test = AD5235m.AD9235_class(0,0,1,2,3,4)
test.set_raw_val(0,2000)
test.set_raw_val(1,100)
test.set_raw_val(2,200)
test.set_raw_val(3,500)
test.set_raw_val(4,1000)
test.set_raw_val(5,800)
test.set_Ohm_val(6,750)
test.set_Ohm_val(7,250000)
test.test_buffer()

