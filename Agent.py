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
#from PIL import Image
#import numpy

class Agent:
    # The default constructor for your Agent. Make sure to execute any
    # processing necessary before your Agent starts solving problems here.
    #
    # Do not add any variables to this signature; they will not be used by
    # main().
    def __init__(self):
        pass

    # The primary method for solving incoming Raven's Progressive Matrices.
    # For each problem, your Agent's Solve() method will be called. At the
    # conclusion of Solve(), your Agent should return an int representing its
    # answer to the question: 1, 2, 3, 4, 5, or 6. Strings of these ints 
    # are also the Names of the individual RavensFigures, obtained through
    # RavensFigure.getName(). Return a negative number to skip a problem.
    #
    # Make sure to return your answer *as an integer* at the end of Solve().
    # Returning your answer as a string may cause your program to crash.
    def Solve(self,problem):
        self.PrintProblemDetails(problem)

        # Determine transformations in existing relationships
        try:
            self.DetermineTransformations(problem)
        except:
            return -1

        return 1

    def PrintProblemDetails(self, problem):
        print('About to solve:', problem.name, '(' + problem.problemType + ')')

        for figure_key in sorted(problem.figures.keys()):
            self.PrintFigureObjects(problem.figures[figure_key])

    def PrintFigureObjects(self, figure):
        print()
        print('Figure', figure.name, 'objects:')
        for object_key in sorted(figure.objects.keys()):
            object = figure.objects[object_key]
            print(object_key)
            for attribute_key in object.attributes:
                attribute = object.attributes[attribute_key]
                print(' ', attribute_key + ':', attribute)

    #
    def DetermineTransformations(self, problem):
        try:
            abPairs = self.MatchObjects(problem.figures['A'], problem.figures['B'])
            acPairs = self.MatchObjects(problem.figures['A'], problem.figures['C'])
        except:
            raise Exception()



    # Takes in two figures and returns a list of pairs of objects (obj1, obj2) such that obj1 is in figure1 and obj2 is in figure2
    # Matches an object with null if it has no suitable match - deemed to be deleted or created
    def MatchObjects(self, figure1, figure2):
        print()
        print('Matching objects from', figure1.name, 'to', figure2.name)
        self.PrintFigureObjects(figure1)
        self.PrintFigureObjects(figure2)

        pairs = []

        # Let's just not try to match for now when we have differing numbers of objects
        if len(figure1.objects) != 1 or len(figure1.objects) != len(figure2.objects):
            print('ERROR: Unable to match objects in figures')
            raise Exception()
        else:
            # Now we know we have one object each
            pairs.append((next(iter(figure1.objects)), next(iter(figure2.objects))))

        return pairs
