# Author: Jacob Dawson
#
# This is the script that actually does the joy plotting!

from scipy.io import wavfile
import os
import matplotlib.pyplot as plt
import numpy as np

for file in os.listdir('wavs'):
    print("Now reading", file)
    rate, data = wavfile.read('wavs/'+file)
    print("Rate:",rate)
    print("Shape:",data.shape)
    length = data.shape[0] / rate
    time = np.linspace(0., length, data.shape[0])
    plt.plot(time, data[:, 0], label="Left channel")
    plt.xlabel("Time [s]")
    plt.ylabel("Amplitude")
    plt.show()
