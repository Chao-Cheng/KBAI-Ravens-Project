from PIL import Image, ImageChops as Chops, ImageFilter as Filter
import numpy as np

from Agent import PixelAnalysis
import MyPillow as Pillow
import Transform as Trans
import os
import sys


def main():
	here = sys.path[0]

	imA = Image.open('A.png')
	imB = Image.open('B.png')
	imC = Image.open('C.png')
	imD = Image.open('D.png')
	imE = Image.open('E.png')
	imF = Image.open('F.png')
	imG = Image.open('G.png')
	imH = Image.open('H.png')
	imA, imB, imC, imD, imE, imF, imG, imH = Pillow.normalize(imA, imB, imC, imD, imE, imF, imG, imH)

	im1 = Image.open('1.png')
	im2 = Image.open('2.png')
	im3 = Image.open('3.png')
	im4 = Image.open('4.png')
	im5 = Image.open('5.png')
	im6 = Image.open('6.png')
	im7 = Image.open('7.png')
	im8 = Image.open('8.png')
	im1, im2, im3, im4, im5, im6, im7, im8 = Pillow.normalize(im1, im2, im3, im4, im5, im6, im7, im8)

	print(PixelAnalysis(imA, imB, imC))

	print()
	print(PixelAnalysis(imD, imE, imF))

	print()
	print(PixelAnalysis(imG, imH, im1))

	print()
	print(PixelAnalysis(imG, imH, im2))

	print()
	print(PixelAnalysis(imG, imH, im3))

	print()
	print(PixelAnalysis(imG, imH, im4))

	print()
	print(PixelAnalysis(imG, imH, im5))

	print()
	print(PixelAnalysis(imG, imH, im6))

	print()
	print(PixelAnalysis(imG, imH, im7))

	print()
	print(PixelAnalysis(imG, imH, im8))


	# changed = Pillow.get_changed_image(im1, im3)
	# changed.save(os.path.join(here, 'changed.png'))
	#
	# same = Pillow.get_same_image(im1, im2)
	# same.save(os.path.join(here, 'same.png'))
	#
	# added = Pillow.get_additions_image(im1, im2)
	# added.save(os.path.join(here, 'added.png'))
	#
	# subtracted = Pillow.get_subtractions_image(im1, im2)
	# subtracted.save(os.path.join(here, 'subtracted.png'))

	# TEST GET PRIORITY TRANSFORMS
	# priority_transforms = [trans.Transform(im1)]  # Start the list with a blank transform
	#
	# # If we don't already match, get list of transforms
	# if not pillow.images_match(im1, im2):
	# 	# For each static transform, add a Transform to the list
	# 	for stat_trans in trans.STATIC_TRANSFORMS:
	# 		priority_transforms.append(trans.Transform(im1).add_static_transform(stat_trans))
	#
	# # Order our list by how well each one matches im2
	# for transform in priority_transforms:
	# 	transform.score = pillow.get_image_match_score(transform.current_image, im2)
	# priority_transforms.sort(key=lambda t: t.score, reverse=True)
	#
	# # Put in the add and subtract images
	# for transform in priority_transforms:
	# 	transform.set_additions(im2)
	# 	transform.set_subtractions(im2)
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