'''
Created on July 15, 2017
@author: Sai Panyam

Credits
Inspired by Clever Algorithms by Jason Brownlee
www.cleveralgorithms.com
'''
'''
Name
Reactive Tabu Search, RTS, R-TABU, Reactive Taboo Search

Taxonomy
Reactive Tabu Search is a Metaheuristic and a Global Optimization algorithm. It is an extension of
Tabu Search and the basis for a broad field called Reactive Search Optimization.

Strategy
The strategy used by RTS is to monitor the search and react to occurrence of cycles and their repetition by
adapting the tabu tenure.

Heuristics
Reactive Tabu Search was proposed to use an long-term memory to diversify the search after a
threshold of cycle repetitions has been reached.

The increase parameter should be greater than one (such as 1.1 or 1.3) and the decrease parameter should be
less than one (such as 0.9 or 0.8).
'''
from Helpers.Utilities import constructInitialSolution, tourCost, stochasticTwoOptWithEdges
# module level variables used in search function
tabuList, prohibitionPeriod = [],1
visitedList, tProhibitionPeriod, avgRepetitionInterval =[],0,1
def convertToEdgeList(perm):
    edges = []
    size = len(perm)
    for index in range(0,size):
        index1 = index
        if index == size-1:
            index2 = 0
        else:
            index2 = index +1

        if index2<index1:
            index1,index2 = index2, index1
        edges.append([perm[index1], perm[index2]])
    return edges
def isEquivalent(e1, e2):
    for edge in e1:
        if edge not in e2:
            return False
    return True
def haveVisitedSolutionBefore(perm, visitedList):
    edgeList = convertToEdgeList(perm)
    for visited in visitedList:
        if isEquivalent(visited["edges"], edgeList):
            return visited
    return None
def memoryBasedReaction(current,increase, decrease,iteration):
    global prohibitionPeriod,tProhibitionPeriod, avgRepetitionInterval,visitedList
    candidateEntry = haveVisitedSolutionBefore(current["permutation"], visitedList)
    if candidateEntry != None:
        # Do when visited
        # calculate repetition interval : current iteration - visited iteration
        repetitionInterval = iteration - candidateEntry["iteration"]
        # Update candidate entry's iteration to current iteration
        candidateEntry["iteration"] = iteration
        # Update the visit count by 1 as we encountered this again
        candidateEntry["visits"] +=1
        # Update average repetition interval if the current RI is less than twice the original size
        if repetitionInterval < 2 * (len(current["permutation"])):
            avgRepetitionInterval = 0.1 * repetitionInterval + 0.9 * avgRepetitionInterval
            # Update Prohibition Period and record last update for PP
            prohibitionPeriod = prohibitionPeriod * increase
            tProhibitionPeriod = iteration
    else:
        entry ={}
        entry["edges"] = convertToEdgeList(current["permutation"])
        entry["iteration"] = iteration
        entry["visits"] = 1
        visitedList.append(entry)

    if (iteration - tProhibitionPeriod) > avgRepetitionInterval:
        prohibitionPeriod = max([1, float(prohibitionPeriod) * decrease])
        tProhibitionPeriod = iteration
def isTabu(edge,iteration):
    global prohibitionPeriod
    for tabu in tabuList:
        if tabu["edge"] == edge:
            if tabu["iteration"] >= iteration - prohibitionPeriod:
                return True
            else:
                return False
    return False
def partitionCandidates(candidates, iteration):
    admissible, tabu = [],[]
    # First sort candidates by cost
    candidates.sort(key = lambda(c): c["candidate"]["cost"])
    for candidate in candidates:
        if isTabu(candidate["edges"][0], iteration) or isTabu(candidate["edges"][1],iteration):
            tabu.append(candidate)
        else:
            admissible.append(candidate)
    return admissible, tabu
def bestMove(candidates, iteration, problemSize, best):
    global prohibitionPeriod,tProhibitionPeriod, avgRepetitionInterval
    bestCandidate ={}
    bestTabu ={}
    bestMoveEdges =[]
    admissible, tabu = partitionCandidates(candidates, iteration)
    if len(admissible)<2:
        prohibitionPeriod = problemSize -2
        tProhibitionPeriod = iteration
    if admissible!=None and len(admissible)>0:
        bestCandidate = admissible[0]["candidate"]
        bestMoveEdges = admissible[0]["edges"]
    else:
        bestCandidate = tabu[0]["candidate"]
        bestMoveEdges = tabu[0]["edges"]

    if tabu !=None and len(tabu)>0:
        bestTabu = tabu[0]["candidate"]
        if bestTabu["cost"]<best["cost"] and bestTabu["cost"]<bestCandidate["cost"]:
            bestCandidate = tabu[0]["candidate"]
            bestMoveEdges = tabu[0]["edges"]
    return bestCandidate, bestMoveEdges
def updateTabuList(edge,iteration):
    global tabuList
    for tabu in tabuList:
        if tabu["edge"]==edge:
            tabu["iteration"]=iteration
            return tabu
    tabu = {}
    tabu["edge"] = edge
    tabu["iteration"] = iteration
    tabuList.append(tabu)
    return tabu
def generateCandidateNeighborhood(current):
    result = {}
    permutation, edges = stochasticTwoOptWithEdges(current["permutation"])
    candidate ={}
    candidate["permutation"] = permutation
    candidate["cost"] = tourCost(candidate["permutation"])
    result["candidate"] = candidate
    result["edges"] = edges
    return result
def reactiveTabuSearch(points, maxIterations, increase, decrease, maxCandidates):
    current ={}
    current["permutation"] = constructInitialSolution(points)
    current["cost"] = tourCost(current["permutation"])
    best = current
    iteration =0
    while iteration < maxIterations:
        # Memory based reaction
        memoryBasedReaction(current,increase, decrease, iteration)
        # Generate Candidate list from neighborhood from current
        candidates = []
        for index in range(0,maxCandidates):
            candidates.append(generateCandidateNeighborhood(current))
        # From candidate list get best
        current, bestEdges = bestMove(candidates, iteration,len(points), best)
        # Update tabu list with the current candidates features
        for edge in bestEdges:
            updateTabuList(edge,iteration)
        # Compare cost of current with best and update best if less than current
        if current["cost"] < best["cost"]:
            best = current
        iteration +=1
    #return best
    return best
