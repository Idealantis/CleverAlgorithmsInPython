'''
Created on July 8, 2017

@author: Sai
'''
import math, random,time
import numpy as np
# Objective function that evaluates the cost
def basinFunction(vector):
    # original basin function from Clever Algorithms book
    #return sum([pow(item,2) for item in vector])
    a,h,k = 0.5,2,-5
    return sum([a * pow((item-h),2) + k for item in vector])
def getRandomWithinBounds(min, max):
    return min + (max - min) * random.random()
# Randomizing function that selects random  inputs for the objective function
def randomSolution(minMax, problemSize):
    inputValues =[]
    while problemSize>0:
        # generates a value between the minimum and maximum values of the search space
        inputValues.append(getRandomWithinBounds(minMax[0], minMax[1]))
        problemSize -=1
    return inputValues
# Function to take a step and return the objective function value
def takeStep(bounds, currentInput, stepSize):
    stepInput =[]
    for index in range(0,len(currentInput)):
        lBound = max([bounds[0], currentInput[index] - stepSize ])
        uBound = min([bounds[1], currentInput[index] + stepSize])
        stepInput.append(getRandomWithinBounds(lBound, uBound))
    return stepInput

# Function which calculates the euclidean distance between two points
def euclideanDistance(v1, v2):
    # use Zip to iterate over the two vectors
    sum =0.0
    for coord1,coord2 in zip(v1,v2):
        sum += pow((coord1-coord2), 2)
    return math.sqrt(sum)
# Function that evaluates the total length of a path
def tourCost(perm):
    # Here tour cost refers to the sum of the euclidean distance between consecutive points starting from first element
    totalDistance =0.0
    size = len(perm)
    for index in range(size):
        # select the consecutive point for calculating the segment length
        if index == size-1 :
            # This is because in order to complete the 'tour' we need to reach the starting point
            point2 = perm[0]
        else: # select the next point
            point2 = perm[index+1]

        totalDistance +=  euclideanDistance(perm[index], point2)
    return totalDistance
# Function that deletes two edges and reverses the sequence in between the deleted edges
def stochasticTwoOpt(perm):
    result = perm[:] # make a copy
    size = len(result)
    # select indices of two random points in the tour
    p1, p2 = random.randrange(0,size), random.randrange(0,size)
    # do this so as not to overshoot tour boundaries
    exclude = set([p1])
    if p1 == 0:
        exclude.add(size-1)
    else:
        exclude.add(p1-1)
    if p1 == size-1:
        exclude.add(0)
    else:
        exclude.add(p1+1)
    while p2 in exclude:
        p2 = random.randrange(0,size)
    # to ensure we always have p1<p2
    if p2<p1:
        p1, p2 = p2, p1
    # now reverse the tour segment between p1 and p2
    result[p1:p2] = reversed(result[p1:p2])
    return result
def stochasticTwoOptWithEdges(perm):
    result = perm[:] # make a copy
    size = len(result)
    # select indices of two random points in the tour
    p1, p2 = random.randrange(0,size), random.randrange(0,size)
    # do this so as not to overshoot tour boundaries
    exclude = set([p1])
    if p1 == 0:
        exclude.add(size-1)
    else:
        exclude.add(p1-1)
    if p1 == size-1:
        exclude.add(0)
    else:
        exclude.add(p1+1)
    while p2 in exclude:
        p2 = random.randrange(0,size)
    # to ensure we always have p1<p2
    if p2<p1:
        p1, p2 = p2, p1
    # now reverse the tour segment between p1 and p2
    result[p1:p2] = reversed(result[p1:p2])
    return result, [[perm[p1-1],perm[p1]],[perm[p2-1],perm[p2]]]
# Function that creates a random permutation from an initial permutation by shuffling the elements in to a random order
def constructInitialSolution(initPerm):
    #Randomize the initial permutation
    permutation = initPerm[:] # make a copy of the initial permutation
    size = len(permutation)
    for index in range(size):
        # shuffle the values of the initial permutation randomly
        # get a random index and exchange values
        shuffleIndex = random.randrange(index,size)# randrange would exclude the upper bound
        permutation[shuffleIndex], permutation[index]= permutation[index], permutation[shuffleIndex]
    return permutation
# for calculating the total value and weight of knapsack
def totalValue(items,limit):
    # get all the items
    totwt = totval = 0
    for item, wt, val in items:
        totwt  += wt # calculate the total weight and total value
        totval += val # calculate the total value
    # return the weight and value tuple
    return (totval, -totwt) if totwt <= limit else (0, 0)
# for 0/1 knapsack problem using dynamic programming
def zeroOneKnapsackSolverByDynamicProgram(items,limit):
    start_time = time.time()
    # create an array with n+1 rows and w+1 columns
    table = [[0 for w in range(limit + 1)] for j in xrange(len(items) + 1)]
    for j in xrange(1,len(items)+1):
        item, wt, val = items[j-1] # get each individual item from items list
        for w in xrange(1, limit + 1):
            if wt > w: # get each value from 1 to limit and check if it is less than total weight
                table[j][w] = table[j-1][w] # make the table[j][w] value 0
            else:
                # formula t(i,j) = max(t(i-1,j),vali+t(i-1,j-wi))
                table[j][w] = max(table[j-1][w],table[j-1][w-wt] + val)
    result = []
    w = limit
    for j in range(len(items), 0, -1):
        # get the last column and the last element of last column becomes the total value
        # and then check the last cols value with the prev value if not same then consider that item
        was_added = table[j][w] != table[j-1][w]
        if was_added:
            item, wt, val = items[j-1] # get the item,wt, value of picked items
            result.append(items[j-1]) # append the item to the result
            w -= wt # decrease the weight so that we can go back to the 0th row
    end_time = time.time()
    total_time = time.strftime('%Mm %Ss',time.gmtime(end_time-start_time))
    return (result,total_time) # return the result

