'''
Created on July 9, 2017
@author: Sai Panyam

Credits
Inspired by Clever Algorithms by Jason Brownlee
www.cleveralgorithms.com
'''
'''
Name
Adaptive Random Search, ARS, Adaptive Step Size Random Search ASSRS, Variable Step Size Random Search

Taxonomy
Adaptive Random Search belongs to Stochastic Optimization and Global Optimization.
It is an extension of Random Search and Localized Random Search Algorithms

Strategy
The strategy is to trial a larger step in each iteration and adopt the larger step if it results in an improved result.
The strategy of preferring large moves is intended to allow the technique to escape local optima. Smaller  step sizes are adopted
if no improvements is made for an extended period.
'''
from Helpers.Utilities import basinFunction, randomSolution, takeStep

# Function to initialize step size
def getInitialStepSize(bounds, initFactor):
    return (bounds[1] - bounds[0]) * initFactor

# Function to generate the large step size
def getLargeStepSize(iteration,stepSize, largeFactor, smallFactor, iterationFactor):
    if iteration > 0 or iteration % iterationFactor==0:
        return stepSize * largeFactor
    else:
        return stepSize * smallFactor

# Search algorithm that implements the Adaptive Random Search strategy
def adaptiveRandomsearch(maxIterations, problemSize, searchSpace, initStepSizeFactor, smallStepSizeFactor, largeStepSizeFactor, iterationStepSizeFactor, maxNoChange):
    # Initialize the no change counter
    noChangeCount =0
    # Initialize the step size
    currentStepSize = getInitialStepSize(searchSpace, initStepSizeFactor)
    current ={}
    current["vector"] = randomSolution(searchSpace, problemSize)
    current["cost"] = basinFunction(current["vector"])
    for index in range(0,maxIterations):
        # Get cost from currentCandidate step size
        step ={}
        step["vector"] = takeStep(searchSpace, current["vector"], currentStepSize)
        step["cost"] = basinFunction(step["vector"])

        # Get large step size
        largeStepSize = getLargeStepSize(index, currentStepSize, largeStepSizeFactor, smallStepSizeFactor, iterationStepSizeFactor)
        # Get cost from currentCandidate large step size
        largeStep ={}
        largeStep["vector"] = takeStep(searchSpace, current["vector"], largeStepSize)
        largeStep["cost"] = basinFunction(largeStep["vector"])

        # Compare costs
        # Identify no change
        if step["cost"]<current["cost"] or largeStep["cost"]<current["cost"]:
            # if either of the new costs are 'better' then we proceed in that direction
            if largeStep["cost"]<step["cost"]:
                currentStepSize = largeStepSize
                current = largeStep
            else:
                current = step
        else:# if not then we did not improve the result and are plateauing so to speak
            noChangeCount +=1
            if noChangeCount > maxNoChange:
                noChangeCount =0
                # adjust step size so that we take smaller steps
                currentStepSize = currentStepSize/smallStepSizeFactor
    return current
