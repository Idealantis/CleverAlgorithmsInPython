'''
Created on July 11, 2017
@author: Sai Panyam

Credits
Inspired by Clever Algorithms by Jason Brownlee
www.cleveralgorithms.com
'''
'''
Name
Stochastic Hill Climbing, SHC, Random Hill Climbing, RHC, Random Mutation Hill Climbing, RMHC.

Taxonomy
The Stochastic Hill Climbing algorithm is a Stochastic Optimization algorithm and is a Local Optimization algorithm
contrasted to Global Optimization algorithms.
It is an extension of deterministic hill climbing algorithms such as Simple Hill Climbing (first-best neighbor),
Steepest-Ascent Hill Climbing (best neighbor), and a parent of approaches such as Parallel Hill Climbing and
Random-Restart Hill Climbing.

Strategy
The strategy of the Stochastic Hill Climbing algorithm is to iterate the process of randomly selecting a neighbor of
a candidate solution and only accept it if it results in an improvement. The strategy addresses the limitations
of deterministic hill climbing techniques that were likely to get stuck in local optima.

Heuristics
SHC is more valuable when applied to discrete domains where there are 'neighbors' as opposed to continuous functions. In order to
apply SHC to continuous functions, we need to define a step size to identify neighbors. Generally SHC is used to refine a candidate solution
got from other search techniques specifically global optimizations. We can also use this on multiple candidate solutions as a starting point.
'''
import random
def randomSolution(size):
    bitString = []
    while size > 0:
        if random.random() < 0.5:
            bitString.append('1')
        else:
            bitString.append('0')
        size -= 1
    return bitString
def oneMax(vector):
    return vector.count('1')
def randomNeighbhor(vector):
    mutant = vector# make a copy of the vector to a mutant
    pos = random.randrange(0, len(vector)) # gets a random position 0<= pos < length of the original list
    if mutant[pos] == '0':
        mutant[pos] = '1'
    return mutant
def stochasticHillClimbing(problemSize, maxIterations):
    candidate = {}
    candidate['vector'] = randomSolution(problemSize)
    initialCost = candidate['cost'] = oneMax(candidate['vector'])
    # initial cost is used for calculating search efficiency later. This doesn't take part in the algorithm
    iterCount = 0
    while iterCount < maxIterations:
        mutant = {}
        mutant['vector'] = randomNeighbhor(candidate["vector"])
        mutant['cost'] = oneMax(mutant['vector'])
        if  mutant['cost'] >= candidate['cost']: # Note here we are looking for optimizing the maximum!
            candidate = mutant
        if candidate['cost'] == problemSize:
            break
        iterCount += 1
    candidate['initialCost']= initialCost
    candidate['iteration'] = iterCount
    return candidate
