# Author: Jacob Dawson
#
# This is the script that actually does the joy plotting!

from scipy.io import wavfile
import sys
import os.path
import matplotlib.pyplot as plt
#from IPython.display import display
import numpy as np
import joypy
import pandas as pd

def main(filename):
    print("\nNow reading", filename)

    # read raw file and get some facts
    rate, data = wavfile.read('wavs/'+filename)
    length = data.shape[0] / rate # length in seconds

    # normally, we have two channels, when we only need 1:
    if data.shape[1]==2:
        data = data[:,0]
    data = np.absolute(data) # and we don't need negatives

    # get some details:
    print("Shape:", data.shape)
    print("Rate:", rate)
    print("Length:", length)

    # now let's take every m sections
    x = 3
    secondsToInclude=2
    m = int(length)//x # and...every xth second?
    mths = []
    stepsize = int(len(data)//m)
    for i in range(0, len(data)-stepsize, stepsize):
        mths.append(data[i:i+int(secondsToInclude*rate)])
    mths = np.array(mths)
    print(mths.shape[0], "graphs, each",mths.shape[1],"long")

    '''
    # ok and what if we just look at the first second of that set?
    mFirstSeconds = []
    n = mths.shape[1] // rate # this is how long each second is in the mths
    stepsize = mths.shape[1]//n
    for i in mths:
        mFirstSeconds.append(i[0:stepsize])
    mFirstSeconds = np.array(mFirstSeconds)
    #print(mFirstSeconds.shape)
    '''

    # ok, now let's make our joyplot!
    df = pd.DataFrame(
        np.transpose(mths),
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
    plt.savefig('plots/'+filename[:-4]+'.png', dpi=500)
    #plt.show()

if __name__ == '__main__':
    if len(sys.argv) > 1:
        if os.path.isfile('wavs/' + sys.argv[1]):
            main(sys.argv[1])
        elif os.path.isfile('wavs/' + sys.argv[1] + '.wav'):
            main(sys.argv[1] + '.wav')
