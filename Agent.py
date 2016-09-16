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

import MyPillow as Pillow
import Transform as Trans
import os
import sys
import time


class Agent:

	submitting = False

	# The default constructor for your Agent. Make sure to execute any
	# processing necessary before your Agent starts solving problems here.
	#
	# Do not add any variables to this signature; they will not be used by
	# main().
	def __init__(self):
		self.here = sys.path[0]
		self.time = time.clock()
		self.max_transform_attempt_order = max([stat_trans.order for stat_trans in Trans.STATIC_TRANSFORMS])

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
		self.time = time.time()
		self.printProblemDetails(problem)

		try:  # Load our images
			imA = self.loadImage(problem, 'A')
			imB = self.loadImage(problem, 'B')
			imC = self.loadImage(problem, 'C')
			imA, imB, imC = Pillow.normalize(imA, imB, imC)
		except IOError as e:
			print('IO issue - probably could not load image')
			print(e)
			return -1
		except:
			print('Unknown Error: Unable to determine transformations')
			return -1

		h_transforms, v_transforms = None, None

		transform_attempt_order = 0
		answer_guess = -1
		while answer_guess == -1 and transform_attempt_order <= self.max_transform_attempt_order:
			# Let's determine what horizontal and vertical transformations we have - iteratively
			h_transforms = self.getPriorityTransforms(imA, imB, h_transforms, transform_attempt_order)
			v_transforms = self.getPriorityTransforms(imA, imC, v_transforms, transform_attempt_order)
			transform_attempt_order += 1

			# Choose between horizontal and vertical transforms
			# Will choose the list that has the best match before additions and subtractions
			print()
			if h_transforms[0].score > v_transforms[0].score:
				print('Choosing horizontal transforms')
				transforms = h_transforms
				image_to_transform = imC
			else:
				print('Choosing vertical transforms')
				transforms = v_transforms
				image_to_transform = imB

			# Apply Transforms to get expected solutions
			solutions = [transform.applyTo(image_to_transform) for transform in transforms]

			# Test solutions for accuracy, returning the best one if it fits well enough
			answer_guess = self.findSolution(problem, solutions)

		if problem.name.endswith('08') and not self.submitting: self.printSolutionInfo(image_to_transform, transforms, solutions)

		self.printElapsedTime()
		return answer_guess

	# Given two images, returns a list of Transforms that will turn im1 into im2
	# List is ordered by how well the images matched before additions and subtractions were considered: best match first
	def getPriorityTransforms(self, im1, im2, transforms=[], order=0):
		priority_transforms = [] if transforms is None else transforms

		if len(priority_transforms) == 0:
			priority_transforms = [Trans.Transform(im1)]  # Start the list with a blank transform

		# For each static transform, add a Transform to the list
		# Only add transforms of the current order - iterative solution
		for stat_trans in filter(lambda t: t.order == order, Trans.STATIC_TRANSFORMS):
			priority_transforms.append(Trans.Transform(im1).addStaticTransform(stat_trans))

		# Score each transform for ordering
		for transform in filter(lambda t: t.score is None, priority_transforms):
			transform.score = Pillow.getImageMatchScore(transform.current_image, im2)
		# Order our list by how well each one matches im2
		priority_transforms.sort(key=lambda t: t.score, reverse=True)

		# Put in the add and subtract images
		for transform in filter(lambda t: t.add_image is None or t.subtract_image is None, priority_transforms):
			if not Pillow.imagesMatch(transform.current_image, im2):
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
			answers = Pillow.normalize(im1, im2, im3, im4, im5, im6)

			# Get the best match from the answers for each solution image
			solutions = []
			for solution_image in solution_images:
				chosen_answer = 0
				percent_match = 0
				for i in range(len(answers)):
					answer = answers[i]

					match_score = Pillow.getImageMatchScore(solution_image, answer, fuzzy=True)
					if match_score > percent_match:
						percent_match = match_score
						chosen_answer = i+1

				solutions.append(Solution(chosen_answer, percent_match))

			# print('Solution Scores:', [str(s) for s in solutions])

			# Pick the best solution (with the highest answer match percentage)
			solutions.sort(key=lambda s: s.percent_match, reverse=True)
			chosen_solution = solutions[0]

			print('Chosen Solution is ', chosen_solution)

			if chosen_solution.percent_match < Pillow.MATCHED_IMAGE_THRESHOLD:
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
		print('==================================================')
		print('About to solve:', problem.name, '(' + problem.problemType + ')')
		print('==================================================')

	def printElapsedTime(self):
		elapsed = time.time() - self.time
		print()
		print('Solution took', int(elapsed*1000), 'milliseconds')
		self.time = time.time()

	# Returns the image with the same name as the given key from the provided problem
	def loadImage(self, problem, key):
		filename = problem.figures[key].visualFilename
		return Pillow.Image.open(os.path.join(self.here, filename))

	def printSolutionInfo(self, start_image, transforms, solution_images):
		start_image.save(os.path.join(self.here, 'testAgent', 'startImage.png'))

		print('  Printing Solution Info:')
		for i in range(len(transforms)):
			transform = transforms[i]
			solution = solution_images[i]
			print('   ', [t.type for t in transform.static_transforms])
			print('    Score:', transform.score)
			print('    Added:', transform.add_percent)
			print('    Subtracted:', transform.subtract_percent)
			print()
			solution.save(os.path.join(self.here, 'testAgent', 'solution{0!s}.png'.format(i+1)))


class Solution:

	def __init__(self, answer, percent_match):
		self.answer = answer
		self.percent_match = percent_match

	def __str__(self):
		return '{0!s}: {1!s}%'.format(self.answer, self.percent_match)
