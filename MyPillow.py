from PIL import Image, ImageChops as Chops, ImageFilter as Filter
import numpy as np

IMAGE_SIDE = 180
IMAGE_SIZE = (IMAGE_SIDE, IMAGE_SIDE)
MATCHED_IMAGE_THRESHOLD = 98.5
BLACK_WHITE_CUTOFF = 65  # Tend to only take things as black if they are very black
FUZZY_MATCH_RESOLUTION = IMAGE_SIDE // 30  # won't offset image more than 3 pixels when matching
FUZZIFICATION_LIMIT = 1  # FUZZY_MATCH_RESOLUTION // 2  # how much to blur the image

corner_reduce = Image.open('corner-reduce.png')

# ADD/SUB IMAGES
def get_same_image(im1, im2):
	return Chops.invert(get_changed_image(im1, im2))


def get_changed_image(im1, im2):
	return Chops.difference(im1, im2)


def get_additions_image(im1, im2):
	return Chops.subtract(fuzzify(im1), im2)


def get_subtractions_image(im1, im2):
	return Chops.subtract(fuzzify(im2), im1)
# END ADD/SUB IMAGES

# STATIC TRANSFORMATIONS
def reflect_horizontal(im):
	return im.transpose(Image.FLIP_LEFT_RIGHT)


def reflect_vertical(im):
	return im.transpose(Image.FLIP_TOP_BOTTOM)


def rotate_90(im):
	return im.transpose(Image.ROTATE_90)


def rotate_180(im):
	return im.transpose(Image.ROTATE_180)


def rotate_270(im):
	return im.transpose(Image.ROTATE_270)


def rotate_45(im):
	return Chops.add(im.rotate(45, resample=Image.BICUBIC), corner_reduce)


def rotate_135(im):
	return Chops.add(im.rotate(135, resample=Image.BICUBIC), corner_reduce)


def rotate_225(im):
	return Chops.add(im.rotate(225, resample=Image.BICUBIC), corner_reduce)


def rotate_315(im):
	return Chops.add(im.rotate(315, resample=Image.BICUBIC), corner_reduce)
# END STATIC TRANSFORMATIONS


# Adds im2 to im1 as black, returns result
def add_to(im1, im2):
	return Chops.subtract(im1, im2)


# Subtracts im2 from im1 as black, returns result
def subtract_from(im1, im2):
	return Chops.add(im1, im2)


def images_match(im1, im2, fuzzy=True):
	return get_image_match_score(im1, im2, fuzzy) > MATCHED_IMAGE_THRESHOLD


# returns [im1, im2] as optimally matching images offset by a few pixels
def fuzzy_match(im1, im2):
	up, down, left, right = True, True, True, True

	improvements = 0
	max_score = get_image_match_score(im1, im2)
	while True:
		offset_image = None
		search_direction = None

		# offset the image
		if up:
			offset_image = Chops.offset(im2, 0, -1)
			search_direction = 'UP'
		elif down:
			offset_image = Chops.offset(im2, 0, 1)
			search_direction = 'DOWN'
		elif left:
			offset_image = Chops.offset(im2, -1, 0)
			search_direction = 'LEFT'
		elif right:
			offset_image = Chops.offset(im2, 1, 0)
			search_direction = 'RIGHT'
		else:
			break

		# test the offset image to see if it's better
		score = get_image_match_score(im1, offset_image)
		if score > max_score and improvements <= FUZZY_MATCH_RESOLUTION:  # if so, update im2
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
# Fuzzy=True offsets the images a few pixels so they optimally match before returning score
def get_image_match_score(im1, im2, fuzzy=False):
	if fuzzy: im1, im2 = fuzzy_match(im1, im2)
	return percent(get_same_image(im1, im2))


# Returns the percentage of non-zero pixels in the image
def percent(im):
	total_pixels = im.size[0] * im.size[1]
	return (count(im) / total_pixels) * 100


# Returns a count of the non-zero (white) pixels in the image
def count(im, color='white'):
	if color == 'black': im = Chops.invert(im)
	return np.count_nonzero(im)


# Standardize the image's size to 184x184 and turn everything black or white
def normalize(*images):
	images = list(images)
	for i in range(len(images)):
		image = images[i]

		image = image.resize(IMAGE_SIZE)
		image = black_or_white(image)

		images[i] = image

	return images


def black_or_white(image):
	gray_scale = image.convert('L')

	array = np.asarray(gray_scale).copy()  # convert to numpy array
	# Color values are not evenly divided on purpose to emphasize white as a background color
	array[array < BLACK_WHITE_CUTOFF] = 0  # Darker colors go to black
	array[array >= BLACK_WHITE_CUTOFF] = 255  # Lighter colors go to white

	return Image.fromarray(array)


# Returns a "blurred" version of the image that is the image smeared around by a few pixels
# Used when calculating additions and subtractions to avoid slivers of mis-aligned images
def fuzzify(im):
	inv = Chops.invert(im)
	# Generate a list of images that are our offsets from the original
	for i in range(-FUZZIFICATION_LIMIT, FUZZIFICATION_LIMIT + 1):
		for j in range(-FUZZIFICATION_LIMIT, FUZZIFICATION_LIMIT + 1):
			inv = Chops.add(inv, Chops.offset(inv, i, j))  # add the offset image

	return Chops.invert(inv)


def count_regions(image, color='black'):
	image = image.resize((30, 30))  # Have to size this down to avoid stack overflow errors

	if color == 'black': pix_val = 0
	elif color == 'white': pix_val = 255
	array = np.asarray(image)
	array.flags.writeable = True

	count = 0
	for r in range(len(array)):
		for c in range(len(array[0])):
			if array[r][c] == pix_val:  # If this pixel matches what we are looking for
				count += 1
				recursive_fill(array, r, c, count, pix_val)
	# print(array)

	return count


def recursive_fill(array, r, c, num, pix_val):
	array[r][c] = num

	up = r-1
	if 0 <= up and array[up][c] == pix_val:
		recursive_fill(array, up, c, num, pix_val)

	down = r+1
	if down < len(array) and array[down][c] == pix_val:
		recursive_fill(array, down, c, num, pix_val)

	left = c-1
	if 0 <= left and array[r][left] == pix_val:
		recursive_fill(array, r, left, num, pix_val)

	right = c+1
	if right < len(array[0]) and array[r][right] == pix_val:
		recursive_fill(array, r, right, num, pix_val)


# Returns the difference in count of black pixels between the two images
def black_pixel_count_difference(im1, im2):
	im1, im2 = Chops.invert(im1), Chops.invert(im2)
	return count(im2) - count(im1)


# Percent (0-100) of black pixels that are the same in im2 as im1
def black_match_rate(im1, im2):
	im1_black = count(im1, color='black')
	im2_black = count(im2, color='black')
	total = im1_black + im2_black

	changed = count(get_changed_image(im1, im2))

	same = (total - changed) / 2

	return same / max(im1_black, im2_black) * 100
