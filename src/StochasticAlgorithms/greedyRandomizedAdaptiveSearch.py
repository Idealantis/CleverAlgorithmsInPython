'''
Created on July 15, 2017
@author: Sai Panyam

Credits
Inspired by Clever Algorithms by Jason Brownlee
www.cleveralgorithms.com
'''
'''
Name
Greedy Randomized Adaptive Search, GRASP

Taxonomy
Greedy Randomized Adaptive Search is a Metaheuristic and a Global Optimization algorithm.

Strategy
The strategy is to iteratively sample stochastically greedy solutions and then use a local search heuristic to refine them
to a local optima. It builds a Restricted Candidate List (RCL) that constrains the features of a solution that may be selected from each
cycle.

Heuristics
The RCL may be constrained by an explicit size, or by using a threshold [0, 1] on the cost of adding each feature
to the current candidate solution.

The threshold defines the amount of greediness of the construction mechanism, where values close to 0 may be too greedy, and values
close to 1 may be too generalized.

As an alternative to using a threshold, the RCL can be constrained to the top n% of candidate features that may be
selected from each construction cycle.

'''
from Helpers.Utilities import stochasticTwoOpt, tourCost,euclideanDistance
import random
def constructGreedySolution(perm, alpha):
    candidate={}
    # Select one point randomly
    problemSize = len(perm)
    candidate["permutation"] = [perm[random.randrange(0,problemSize)]]
    # While candidate's size is not equal to the original permutation size
    while len(candidate["permutation"]) < problemSize:
        # Get all points except for ones present in candidate solution
        candidates = [item for item in perm if item not in candidate["permutation"]]
        # Calculate the cost of adding feature to solution
        # Here a 'feature' is defined by the how far other points are to the last element of the candidates list
        costs =[]
        candidateSize = len(candidate["permutation"])
        for item in candidates:
            costs.append(euclideanDistance(candidate["permutation"][candidateSize-1], item))
        # Determining the max cost and min cost from the feature set
        rcl, maxCost, minCost = [], max(costs), min(costs)
        # Build the RCL by:
        # We add the one which is <= the  minimum + adjusted feature cost as per RCL formula below
        # Here the smaller the distance, smaller will be the 'final' tour cost!
        # for each feature cost:
        for index,cost in enumerate(costs):# so that we can get both the index and the item while looping
            # IF Fcurrent <= Fmin + alpha * (Fmax-Fmin) THEN
            if (cost <= minCost + alpha * (maxCost-minCost)):
                # Add it to the RCL
                rcl.append(candidates[index])
        # Select random feature from RCL and add it to the solution
        candidate["permutation"].append(rcl[random.randrange(0,len(rcl))])
    # calculate the final tour cost before returning the candidate solution
    candidate["cost"] = tourCost(candidate["permutation"])
    # return solution
    return candidate
def localSearch(best, maxIter):
    count =0
    while count<maxIter:
        candidate ={}
        candidate["permutation"] = stochasticTwoOpt(best["permutation"])
        candidate["cost"] = tourCost(candidate["permutation"])
        if candidate["cost"] < best["cost"]:# We also restart the search when we find the local optima
            best,count = candidate, 0
        else:
            count +=1
    return best
def greedyRandomizedAdaptiveSearch(points, maxIterations, maxNoImprove, threshold):
    best = None
    while maxIterations>0:
        # Construct a Greedy solution
        candidate = constructGreedySolution(points, threshold)
        # refine it using a local search heuristic
        candidate = localSearch(candidate,maxNoImprove)
        if best==None or candidate["cost"]< best["cost"]:
            best = candidate
        maxIterations -=1
    return best
