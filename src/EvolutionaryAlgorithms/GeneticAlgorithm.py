import random
from Strategis.crossoverStrategis import onePointCrossOver,multiPointCrossOver,uniformCrossOver
from Strategis.mutationStrategis import bitFlip,inversionMutation,swapMutaion,scrambleMutation,pointMutation
from Strategis.selectionStrategis import binaryTournament,rouletteWheelSelection,stochasticUniversalSampling,rankSelection
def oneMax(temp):
    return temp.count('1')
def getPopulation(numOfBits, popSize):
    population = [{"bitstring":None,"fitness":None}]*popSize
    for i in range(popSize):
        temp = ''.join( '1' if random.random() < 0.5 else '0' for i in range(numOfBits))
        population[i] = {"bitstring":temp,"fitness":oneMax(temp)}
    return population
def reproduce(strategis, numOfBits, selected, popSize, popCrossOver, popMutation):
    children = [None]*popSize
    child = {}
    for index, parent1 in enumerate(selected):
        parent2 = selected[index-1] if index%2 else selected[index+1]
        if index == len(selected)-1:
            parent2 = selected[0]
        child = {}
        child["bitstring"] = eval(strategis[1])(parent1["bitstring"], parent2["bitstring"], popCrossOver)
        # if strategis[2] == 'bitFlip' or strategis[2] == 'swapMutaion' :
        #     child["bitstring"] = eval(strategis[2])(child["bitstring"], numOfBits ,popMutation)
        # else:
        child["bitstring"] = eval(strategis[2])(child["bitstring"], numOfBits ,popMutation)
        child["fitness"] = oneMax(child["bitstring"])
        children[index] = child
    return children
def geneticAlgorithm(strategis, maxNoGenes, numOfBits, popSize, popCrossOver, popMutation):
    population = getPopulation(numOfBits, popSize)
    best = sorted(population, key = lambda x: x['fitness'], reverse=True)[0]
    selectedSUS = [eval(strategis[0])(population, popSize) for j in range(popSize)]
    for i in range(maxNoGenes):
        children = 0
        if strategis[0] == 'stochasticUniversalSampling':
            children = reproduce(strategis,numOfBits,selectedSUS[i], popSize, popCrossOver, popMutation)
        else:
            selected = [eval(strategis[0])(population, popSize) for j in range(popSize)]
            children = reproduce(strategis, numOfBits, selected, popSize, popCrossOver, popMutation)
        bestFromChildren = sorted(children, key = lambda x: x['fitness'], reverse=True)[0]
        if bestFromChildren["fitness"] >= best['fitness']:
            best  = bestFromChildren
        if best["fitness"] == numOfBits:
            break
    return best
