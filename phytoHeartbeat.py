# Author: Jacob Dawson
#
# The goal of this file is to create a joyplot from data gathered by NASA
# spacecraft regarding phytoplankton presence in the ocean. First we'll
# need to do some beautifulsouping and download photos from NASA's Ocean
# Color website. Then, we will have to calculate when/how much phytoplankton
# there is in the ocean in an individual photo (likely in just one hemisphere).
# Then, we'll take the average of that, and we can plot a joyplot!

import requests
import time
from PIL import Image
from os import listdir
from os.path import isfile, join
import numpy as np
import pandas as pd
import pickle
import matplotlib.pyplot as plt
import joypy

def getPhotos():
    # using the Level 3 browser, a user can get a list of image URLs to
    # download. I've uploaded a file with all the URLs for the 8-day composite
    # images taken during the spacecraft "Aqua"'s lifetime, estimating the
    # amount of chlorophyll in the ocean. We'll use that to fill a folder with
    # images!
    with open('8day_aqua_modis_lifetime_links.txt') as file:
        lines = [line.rstrip() for line in file]

    i = 0
    for line in lines:
        #print(line)

        i+=1

        # uncomment if you had an error and want to restart
        #if i < 199:
        #    continue
        
        # load and save img
        img = Image.open(requests.get(line, stream=True).raw)
        img.save('chlorImages/'+str(i)+'.png')
        time.sleep(1) # avoid ddos'ing lol

def getNumFromFilename(filename):
    # given a filename like "104.png", return the integer 104
    return int(filename.split('.')[0])

def extractAverages():
    chlorImagesPath = 'chlorImages/'
    files = [f for f in listdir(chlorImagesPath) if isfile(join(chlorImagesPath, f))]
    files.sort(key=getNumFromFilename)
    #print(files)

    averages = []
    for file in files:
        img = np.array(Image.open('chlorImages/' + file))
        img = img[:(img.shape[0]), (img.shape[1]//2):]
        averages.append(np.mean(img))

        #break
    
    return averages

def plotAverages(averages):
    averages = [averages[i:i+45] for i in range(0, len(averages), 45)]
    averages = averages[:-1]
    averages = np.array(averages)
    averages = averages - np.min(averages)
    averages = averages / np.mean(averages)
    df = pd.DataFrame(
        np.transpose(averages),
    )
    # display(df)
    fig, axes = joypy.joyplot(
        data=df,
        xlabels=False,
        ylabels=False,
        grid=False,
        fill=False,
        background="w",
        linecolor="k",
        linewidth=1,
        legend=False,
        overlap=0.5,
        # figsize=(6,5)
    )

    plt.subplots_adjust(left=0.333, right=0.667, top=0.8, bottom=0.2)  # rule of thirds!
    plt.savefig("phytoHeartbeat.png", dpi=500)

if __name__=='__main__':
    pass

    # uncomment if the images aren't loaded
    #getPhotos()

    # uncomment if the averages aren't pickled yet
    # get the averages
    #averages = extractAverages()
    # and let's save those to a file I guess
    #with open('averages.pickle', 'wb') as handle:
    #    pickle.dump(averages, handle, protocol=pickle.HIGHEST_PROTOCOL)

    # and let's reload it because I'd like to avoid that processing again
    with open('averages.pickle', 'rb') as handle:
        averages = pickle.load(handle)
    #print(averages)

    # and let's make our joyplot with that:
    plotAverages(averages)
