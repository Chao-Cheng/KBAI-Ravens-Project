from PIL import Image, ImageChops as chops
import numpy as np

IMAGE_SIZE = (100, 100)

def getSameImage(im1, im2):
    return chops.invert(getChangedImage(im1, im2))


def getChangedImage(im1, im2):
    return chops.difference(im1, im2)


def getAdditionsImage(im1, im2):
    return chops.subtract(im1, im2)


def getSubtractionsImage(im1, im2):
    return chops.subtract(im2, im1)


# Given two images, returns percentage of matching pixels (0 - 100)
def getImageMatchScore(im1, im2):
    different_pixels = np.count_nonzero(getChangedImage(im1, im2))
    total_pixels = im1.size[0] * im1.size[1]
    return (1 - (different_pixels / total_pixels)) * 100


# Standardize the image's size to 184x184 and turn everything black or white
def normalize(*images):
    images = list(images)
    for i in range(len(images)):
        image = images[i]

        image = image.resize(IMAGE_SIZE)
        image = blackOrWhite(image)

        images[i] = image

    return images


def blackOrWhite(image):
    gray_scale = image.convert('L')

    array = np.asarray(gray_scale).copy()  # convert to numpy array
    array[array < 128] = 0  # Darker colors go to black
    array[array >= 128] = 255  # Lighter colors go to white

    return Image.fromarray(array)


def printColors(*images):
    for image in images:
        print(image.getcolors())
