import numpy as np
import matplotlib.pyplot as plt
# Your measured dB values
measured_db = np.array([33.97, 44.85, 86.59])

# Convert measured dB values to linear scale
measured_linear = 10 ** (measured_db / 20)

# Your applied dB values
applied_db = np.array([0, 5, 10])

# Convert applied dB values to linear scale
applied_linear = 10 ** (applied_db / 20)

# plot the result
plt.plot(applied_linear, measured_linear)
plt.xlabel('Applied Gain (linear)')
plt.ylabel('Measured Gain (linear)')
plt.title('Gain Curve')
plt.grid()
plt.show()

