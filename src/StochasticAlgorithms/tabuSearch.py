'''
Created on Jun 17, 2011
@author: Sai Panyam

Credits
Inspired by Clever Algorithms by Jason Brownlee
www.cleveralgorithms.com
'''
'''
Name
Tabu Search, TS, Taboo Search

Taxonomy
Tabu Search is a Metaheuristic and a Global Optimization algorithm.

Strategy
The strategy is to constrain an embedded heuristic from returning to recently visited areas of the search space (cycling).
It maintains a short term memory of recent moves and prevents future moves from undoing those changes. This strategy can be extended
by having intermediate term memory structures to bias moves towards promising areas (intensification), as well as long term memory
structures that promote diversity.

Heuristics
Tabu search was designed to manage an embedded hill climbing heuristic, although may be adapted to manage any neighborhood
exploration heuristic.

It has predominately been applied to discrete domains such as combinatorial optimization problems.

Candidates for neighboring moves can be generated deterministically for the entire neighborhood
or the neighborhood can be stochastically sampled to a fixed size, trading off efficiency for accuracy.

'''
from Helpers.Utilities import constructInitialSolution, tourCost, stochasticTwoOptWithEdges
# Function that returns a best candidate, sorting by cost
def locateBestCandidate(candidates):
    candidates.sort(key = lambda(c): c["candidate"]["cost"])
    best, edges = candidates[0]["candidate"], candidates[0]["edges"]
    return best, edges
def isTabu(perm, tabuList):
    result = False
    size = len(perm)
    for index, edge in enumerate(perm):
        if index == size-1:
            edge2 = perm[0]
        else:
            edge2 = perm[index+1]
        if [edge, edge2] in tabuList:
            result = True
            break
    return result
def generateCandidates(best, tabuList, points):
    permutation, edges, result = None, None, {}
    while permutation == None or isTabu(best["permutation"], tabuList):
        permutation, edges = stochasticTwoOptWithEdges(best["permutation"])
    candidate ={}
    candidate["permutation"] = permutation
    candidate["cost"] = tourCost(candidate["permutation"])
    result["candidate"] = candidate
    result["edges"] = edges
    return result
def tabuSearch(points, maxIterations, maxTabu, maxCandidates):
    # construct a random tour
    best ={}
    best["permutation"] = constructInitialSolution(points)
    best["cost"] = tourCost(best["permutation"])
    tabuList =[]
    while maxIterations>0:
        # Generate candidates using stocahstic 2-opt near current best candidate
        # Use Tabu list to not revisit previous rewired edges
        candidates = []
        for index in range(0,maxCandidates):
            candidates.append(generateCandidates(best, tabuList, points))
        # Locate the best candidate
        # sort the list of candidates by cost
        # since it is an  involved sort, we write a function for getting the least cost candidate
        bestCandidate, bestCandidateEdges = locateBestCandidate(candidates)
        # compare with current best and update if necessary
        if bestCandidate["cost"] < best["cost"]:
            # set current to the best, so thatwe can continue iteration
            best = bestCandidate
            # update tabu list
            for edge in bestCandidateEdges:
                if len(tabuList) < maxTabu:
                    tabuList.append(edge)
        maxIterations -=1
    return best
