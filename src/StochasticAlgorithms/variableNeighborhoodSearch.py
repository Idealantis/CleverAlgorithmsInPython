'''
Created on July 15, 2017
@author: Sai Panyam

Credits
Inspired by Clever Algorithms by Jason Brownlee
www.cleveralgorithms.com
'''
'''
Name
Variable Neighborhood Search, VNS

Taxonomy
Variable Neighborhood Search is a Metaheuristic and a Global Optimization technique that manages a local search technique.

Strategy
The strategy for the Variable Neighborhood Search involves iterative exploration of larger and larger neighborhoods for a
given local optima until an improvement is located after which time the search across expanding neighborhoods is repeated.
The strategy is motivated by three principles:
1) a local minimum for one neighborhood structure may not be a local minimum for a different neighborhood structure,
2) a global minimum is a local minimum for all possible neighborhood structures, and
3) local minima are relatively close to global minima for many problem classes

Heuristics
Approximation methods (such as stochastic hill climbing) are suggested for use as the
Local Search procedure for large problem instances in order to reduce the running time.

Variable Neighborhood Search has been applied to a very wide array of combinatorial optimization problems
as well as clustering and continuous function optimization problems.

The embedded Local Search technique should be specialized to the problem type and instance to which the
technique is being applied.

The Variable Neighborhood Descent (VND) can be embedded in the Variable Neighborhood Search
as a the Local Search procedure and has been shown to be most effective.
'''
from Helpers.Utilities import stochasticTwoOpt, tourCost, constructInitialSolution
def localSearch(best, maxIter, neighborhood):
    count =0
    while count<maxIter:
        candidate ={}
        candidate["permutation"]=best["permutation"]
        for index in range(0,neighborhood):#Involves running stochastic two opt for neighbor times
                # Get candidate solution from neighborhood
                candidate["permutation"] = stochasticTwoOpt(candidate["permutation"])

        candidate["cost"] = tourCost(candidate["permutation"])
        if candidate["cost"] < best["cost"]:# We also restart the search when we find the local optima
            best,count = candidate, 0
        else:
            count +=1
    return best
def variableNeighborhoodSearch(points,neighborhoods, maxNoImprove, maxNoImproveLocalSearch):
    # First construct the initial solution. We use a random permutation as the initial solution
    best ={}
    best["permutation"] = constructInitialSolution(points)
    best["cost"] = tourCost(best["permutation"])
    noImproveCount =0
    while noImproveCount<=maxNoImprove:
        candidate ={}
        candidate["permutation"] = best["permutation"]
        # for each neighborhood in neighborhoods
        for neighborhood in neighborhoods:
            #Calculate Neighborhood : Involves running stochastic two opt for neighbor times
            for index in range(0,neighborhood):
                # Get candidate solution from neighborhood
                candidate["permutation"] = stochasticTwoOpt(candidate["permutation"])

            # Calculate the cost of the final neighborhood
            candidate["cost"] = tourCost(candidate["permutation"])
            # Refine candidate solution using local search and neighborhood
            candidate = localSearch(candidate,maxNoImproveLocalSearch, neighborhood)
            #if the cost of the candidate is lesser than cost of current best then replace
            #best with current candidate
            if candidate["cost"] < best["cost"]:
                best, noImproveCount = candidate, 0 # We also restart the search when we find the local optima
                # break: this breaks out of the neighborhoods iteration
                break
            else: # increment the count as we did not find a local optima
                noImproveCount +=1
    return best


