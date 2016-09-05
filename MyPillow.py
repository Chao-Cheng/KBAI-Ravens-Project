from PIL import Image, ImageChops as chops
import numpy as np

IMAGE_SIZE = (100, 100)
MATCHED_IMAGE_THRESHOLD = 98

def getSameImage(im1, im2):
	return chops.invert(getChangedImage(im1, im2))


def getChangedImage(im1, im2):
	return chops.difference(im1, im2)


def getAdditionsImage(im1, im2):
	return chops.subtract(im1, im2)


def getSubtractionsImage(im1, im2):
	return chops.subtract(im2, im1)


def reflectHorizontal(im):
	return im.transpose(Image.FLIP_LEFT_RIGHT)


def reflectVertical(im):
	return im.transpose(Image.FLIP_TOP_BOTTOM)


def rotate90(im):
	return im.transpose(Image.ROTATE_90)


def rotate180(im):
	return im.transpose(Image.ROTATE_180)


def rotate270(im):
	return im.transpose(Image.ROTATE_270)


def imagesMatch(im1, im2):
	return getImageMatchScore(im1, im2) > MATCHED_IMAGE_THRESHOLD

# Given two images, returns percentage of matching pixels (0 - 100)
def getImageMatchScore(im1, im2):
	different_pixels = count(getChangedImage(im1, im2))
	total_pixels = im1.size[0] * im1.size[1]
	return (1 - (different_pixels / total_pixels)) * 100

# Returns the non-zero pixels in the image
def count(im):
	return np.count_nonzero(im)


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
	# Color values are not evenly divided on purpose to emphasize white as a background color
	array[array < 200] = 0  # Darker colors go to black
	array[array >= 200] = 255  # Lighter colors go to white

	return Image.fromarray(array)


def printColors(*images):
	for image in images:
		print(image.getcolors())
