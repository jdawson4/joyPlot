# Author: Jacob Dawson
#
# This is the script that actually does the joy plotting!

from scipy.io import wavfile
import os
import matplotlib.pyplot as plt
#from IPython.display import display
import numpy as np
import joypy
import pandas as pd

for file in os.listdir('wavs'):
    print("\nNow reading", file)

    # read raw file and get some facts
    rate, data = wavfile.read('wavs/'+file)
    length = data.shape[0] / rate # length in seconds

    # we actually have two channels, we only need 1:
    data = data[:,0]
    data = np.absolute(data) # and we don't need negatives

    # get some details:
    print("Shape:", data.shape)
    print("Rate:", rate)
    print("Length:", length)

    # now let's take every m sections
    x = 2
    m = int(length)//x # and...every xth second?
    mths = []
    stepsize = len(data)//m
    for i in range(0, len(data)-stepsize, stepsize):
        mths.append(data[i:i+stepsize])
    mths = np.array(mths)
    #print(mths.shape)

    # ok and what if we just look at the first second of that set?
    mFirstSeconds = []
    n = mths.shape[1] // rate # this is how long each second is in the mths
    stepsize = mths.shape[1]//n
    for i in mths:
        mFirstSeconds.append(i[0:stepsize])
    mFirstSeconds = np.array(mFirstSeconds)
    #print(mFirstSeconds.shape)

    # ok, now let's make our joyplot!
    df = pd.DataFrame(
        np.transpose(mFirstSeconds),
    )
    #display(df)
    fig, axes = joypy.joyplot(
        data=df,
        xlabels=False,
        ylabels=False,
        grid=False, fill=False, background='w', linecolor="k", linewidth=1,
        legend=False, overlap=0.5,
        #figsize=(6,5)
    )

    plt.subplots_adjust(left=.333, right=.667, top=1, bottom=0) # rule of thirds!
    #for a in axes[:-1]:
    #    a.set_xlim([-1*mFirstSeconds.shape[1],2*mFirstSeconds.shape[1]])
    plt.savefig('plots/'+file[:-4]+'.png', dpi=500)
    #plt.show()
