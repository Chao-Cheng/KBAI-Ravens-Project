import MyPillow as pillow
import Transform as trans
import os, sys


def main():
	here = sys.path[0]

	im1 = pillow.Image.open('A.png')
	im2 = pillow.Image.open('B.png')
	im1, im2 = pillow.normalize(im1, im2)

	print(pillow.getImageMatchScore(im1, im2))

	changed = pillow.getChangedImage(im1, im2)
	changed.save(os.path.join(here, 'changed.png'))

	same = pillow.getSameImage(im1, im2)
	same.save(os.path.join(here, 'same.png'))

	added = pillow.getAdditionsImage(im1, im2)
	added.save(os.path.join(here, 'added.png'))

	subtracted = pillow.getSubtractionsImage(im1, im2)
	subtracted.save(os.path.join(here, 'subtracted.png'))



	# TEST GET PRIORITY TRANSFORMS
	priority_transforms = [trans.Transform(im1)]  # Start the list with a blank transform]

	# If we don't already match, get list of transforms
	if not pillow.imagesMatch(im1, im2):
		# For each static transform, add a Transform to the list
		for stat_trans in trans.STATIC_TRANSFORMS:
			priority_transforms.append(trans.Transform(im1).addStaticTransform(stat_trans))

	# Order our list by how well each one matches im2
	for transform in priority_transforms:
		transform.score = pillow.getImageMatchScore(transform.current_image, im2)
	priority_transforms.sort(key=lambda t: t.score, reverse=True)

	# Put in the add and subtract images
	for transform in priority_transforms:
		transform.setAdditions(im2)
		transform.setSubtractions(im2)

	count = 0
	for transform in priority_transforms:
		count += 1
		name = 'priTrans' + str(count)
		print(name, transform.score, transform.static_transforms)
		transform.current_image.save(os.path.join(here, name + '.png'))
		transform.add_image.save(os.path.join(here, name + '_added.png'))
		transform.subtract_image.save(os.path.join(here, name + '_subtracted.png'))

	# END TEST GET PRIORITY TRANSFORMS


if __name__ == "__main__":
	main()