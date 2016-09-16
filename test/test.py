import MyPillow as Pillow
from PIL import Image, ImageChops as Chops
import Transform as Trans
import os
import sys


def main():
	here = sys.path[0]

	im1 = Image.open('A.png')
	im2 = Image.open('B.png')
	corner_reduce = Chops.invert(Image.open('cornerReduce.png'))
	im1, im2, corner_reduce = Pillow.normalize(im1, im2, corner_reduce)

	# im1 = pillow.chops.offset(im1, 0, 10)

	# im1, im2 = pillow.fuzzyMatch(im1, im2)

	print(Pillow.getImageMatchScore(im1, im2))
	print(Pillow.getImageMatchScore(im1, im2, fuzzy=True))

	corner_reduce.save(os.path.join(here, 'corner-reduce.png'))

	test = im1.rotate(45, resample=Image.BICUBIC)
	test = Chops.add(test, corner_reduce)
	test.save(os.path.join(here, 'test.png'))

	changed = Pillow.getChangedImage(im1, im2)
	changed.save(os.path.join(here, 'changed.png'))

	same = Pillow.getSameImage(im1, im2)
	same.save(os.path.join(here, 'same.png'))

	added = Pillow.getAdditionsImage(im1, im2)
	added.save(os.path.join(here, 'added.png'))

	subtracted = Pillow.getSubtractionsImage(im1, im2)
	subtracted.save(os.path.join(here, 'subtracted.png'))

	# TEST GET PRIORITY TRANSFORMS
	# priority_transforms = [trans.Transform(im1)]  # Start the list with a blank transform
	#
	# # If we don't already match, get list of transforms
	# if not pillow.imagesMatch(im1, im2):
	# 	# For each static transform, add a Transform to the list
	# 	for stat_trans in trans.STATIC_TRANSFORMS:
	# 		priority_transforms.append(trans.Transform(im1).addStaticTransform(stat_trans))
	#
	# # Order our list by how well each one matches im2
	# for transform in priority_transforms:
	# 	transform.score = pillow.getImageMatchScore(transform.current_image, im2)
	# priority_transforms.sort(key=lambda t: t.score, reverse=True)
	#
	# # Put in the add and subtract images
	# for transform in priority_transforms:
	# 	transform.setAdditions(im2)
	# 	transform.setSubtractions(im2)
	#
	# count = 0
	# for transform in priority_transforms:
	# 	count += 1
	# 	name = 'priTrans' + str(count)
	# 	print(name, transform.score, transform.static_transforms)
	# 	transform.current_image.save(os.path.join(here, name + '.png'))
	# 	transform.add_image.save(os.path.join(here, name + '_added.png'))
	# 	transform.subtract_image.save(os.path.join(here, name + '_subtracted.png'))

	# END TEST GET PRIORITY TRANSFORMS


if __name__ == "__main__":
	main()