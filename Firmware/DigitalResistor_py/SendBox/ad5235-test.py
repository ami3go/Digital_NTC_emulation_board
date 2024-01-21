# import sys
# sys.path.append('..')  # Add the parent directory to the path
import AD5235

test = AD5235.AD9235_class(0,0,1,2,3,4)
test.set_buffer(0,2000)
test.set_buffer(1,100)
test.set_buffer(2,200)
test.set_buffer(3,500)
test.set_buffer(4,1000)
test.set_buffer(5,800)
test.set_buffer(6,900)
test.set_buffer(7,1000)
test.test_buffer()
