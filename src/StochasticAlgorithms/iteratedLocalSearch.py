'''
Created on July 12, 2011
@author: Sai Panyam

Credits
Inspired by Clever Algorithms by Jason Brownlee
www.cleveralgorithms.com
'''
'''
Name
Iterated Local Search, ILS

Taxonomy
Iterated Local Search is a Metaheuristic and a Global Optimization technique. It is predominantly applied to discrete domains such as
combinatorial optimization problems.

Strategy
The strategy employed by ILS is to sample a broader neighborhood of candidate solutions and use a local search technique to
refine solutions to their local optima. ILS explores a sequence of solutions created as perturbations of the current best solution,
the result of which is refined using an embedded heuristic

Heuristics
The perturbation of the current best solution should be in a neighborhood beyond the reach of the embedded heuristic
and should not be easily undone.

Perturbations that are too small make the algorithm too greedy, perturbations that are too large make
the algorithm too stochastic.

The embedded heuristic is most commonly a problem-specific local search technique.

The starting point for the search may be a randomly constructed candidate solution, or
constructed using a problem-specific heuristic (such as nearest neighbor).

Perturbations can be made deterministically, although stochastic and probabilistic (adaptive based on history)
are the most common.

The procedure may store as much or as little history as needed to be used during perturbation and acceptance criteria.

No history represents a random walk in a larger neighborhood of the best solution and is the most common implementation of the approach.
'''
import random
from Helpers.Utilities import stochasticTwoOpt, tourCost, constructInitialSolution
def perturbation(best, searchHistory):
    # uses a 'double bridge move' for perturbation
    # We can extend perturbation by incorporating search history if need be.
    candidate = {}
    candidate["permutation"] = doubleBridgeMove(best["permutation"])
    candidate["cost"] = tourCost(candidate["permutation"])
    return candidate
#The double-bridge move involves partitioning a permutation into 4 pieces
#(a,b,c,d) and putting it back together in a specific and jumbled ordering
#(a,d,c,b) - This equivalent to a 4-opt move
def doubleBridgeMove(perm):
    # make four slices
    sliceLength = len(perm)/4
    p1 = 1 + random.randrange(0,sliceLength)
    p2 = p1 + 1 + random.randrange(0,sliceLength)
    p3 = p2 + 1 + random.randrange(0,sliceLength)
    # Combine first and fourth slice in order
    # Combine third and second slice in order
    # return the combination of the above two combined slices
    return perm[0:p1] + perm[p3:] + perm[p2:p3] + perm[p1:p2]
def localSearch(best, maxIter):
    while maxIter>0:
        candidate ={}
        candidate["permutation"] = stochasticTwoOpt(best["permutation"])
        candidate["cost"] = tourCost(candidate["permutation"])
        if candidate["cost"] < best["cost"]:
            best = candidate
        maxIter -=1

    return best

def acceptanceCriterion(best, candidate, searchHistory):
    # Here we can incorporate search history if need be
    if candidate["cost"] < best["cost"]:
            best = candidate
    return best
def iteratedLocalSearch(points, maxIterations, maxNoImprove, maxSearchHistory):
    # First construct the initial solution. We use a random permutation as the initial solution
    best ={}
    best["permutation"] = constructInitialSolution(points)
    best["cost"] = tourCost(best["permutation"])
    # now refine this using a local search for getting to the local optima
    best = localSearch(best, maxNoImprove)
    # One can incorporate search history for either diversification or intensification
    # here though i include search history, it is not used in the algorithm directly
    searchHistory =[]
    if len(searchHistory) < maxSearchHistory:
        searchHistory.append(best)
    # Iterate
    while maxIterations > 0:
        candidate = perturbation(best,searchHistory)
        candidate = localSearch(candidate, maxNoImprove)
        best = acceptanceCriterion(best,candidate, searchHistory)
        maxIterations -=1
    return best
