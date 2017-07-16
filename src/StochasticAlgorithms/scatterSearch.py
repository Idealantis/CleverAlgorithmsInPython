'''
Created on Jun 15, 2017
@author: Sai Panyam

Credits
Inspired by Clever Algorithms by Jason Brownlee
www.cleveralgorithms.com
'''
'''
Name
Scatter Search, SC

Taxonomy
Scatter search is a Metaheuristic and a Global Optimization algorithm. It is also sometimes associated with the field of
Evolutionary Computation given the use of a population and recombination in the structure of the technique.
Scatter Search is a sibling of Tabu Search.

Strategy
The objective of Scatter Search is to maintain a set of diverse and high quality candidate solutions.
The principle of the approach is that useful information about the global optima is stored in a diverse
and elite set of solutions (the reference set) and that recombining samples from the set can exploit this information.
The strategy involves an iterative process, where a population of diverse and high-quality candidate solutions that
are partitioned into subsets and linearly recombined to create weighted centroids of sample-based neighborhoods.
The results of recombination are refined using an embedded heuristic (Local Search) and assessed in the context of the
reference set as to whether or not they are retained.

Heuristics
Scatter search is suitable for both discrete domains such as combinatorial optimization as well as continuous domains
such as non-linear programming (continuous function optimization).
Small set sizes are preferred for the ReferenceSet, such as 10 or 20 members.
Subset sizes can be 2, 3, 4 or more members that are all recombined to produce viable candidate solutions
within the neighborhood of the members of the subset.
Each subset should comprise at least one member added to the set in the previous algorithm iteration.
The Local Search procedure should be a problem-specific improvement heuristic.
The selection of members for the ReferenceSet at the end of each iteration favors solutions with higher quality and may also promote diversity.
The ReferenceSet may be updated at the end of an iteration, or dynamically as candidates are
created (a so-called steady-state population in some evolutionary computation literature).
A lack of changes to the ReferenceSet may be used as a signal to stop the current search, and
potentially restart the search with a newly initialized ReferenceSet.
'''
from Helpers.Utilities import basinFunction, randomSolution, takeStep, euclideanDistance
import operator,random
def distance(candidate, ref):
    candidate["distance"] = reduce(lambda x,y: x + euclideanDistance(candidate["vector"],y["vector"]), ref, 0.0 )
    return candidate
def localSearchHeuristic(best, bounds, maxNoImprove, stepSize):
    candidate = {}
    while maxNoImprove>0:
        candidate["vector"] = takeStep(bounds, best["vector"], stepSize)
        candidate["cost"] = basinFunction(candidate["vector"])
        if candidate["cost"] < best["cost"]:
            best = candidate
        maxNoImprove -=1
    return best
def selectSubsets(ref):
    subsets =[]
    refCopy = ref[:]
    # now take an element from main ref set and self join to its copy
    # basically do a combination on itself. i.e. [a,b]==[b,a] and a!=b
    for outer in ref:
        for inner in refCopy:
            if inner !=outer and ([inner,outer] not in subsets):
                subset = [outer,inner]
                subsets.append(subset)
    return subsets
def constructInitialSet(setSize, bounds, maxNoImprove, stepSize, problemSize):
    diverseList = []
    candidate ={}
    candidate["vector"] = randomSolution(bounds,problemSize)
    candidate["cost"] = basinFunction(candidate["vector"])
    while len(diverseList)< setSize:
        refined = localSearchHeuristic(candidate, bounds, maxNoImprove, stepSize)
        if refined not in diverseList:
            diverseList.append(refined)
    return diverseList
def selectReferenceSet(setSize, diverseList, maxElite):
    diverseList.sort(key = operator.itemgetter("cost")) # In place sort cmp = lambda x,y: cmp(x["cost"],y["cost"])
    reference = diverseList[:maxElite] # make a copy of the diverse list of size maxElite
    # get the remainder elements from diverse list not present in reference list
    remainder = diverseList[maxElite:]
    # calculate the euclidean distance of each element in remainder with each element in the reference list
    remainder = [distance(item, reference) for item in remainder]
    remainder.sort(key = operator.itemgetter("distance"))
    reference = reference + remainder[0:setSize-len(reference)]
    return reference, reference[0]
def recombineMembers(subset, minmax):
    a,b =subset # unpack the elements of the set
    delta = random.uniform(0,euclideanDistance(a["vector"], b["vector"]))/2.0
    children = []
    for candidate in subset:
        if random.random()>0.5:
            step = delta
        else:
            step =-delta
        child ={}
        child["vector"]= [item + step for item in candidate["vector"]]
        # stay within the min max bounds
        lBound = max(child["vector"][0], minmax[0])
        uBound = min(child["vector"][1], minmax[1])
        child["vector"]=[lBound, uBound]
        child["cost"] = basinFunction(child["vector"])
        children.append(child)
    return children
def selectBest(referenceSet, candidateSet, refSetSize):
    change = False
    for candidate in candidateSet:
        if candidate not in referenceSet:
            referenceSet.sort(key = operator.itemgetter("cost"))
            if candidate["cost"]<referenceSet[refSetSize-1:refSetSize]:
                # remove and replace the last element with the candidate
                referenceSet.pop(refSetSize-1)
                referenceSet.append(candidate)
                change =True
    return change
def scatterSearch(searchSpace, problemSize, referenceSetSize, diverseSetSize, maxIterations, maxNoImprove, maxElite, stepSize):
    # Construct Initial Set which employs an embedded local search heuristic to refine the results and
    #the configurable diverse set size
    diverse = constructInitialSet(diverseSetSize, searchSpace, maxNoImprove, stepSize, problemSize)

    # Construct the Reference Set from the initial refined set by employing Diversification
    reference, best = selectReferenceSet(referenceSetSize, diverse, maxElite)

    # Iterate for maxIterations
    while maxIterations>0:
        # select subsets from reference sets
        subsets = selectSubsets(reference)
        candidates =[]
        # for each subset in subsets
        for subset in subsets:
            # recombine subsets to get candidates
            recombined = recombineMembers(subset, searchSpace)
            # for each of the recombined candidates do a local search
            for candidate in recombined:
                # and add it to a candidate set
                candidates.append(localSearchHeuristic(candidate, searchSpace, maxNoImprove, stepSize))

        # return the best candidate from the final candidate set and reference set
        wasChanged = selectBest(reference, candidates, referenceSetSize)
        if reference[0]["cost"] < best["cost"]:
            best = reference[0]

        if not wasChanged:
            break
        maxIterations -=1
    return best

