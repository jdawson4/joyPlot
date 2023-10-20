# Author: Jacob Dawson
#
# The goal of this file is to create a joyplot from data gathered by NASA
# spacecraft regarding phytoplankton presence in the ocean. First we'll
# need to do some beautifulsouping and download photos from NASA's Ocean
# Color website. Then, we will have to calculate when/how much phytoplankton
# there is in the ocean in an individual photo (likely in just one hemisphere).
# Then, we'll take the average of that, and we can plot a joyplot!

import requests
#from bs4 import BeautifulSoup
import time
from PIL import Image

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

if __name__=='__main__':
    pass

    # uncomment if the images aren't loaded
    #getPhotos()
