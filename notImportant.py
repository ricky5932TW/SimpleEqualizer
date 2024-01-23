import numpy as np
import matplotlib.pyplot as plt
# Your measured dB values


import numpy as np

def find_middle_log_scale(num1, num2):
    return np.sqrt(num1 * num2)

# Example usage:
num1 = 1000
num2 = 3000
middle_num = find_middle_log_scale(num1, num2)
print(middle_num)