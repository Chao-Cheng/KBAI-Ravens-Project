from PIL import Image, ImageChops as chops
import numpy as np
import os

def getSameImage(im1, im2):
    return chops.invert(getChangedImage(im1, im2))


def getChangedImage(im1, im2):
    return chops.difference(im1, im2)


def getAdditionsImage(im1, im2):
    return chops.subtract(im1, im2)


def getSubtractionsImage(im1, im2):
    return chops.subtract(im2, im1)


# Given two images, returns the number of pixels that don't match
# 0 is perfect match, while higher number returned means more pixels are mismatched
def getImageMatchScore(im1, im2):
    return np.count_nonzero(getChangedImage(im1, im2))


# Standardize the image's size to 184x184 and turn everything black or white
def normalize(*images):
    images = list(images)
    for i in range(len(images)):
        image = images[i]

        image = image.resize((184, 184))
        image = blackOrWhite(image)

        images[i] = image

    return images


def blackOrWhite(image):
    gray_scale = image.convert('L')  # to black and white

    array = np.asarray(gray_scale).copy()  # convert to numpy array
    array[array < 128] = 0  # Darker colors go to black
    array[array >= 128] = 255  # Lighter colors go to white

    return Image.fromarray(array)


def printColors(*images):
    for image in images:
        print(image.getcolors())
