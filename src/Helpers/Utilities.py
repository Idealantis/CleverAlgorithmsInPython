import random
# Randomizing function that selects random  inputs for the objective function
def getRandomWithinBounds(min, max):
    return min + (max - min) * random.random()
def randomSolution(minMax,problemSize):
    inputValues =[]
    # generates a value between the minimum and maximum values of the search space
    while problemSize>0:
        # generates a value between the minimum and maximum values of the search space
        inputValues.append(getRandomWithinBounds(minMax[0], minMax[1]))
        problemSize -=1
    return inputValues
# Objective function that evaluates the cost
def basinFunction(vector):
    # original basin function from Clever Algorithms book
    #return sum([pow(item,2) for item in vector])
    a,h,k = 0.5,2,-5
    return sum([a * pow((item-h),2) + k for item in vector])