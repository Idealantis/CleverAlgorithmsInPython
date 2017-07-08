'''
Created on Jul 8, 2017
@author: Sai Panyam

Credits
Inspired by Clever Algorithms by Jason Brownlee
www.cleveralgorithms.com
'''
'''
Name
Random Search, RS, Blind Random Search, Pure RandomSearch, PRS

Taxonomy
Random Search belongs to Stochastic Optimization and Global Optimization.

Strategy
The strategy is to sample solutions from across the entire search space using a uniform probability distribution.
'''
# import the helper functions
from Helpers.Utilities import randomSolution,basinFunction
# Search algorithm that implements the Random Search strategy
def randomSearch(searchSpace,maxIter,problemSize):
    best = None
    while maxIter > 0:
        maxIter -= 1
        candidate = {} # Dictionary is preferred, because we can store the vector and the associated cost as one element
        candidate['vector'] = randomSolution(searchSpace,problemSize)
        candidate['cost'] = basinFunction(candidate['vector'])
        # if the cost is a better value then replace the best with this value
        if best == None or candidate['cost'] < best['cost']:
            best = candidate
        # print(' > iteration = ' + str(iter+1) + ', best = '+str(best["cost"]))
    return best