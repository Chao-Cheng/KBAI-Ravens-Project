import MyPillow as Pillow

class StaticTransform:
	def __init__(self, type, order):
		self.type = type
		self.order = order

STATIC_TRANSFORMS = [
	StaticTransform('REFLECT_HORIZONTAL', 1),
	StaticTransform('REFLECT_VERTICAL', 1),
	StaticTransform('ROTATE_90', 2),
	StaticTransform('ROTATE_180', 2),
	StaticTransform('ROTATE_270', 2),
	StaticTransform('ROTATE_45', 3),
	StaticTransform('ROTATE_135', 3),
	StaticTransform('ROTATE_225', 3),
	StaticTransform('ROTATE_315', 3)
]


# Applies the static transform to the imgage, returning the resultant image
def applyStaticTransform(im, static_transform):
	if static_transform.type == 'REFLECT_HORIZONTAL':
		return Pillow.reflectHorizontal(im)
	elif static_transform.type == 'REFLECT_VERTICAL':
		return Pillow.reflectVertical(im)
	elif static_transform.type == 'ROTATE_90':
		return Pillow.rotate90(im)
	elif static_transform.type == 'ROTATE_180':
		return Pillow.rotate180(im)
	elif static_transform.type == 'ROTATE_270':
		return Pillow.rotate270(im)
	elif static_transform.type == 'ROTATE_45':
		return Pillow.rotate45(im)
	elif static_transform.type == 'ROTATE_135':
		return Pillow.rotate135(im)
	elif static_transform.type == 'ROTATE_225':
		return Pillow.rotate225(im)
	elif static_transform.type == 'ROTATE_315':
		return Pillow.rotate315(im)
	else:
		print('Unrecognized transform:', static_transform.type, 'Image unchanged')
		return im


class Transform:
	def __init__(self, start_image=None):
		self.static_transforms = []  # The transforms that have been applied - can be anything from STATIC_TRANSFORMS
		self.current_image = start_image  # The current image given the applied transforms listed in static_transoforms
		self.add_image = None  # Image of what was added
		self.add_percent = None  # Measure of how much was added
		self.subtract_image = None  # Image of what was subtracted
		self.subtract_percent = None  # Measure of how much was subtracted
		self.score = None  # Just a generic score used to ranking Transforms

	# Alters the Transform by the static_transform provided
	def addStaticTransform(self, static_transform):
		self.static_transforms.append(static_transform)
		self.current_image = applyStaticTransform(self.current_image, static_transform)
		return self

	# Sets the addition info needed to reach the image provided
	def setAdditions(self, im):
		self.add_image = Pillow.getAdditionsImage(self.current_image, im)
		self.add_percent = Pillow.percent(self.add_image)

	# Sets the subtraction info needed to reach the image provided
	def setSubtractions(self, im):
		self.subtract_image = Pillow.getSubtractionsImage(self.current_image, im)
		self.subtract_percent = Pillow.percent(self.subtract_image)

	# Applies all the current transformations in this Transform to the provided image
	# Returns the resultant image after all transformations
	def applyTo(self, im):
		# Apply static transformations, in order
		for stat_trans in self.static_transforms:
			im = applyStaticTransform(im, stat_trans)

		# Apply additions and subtractions
		if self.add_image is not None:
			im = Pillow.addTo(im, self.add_image)
		if self.subtract_image is not None:
			im = Pillow.subtractFrom(im, self.subtract_image)

		return im
