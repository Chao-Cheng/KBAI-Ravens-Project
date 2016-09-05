# Your Agent for solving Raven's Progressive Matrices. You MUST modify this file.
#
# You may also create and submit new files in addition to modifying this file.
#
# Make sure your file retains methods with the signatures:
# def __init__(self)
# def Solve(self,problem)
#
# These methods will be necessary for the project's main method to run.

# Install Pillow and uncomment this line to access image processing.
# import numpy

import MyPillow as pillow
import Transform as trans
import os, sys


class Agent:
	# The default constructor for your Agent. Make sure to execute any
	# processing necessary before your Agent starts solving problems here.
	#
	# Do not add any variables to this signature; they will not be used by
	# main().
	def __init__(self):
		self.here = sys.path[0]

	# The primary method for solving incoming Raven's Progressive Matrices.
	# For each problem, your Agent's Solve() method will be called. At the
	# conclusion of Solve(), your Agent should return an int representing its
	# answer to the question: 1, 2, 3, 4, 5, or 6. Strings of these ints
	# are also the Names of the individual RavensFigures, obtained through
	# RavensFigure.getName(). Return a negative number to skip a problem.
	#
	# Make sure to return your answer *as an integer* at the end of Solve().
	# Returning your answer as a string may cause your program to crash.
	def Solve(self, problem):
		self.printProblemDetails(problem)

		h_transforms, v_transforms = None, None

		# Let's determine what horizontal and vertical transformations we have
		try:
			imA = self.loadImage(problem, 'A')
			imB = self.loadImage(problem, 'B')
			imC = self.loadImage(problem, 'C')
			imA, imB, imC = pillow.normalize(imA, imB, imC)

			h_transforms = self.getPriorityTransforms(imA, imB)
			v_transforms = self.getPriorityTransforms(imA, imC)

		except IOError as e:
			print('IO issue - probably could not load image')
			print(e)
			return -1
		except:
			print('Unknown Error: Unable to determine transformations')
			return -1

		# Choose between horizontal and vertical transforms
		# Will choose the list that has the best match before additions and subtractions
		transforms = None
		transform_direction = None
		image_to_transform = None
		if h_transforms[0].score > v_transforms[0].score:
			print('Choosing horizontal transforms')
			transforms = h_transforms
			transform_direction = 'H'
			image_to_transform = imC
		else:
			print('Choosing vertical transforms')
			transforms = v_transforms
			transform_direction = 'V'
			image_to_transform = imB

		# Apply Transforms to get expected answers
		solutions = [transform.applyTo(image_to_transform) for transform in transforms]

		if problem.name.endswith('05'): self.printSolutionInfo(image_to_transform, transforms, solutions)

		# Test solutions for accuracy, returning the best one if it fits well enough
		return self.findSolution(problem, solutions)

	# Given two images, returns a list of Transforms that will turn im1 into im2
	# List is ordered by how well the images matched before additions and subtractions were considered: best match first
	def getPriorityTransforms(self, im1, im2):
		priority_transforms = [trans.Transform(im1)]  # Start the list with a blank transform

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

		return priority_transforms

	# Given the problem and a list of expected solutions, tests the solutions against the
	# 	provided answers in the problem to find the best match
	# Returns the number representing the chosen answer, the return for the Agent's Solve method
	def findSolution(self, problem, solution_images):
		try:
			# Load answer images
			im1 = self.loadImage(problem, '1')
			im2 = self.loadImage(problem, '2')
			im3 = self.loadImage(problem, '3')
			im4 = self.loadImage(problem, '4')
			im5 = self.loadImage(problem, '5')
			im6 = self.loadImage(problem, '6')
			answers = pillow.normalize(im1, im2, im3, im4, im5, im6)

			# Get the best match from the answers for each solution image
			solutions = []
			for solution_image in solution_images:
				chosen_answer = 0
				percent_match = 0
				for i in range(len(answers)):
					answer = answers[i]

					match_score = pillow.getImageMatchScore(solution_image, answer)
					if match_score > percent_match:
						percent_match = match_score
						chosen_answer = i+1

				solutions.append(Solution(chosen_answer, percent_match))

			# Pick the best solution (with the highest answer match percentage)
			solutions.sort(key=lambda s: s.percent_match, reverse=True)
			chosen_solution = solutions[0]

			print('max score:', chosen_solution.percent_match)
			print('we think the correct answer is', chosen_solution.answer)

			if chosen_solution.percent_match < pillow.MATCHED_IMAGE_THRESHOLD:
				print('No decent match. Giving up.')
				return -1

			return chosen_solution.answer

		except IOError as e:
			print('IO issue - probably could not load image')
			print(e)
			return -1
		except Exception as e:
			print('Error: Unable to find solution')
			print(e)
			return -1

	def printProblemDetails(self, problem):
		print()
		print('About to solve:', problem.name, '(' + problem.problemType + ')')

	# Returns the image with the same name as the given key from the provided problem
	def loadImage(self, problem, key):
		filename = problem.figures[key].visualFilename
		return pillow.Image.open(os.path.join(self.here, filename))

	def printSolutionInfo(self, start_image, transforms, solutions):
		start_image.save(os.path.join(self.here, 'testAgent', 'startImage.png'))

		print('  Printing Solution Info:')
		for i in range(len(transforms)):
			transform = transforms[i]
			solution = solutions[i]
			print('   ', transform.static_transforms)
			print('    Added:', transform.add_percent)
			print('    Subtracted:', transform.subtract_percent)
			print()
			solution.save(os.path.join(self.here, 'testAgent', 'solution{0!s}.png'.format(i+1)))


class Solution:

	def __init__(self, answer, percent_match):
		self.answer = answer
		self.percent_match = percent_match
