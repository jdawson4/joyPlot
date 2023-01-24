# Author: Jacob Dawson
#
# This is the script that actually does the joy plotting!

from scipy.io import wavfile
import os
import matplotlib.pyplot as plt
import numpy as np

for file in os.listdir('wavs'):
    print("\n\nNow reading", file)

    # read raw file and get some facts
    rate, data = wavfile.read('wavs/'+file)
    length = data.shape[0] / rate # length in seconds

    # we actually have two channels, we only need 1:
    data = data[:,0]
    data = np.absolute(data)

    # get some details:
    print("Shape:", data.shape)
    print("Rate:", rate)
    print("Length:", length)

    # now let's take every m sections
    m = int(length)//10 # and...every 10th second?
    mths = []
    stepsize = len(data)//m
    for i in range(0, len(data)-1, stepsize):
        mths.append(data[i:i+stepsize])
        #print(np.amin(data[i:i+stepsize]))
        #print(np.amax(data[i:i+stepsize]))
    mths = np.array(mths)
    print(mths.shape)

    # ok and what if we just look at the first second of that set?
    mFirstSeconds = []
    n = mths.shape[1] // rate # this is how long each second is in the mths
    stepsize = mths.shape[1]//n
    for i in mths:
        mFirstSeconds.append(i[0:stepsize])
    mFirstSeconds = np.array(mFirstSeconds)
    print(mFirstSeconds.shape)

    # and let's do some plotting:
    for i in range(m):
        time = np.linspace(0., (length/m)/n, mFirstSeconds[0].shape[0])
        plt.plot(time, mFirstSeconds[i], label="Left channel")
        plt.xlabel("Time [s]")
        plt.ylabel("Amplitude")
        plt.show()