# MUTATION STRATEGIES START

# BitFlip 
def bitFlip(bitstring, numOfBits):
	newBitString = bitstring
	flag = []
	bitIndex = 0
	numOfZeros = numOfBits - bitstring.count('1')
	while(numOfZeros):
		while True:
			bitIndex = random.randint(0,numOfBits-1)
			if(bitIndex in flag):
				continue
			flag.insert(0, bitIndex)
			break
		if newBitString[bitIndex] == '0':
			newBitString = newBitString[0:bitIndex]+'1'+newBitString[bitIndex+1:numOfBits]
		else:
			newBitString = newBitString[0:bitIndex]+'0'+newBitString[bitIndex+1:numOfBits]
		numOfZeros -= 1
	return newBitString

# Swap
def swapMutaion(bitstring, numOfBits):
	newBitString = bitstring
	bitsToBeFlipped = random.sample(range(0, numOfBits), 2)
	
	newBitString = newBitString[ 0 : bitsToBeFlipped[0] ] + bitstring[ bitsToBeFlipped[1] ] + newBitString[ bitsToBeFlipped[0] + 1 : numOfBits ]
	newBitString = newBitString[ 0 : bitsToBeFlipped[1] ] + bitstring[ bitsToBeFlipped[0] ] + newBitString[ bitsToBeFlipped[1] + 1 : numOfBits ]
	return newBitString

#Scramble 
def scrambleMutation(bitstring, numOfBits):
	bRangeScramble = random.sample(range(0, numOfBits), 2)
	newBitString = bitstring
	if(bRangeScramble[0] > bRangeScramble[1]):
        temp = bRangeScramble[1]
        bRangeScramble[1] = bRangeScramble[0]
        bRangeScramble[0] = temp
	flag = random.sample(range(bRangeScramble[0], bRangeScramble[1]), bRangeScramble[1]-bRangeScramble[0])
	index = 0
	for i in range(bRangeScramble[0], bRangeScramble[1]):
		newBitString = newBitString[0:i]+bitstring[flag[index]]+newBitString[i+1:numOfBits]
		index += 1
	return newBitString

#Inversion
def inversionMutation(bitstring, numOfBits):
	bRangeInverse = random.sample(range(0,numOfBits),2)
	newBitString = bitstring
	if(bRangeInverse[0] > bRangeInverse[1]):
        temp = bRangeInverse[1]
        bRangeInverse[1] = bRangeInverse[0]
        bRangeInverse[0] = temp
	index = bRangeInverse[1]
	for i in range(bRangeInverse[0], bRangeInverse[1]+1):
		newBitString = newBitString[0:i]+bitstring[index]+newBitString[i+1:numOfBits]
		index -= 1
	return newBitString

# MUTATION STRATEGIES END

def getPopulation(numOfBits, popSize):
	population = [{"bitstring":None,"fitness":None}]*popSize
	for i in range(popSize):
		temp = ''.join( '1' if random.random() < 0.5 else '0' for i in range(numOfBits))
		population[i] = {"bitstring":temp,"fitness":oneMax(temp)}
	return population

def sumOfPopulationFit(population, popSize):
	sum = 0
	for i in range(popSize):
		sum += population[i]['fitness']
	return sum

def findAbsoulteIndex(A, value):
	A = np.array(A)
	index = ( np.abs(A-value)).argmin()
	return index

def getRangeBasedFitnesses(population, popSize):
	tempList = range(popSize)
	random.shuffle(tempList)
	A = [None]*(popSize*2)
	temp = 0
	j = 0
	for randomIndex in tempList:
		A[j] = temp+1
		A[j+1] = A[j]+population[randomIndex]['fitness']-1
		temp = A[j+1]
		j += 2
	return A

# PARENT SELECTION STRATEGIES START
# Roulette Wheel 
def rouletteWheelSelection(population, popSize):
	A = getRangeBasedFitnesses(population, popSize)
	randomNumOnWheel = random.randint(1, sum)
	parentIndex = findAbsoulteIndex(A, randomNumOnWheel)
	return population[parentIndex/2]

# Stochastic Universal Sampling(SUS)
def StochasticUniversalSampling(population, popSize):
	A = getRangeBasedFitnesses(population, popSize)
	tempPopulation = [None]*popSize
	for i in range(popSize):
		tempPopulation[i] = population[findAbsoulteIndex(A, random.randint(1, sum))/2]
	return tempPopulation

# Rank Selection
def rankSelection(rankPopulation, popSize):
	i = random.randint(0,popSize/2)
	j = random.randint(0,popSize/2)
	while i != j:
		j = random.randint(0,popSize)
	return rankPopulation[i] if rankPopulation[i]['fitness'] > rankPopulation[j]['fitness'] else rankPopulation[j]

# PARENT SELECTION STRATEGIES END