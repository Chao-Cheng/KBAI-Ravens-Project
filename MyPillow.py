from PIL import Image, ImageChops as chops
import numpy as np

IMAGE_SIDE = 180
IMAGE_SIZE = (IMAGE_SIDE, IMAGE_SIDE)
MATCHED_IMAGE_THRESHOLD = 99
FUZZY_DIRECTION_IMPROVE_LIMIT = IMAGE_SIDE // 20  # won't offset image more than 3 pixels when matching


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


# Adds im2 to im1 as black, returns result
def addTo(im1, im2):
	return chops.subtract(im1, im2)


# Subtracts im2 from im1 as black, returns result
def subtractFrom(im1, im2):
	return chops.add(im1, im2)


def imagesMatch(im1, im2):
	return getImageMatchScore(im1, im2, fuzzy=True) > MATCHED_IMAGE_THRESHOLD


# returns [im1, im2] as optimally matching images offset by a few pixels
def fuzzyMatch(im1, im2):
	up, down, left, right = True, True, True, True

	improvements = 0
	max_score = getImageMatchScore(im1, im2)
	while True:
		offset_image = None
		search_direction = None

		# offset the image
		if up:
			offset_image = chops.offset(im2, 0, -1)
			search_direction = 'UP'
		elif down:
			offset_image = chops.offset(im2, 0, 1)
			search_direction = 'DOWN'
		elif left:
			offset_image = chops.offset(im2, -1, 0)
			search_direction = 'LEFT'
		elif right:
			offset_image = chops.offset(im2, 1, 0)
			search_direction = 'RIGHT'
		else:
			break

		# test the offset image to see if it's better
		score = getImageMatchScore(im1, offset_image)
		if score > max_score and improvements <= FUZZY_DIRECTION_IMPROVE_LIMIT:  # if so, update im2
			im2 = offset_image
			max_score = score
			improvements += 1
		# print('Improved', search_direction)
		else:  # if not, turn off whatever step we just took
			# print('Failed to improve', search_direction)
			if search_direction == 'UP':
				up = False
			elif search_direction == 'DOWN':
				down = False
			elif search_direction == 'LEFT':
				left = False
			elif search_direction == 'RIGHT':
				right = False

			improvements = 0

	return [im1, im2]


# Given two images, returns percentage of matching pixels (0 - 100)
# Note: Offsets the images a few pixels so they optimally match before returning score
def getImageMatchScore(im1, im2, fuzzy=False):
	if fuzzy: im1, im2 = fuzzyMatch(im1, im2)
	return percent(getSameImage(im1, im2))


# Returns the percentage of non-zero pixels in the image
def percent(im):
	total_pixels = im.size[0] * im.size[1]
	return (count(im) / total_pixels) * 100


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
