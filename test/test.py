from PIL import Image, ImageChops as Chops, ImageFilter as Filter
import numpy as np

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

	print('A TO B')
	print(Pillow.count(imA, 'black'), Pillow.count(imB, 'black'))
	print(Pillow.black_pixel_count_difference(imA, imB), Pillow.black_match_rate(imA, imB))
	print()
	print('B TO C')
	print(Pillow.count(imB, 'black'), Pillow.count(imC, 'black'))
	print(Pillow.black_pixel_count_difference(imB, imC), Pillow.black_match_rate(imB, imC))
	print()
	print('D TO E')
	print(Pillow.count(imD, 'black'), Pillow.count(imE, 'black'))
	print(Pillow.black_pixel_count_difference(imD, imE), Pillow.black_match_rate(imD, imE))
	print()
	print('E TO F')
	print(Pillow.count(imE, 'black'), Pillow.count(imF, 'black'))
	print(Pillow.black_pixel_count_difference(imE, imF), Pillow.black_match_rate(imE, imF))
	print()
	print('G TO H')
	print(Pillow.count(imG, 'black'), Pillow.count(imH, 'black'))
	print(Pillow.black_pixel_count_difference(imG, imH), Pillow.black_match_rate(imG, imH))
	print()
	print('H TO ANSWER')
	print(Pillow.count(imH, 'black'), Pillow.count(im4, 'black'))
	print(Pillow.black_pixel_count_difference(imH, im4), Pillow.black_match_rate(imH, im4))

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