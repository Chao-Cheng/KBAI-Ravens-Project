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
import os, sys


class Agent:
	MATCHED_IMAGE_THRESHOLD = 98

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

		horizontal_transforms, vertical_transforms = None, None

		# Let's determine what horizontal and vertical transformations we have
		try:
			imA = self.loadImage(problem, 'A')
			imB = self.loadImage(problem, 'B')
			imC = self.loadImage(problem, 'C')
			imA, imB, imC = pillow.normalize(imA, imB, imC)

			horizontal_transforms = self.determineTransformations(imA, imB)
			vertical_transforms = self.determineTransformations(imA, imC)

		except IOError as e:
			print('IO issue - probably could not load image')
			print(e)
			return -1
		except:
			print('Unknown Error: Unable to determine transformations')
			return -1

		# Apply Transforms to get expected answer
		print('horizontal transforms:')
		print(' ', horizontal_transforms)
		print('vertical transforms')
		print(' ', vertical_transforms)

		expectedIm1 = self.applyTransformations(imC, horizontal_transforms)
		expectedIm2 = self.applyTransformations(imB, vertical_transforms)

		# Test solutions for accuracy, returning the best one if it fits well enough
		return self.findSolution(problem, [expectedIm1, expectedIm2])

	# Given two images, returns an array of the steps to take to transform im1 into im2
	def determineTransformations(self, im1, im2):
		match_score = pillow.getImageMatchScore(im1, im2)
		print('Match Score:', match_score)
		if match_score > self.MATCHED_IMAGE_THRESHOLD:
			print('  Images seem to match')
			return []
		else:
			raise Exception('Giving Up')

	# Apply the provided transformations to the im, returning the resulting image
	def applyTransformations(self, im, transforms):
		for transform in transforms:
			pass  # apply this particular transform

		return im

	# Given the problem and a list of expected solutions, tests the solutions against the
	# provided answers in the problem to find the best match
	def findSolution(self, problem, solutions):
		try:
			im1 = self.loadImage(problem, '1')
			im2 = self.loadImage(problem, '2')
			im3 = self.loadImage(problem, '3')
			im4 = self.loadImage(problem, '4')
			im5 = self.loadImage(problem, '5')
			im6 = self.loadImage(problem, '6')
			im1, im2, im3, im4, im5, im6 = pillow.normalize(im1, im2, im3, im4, im5, im6)

			answers = [im1, im2, im3, im4, im5, im6]
			answer_scores = []

			# Compare each answer to the solutions, giving each answer a score
			for a in range(len(answers)):
				answer = answers[a]
				total_answer_score = 0
				for s in range(len(solutions)):
					solution = solutions[s]
					total_answer_score += pillow.getImageMatchScore(answer, solution)

				answer_scores.append(total_answer_score / len(solutions))

			print('here are our answer scores:', answer_scores)
			correct_answer = answer_scores.index(max(answer_scores)) + 1
			print('we think the correct answer is', correct_answer)
			return correct_answer

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

	def loadImage(self, problem, key):
		filename = problem.figures[key].visualFilename
		return pillow.Image.open(os.path.join(self.here, filename))
