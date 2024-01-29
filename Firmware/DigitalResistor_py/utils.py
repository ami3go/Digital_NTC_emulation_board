# Check if a variable is a digit
def is_digit(var):
    return str(var).isdigit() if not isinstance(var, str) else var.isdigit()

# # Test the function
# print(is_digit("123"))  # Output: True
# print(is_digit("abc"))  # Output: False
# print(is_digit(456))     # Output: True
# print(is_digit("789x"))  # Output: False

import pyb

