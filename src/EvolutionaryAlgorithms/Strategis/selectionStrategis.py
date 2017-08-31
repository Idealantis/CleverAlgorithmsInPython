import random
import numpy as np
def getRangeBasedFitnesses(population, popSize):
    tempList = range(popSize)
    random.shuffle(tempList)
    A = [None]*(popSize*2)
    temp = 0
    j = 0
    for randomIndex in range(0,len(tempList)):
        A[j] = temp+1
        A[j+1] = A[j]+population[randomIndex]['fitness']-1
        temp = A[j+1]
        j += 2
        continue
    return A
def findAbsoulteIndex(A, value):
    A = np.array(A)
    index = (np.abs(A-value)).argmin()
    return index
def sumOfPopulationFit(population, popSize):
    sumFitness = 0
    for i in range(popSize):
        sumFitness += population[i]['fitness']
    return sumFitness
# Roulette Wheel
def rouletteWheelSelection(population, popSize):
    A = getRangeBasedFitnesses(population, popSize)
    sumFitness = sumOfPopulationFit(population, popSize)
    randomNumOnWheel = random.randint(1, sumFitness)
    parentIndex = findAbsoulteIndex(A, randomNumOnWheel)
    return population[parentIndex/2]
# Stochastic Universal Sampling(SUS)
def stochasticUniversalSampling(population, popSize):
    A = getRangeBasedFitnesses(population, popSize)
    sumFitness = sumOfPopulationFit(population,popSize)
    tempPopulation = [None]*popSize
    for i in range(popSize):
        tempPopulation[i] = population[findAbsoulteIndex(A, random.randint(1, sumFitness))/2]
    return tempPopulation
# Rank Selection
def rankSelection(rankPopulation, popSize):
    i = random.randint(0,popSize/2)
    j = random.randint(0,popSize/2)
    while i != j:
        j = random.randint(0,popSize)
    return rankPopulation[i] if rankPopulation[i]['fitness'] > rankPopulation[j]['fitness'] else rankPopulation[j]
# binary tournament
def binaryTournament(population, popSize):
    i, j = random.randrange(popSize), random.randrange(popSize)
    while j==i:
        j = random.randrange(popSize)
    return population[i] if population[i]["fitness"]>population[j]["fitness"] else population[j]
