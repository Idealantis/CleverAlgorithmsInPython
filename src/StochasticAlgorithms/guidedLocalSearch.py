'''
Created on July 13, 2017
@author: Sai Panyam

Credits
Inspired by Clever Algorithms by Jason Brownlee
www.cleveralgorithms.com
'''
'''
Name
Guided Local Search, GLS

Taxonomy
Guided Local Search is a Metaheuristics and a Global Optimization algorithm. It is an extension of Local
Search algorithms such as Hill climbing and is similar to Tabu Search and Iterated Local Search.

Strategy
The strategy is to use penalties to encourage a Local Search technique escape local optima and get to
the global optima. The local search is repeated a number of times using the last local optima discovered
and the augmented cost function that guides exploration away from solutions with features present in discovered
local optima.

Heuristics
The Guided Local Search procedure is independent of the Local Search procedure embedded within it.

The Guided Local Search procedure may need to be executed for thousands to hundreds-of-thousands of iterations,
each iteration of which assumes a run of a Local Search algorithm to convergence.

The lambda parameter is a scaling factor for feature penalization that must be in the same proportion to the candidate solution
costs from the specific problem instance to which the algorithm is being applied. As such, the value
for lambda must be meaningful when used within the augmented cost function (such as when it is added to a candidate
solution cost in minimization and subtracted from a cost in the case of a maximization problem).
'''
from Helpers.Utilities import constructInitialSolution, euclideanDistance, stochasticTwoOpt
def augmentedCost(perm, penalties, scalingFactor):
    distance, augmented = 0,0
    size = len(perm)
    for index in range(0,size):
        index1 = index
        if index == size-1:
            index2 = 0
        else:
            index2 = index +1

        if index2<index1:
            index1,index2 = index2, index1
        v1 = perm[index1]
        v2 = perm[index2]
        d = euclideanDistance(v1, v2)
        distance +=d
        augmented +=d + (scalingFactor * penalties[index1][index2])
    return distance, augmented
def cost(candidate, penalties,scalingFactor):
    cost, augCost = augmentedCost(candidate['permutation'], penalties, scalingFactor)
    candidate['cost'], candidate['augmentedCost'] = cost, augCost
def calculateFeatureUtilities(perm, penalties):
    size = len(perm)
    utilities = [0] * size
    for index in range(0,size):
        index1 = index
        if index == size-1:
            index2 = 0
        else:
            index2 = index +1

        if index2<index1:
            index1,index2 = index2, index1
        v1 = perm[index1]
        v2 = perm[index2]
        utilities[index] = euclideanDistance(v1, v2)/(1 + penalties[index1][index2])
    return utilities
def updateFeaturePenalties(perm, penalties, utilities):
    size = len(perm)
    maxUtil = max(utilities)
    for index in range(0,size):
        index1 = index
        if index == size-1:
            index2 = 0
        else:
            index2 = index +1

        if index2<index1:
            index1,index2 = index2, index1
        # Update penalties
        if utilities[index] == maxUtil:
            penalties[index1][index2] +=1
    return penalties
def localSearch(current, scalingFactor, penalties, maxNoImprove):
    cost(current, penalties, scalingFactor)
    count =0
    while count < maxNoImprove:
        candidate = {}
        candidate['permutation'] = stochasticTwoOpt(current['permutation'])
        cost(candidate,penalties,scalingFactor)
        # Now we encourage diversification by aiming for a 'larger' augmented cost to escape local minima
        if candidate['augmentedCost'] < current['augmentedCost']:
            # reset the counter to restart the search
            count =0
            current = candidate
        else:
            count +=1

    return current
def guidedLocalSearch(points, maxIterations, maxNoImprove, scalingFactor):
    # Create a random solution
    current ={}
    current['permutation'] = constructInitialSolution(points)
    best = None
    # Initialize penalties. We create a list of lists. Each element of penalties is a list of penalties for each point
    penalties = [[0] * len(points)] * len(points)
    while maxIterations > 0:
        # Execute the local search taking into account lambda and penalties
        current = localSearch(current, scalingFactor, penalties, maxNoImprove)
        # Calculate feature utilities
        utilities = calculateFeatureUtilities(current['permutation'], penalties)
        # Update feature penalties
        penalties = updateFeaturePenalties(current['permutation'], penalties, utilities)
        # Compare current candidate cost with best and update if less
        if best==None or current['cost'] < best['cost']:
            best = current
        maxIterations -=1
    return best
