'''
Created on July 8, 2017

@author: Sai
'''
import math,random,time
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
# 0/1 KNAPSACK BY GENETIC ALGO
def crossover(ind1,ind2,KNAPSACK_ITEMS,NUM_ITEMS,MAX_WEIGHT):
    cop = random.randint(1,NUM_ITEMS-2)
    new_ind1 = ind1[0:cop] + ind2[cop:NUM_ITEMS]
    new_ind2 = ind2[0:cop] + ind1[cop:NUM_ITEMS]
    while fitness(new_ind1,KNAPSACK_ITEMS,NUM_ITEMS,MAX_WEIGHT) == 0:
        ones = [i for i,x in enumerate(new_ind1) if x==1]
        new_ind1[random.choice(ones)] = 0
    while fitness(new_ind2,KNAPSACK_ITEMS,NUM_ITEMS,MAX_WEIGHT) == 0:
        ones = [i for i,x in enumerate(new_ind2) if x==1]
        new_ind2[random.choice(ones)] = 0
    return new_ind1,new_ind2
def select(p,KNAPSACK_ITEMS,NUM_ITEMS,MAX_WEIGHT):
    ind1,ind2 = random.sample(p,2)
    if fitness(ind1,KNAPSACK_ITEMS,NUM_ITEMS,MAX_WEIGHT) > fitness(ind2,KNAPSACK_ITEMS,NUM_ITEMS,MAX_WEIGHT):
        return ind1
    else:
        return ind2
def mutate(ind,KNAPSACK_ITEMS,NUM_ITEMS,MAX_WEIGHT):
    chrom = random.randint(0,NUM_ITEMS - 1)
    ind[chrom] = int(not ind[chrom])
    while fitness(ind,KNAPSACK_ITEMS,NUM_ITEMS,MAX_WEIGHT) == 0:
        ones = [i for i,x in enumerate(ind) if x==1]
        ind[random.choice(ones)] = 0
    return ind
def evolve(p,KNAPSACK_ITEMS,POPULATION_SIZE,ELITISM_PERC,CROSSOVER_PROB,MUTATION_PROB,NUM_ITEMS,MAX_WEIGHT):
    elite_elements = POPULATION_SIZE * ELITISM_PERC / 100.0
    crossover_float = CROSSOVER_PROB / 100.0
    mutation_float = MUTATION_PROB / 100.0
    sorted_p = [ind for fitn,ind in reversed(sorted([(fitness(ind,KNAPSACK_ITEMS,NUM_ITEMS,MAX_WEIGHT),ind) for ind in p]))]
    new_population = []
    for i in xrange(POPULATION_SIZE/2):
        if i < elite_elements:
            mother = sorted_p[i]
            father = sorted_p[i+1]
        else:
            mother = select(p,KNAPSACK_ITEMS,NUM_ITEMS,MAX_WEIGHT)
            father = select(p,KNAPSACK_ITEMS,NUM_ITEMS,MAX_WEIGHT)
        if random.random() < crossover_float:
            child1,child2 = crossover(mother,father,KNAPSACK_ITEMS,NUM_ITEMS,MAX_WEIGHT)
        else:
            child1 = mother
            child2 = father
        if random.random() < mutation_float:
            child1=mutate(child1,KNAPSACK_ITEMS,NUM_ITEMS,MAX_WEIGHT)
        if random.random() < mutation_float:
            child2=mutate(child2,KNAPSACK_ITEMS,NUM_ITEMS,MAX_WEIGHT)
        new_population.append(child1)
        new_population.append(child2)
    return new_population
def get_fittest(p,KNAPSACK_ITEMS,NUM_ITEMS,MAX_WEIGHT):
    best_fitness,fittest_ind = max([(fitness(ind,KNAPSACK_ITEMS,NUM_ITEMS,MAX_WEIGHT),ind) for ind in p])
    return fittest_ind,best_fitness
def fitness(ind,KNAPSACK_ITEMS,NUM_ITEMS,MAX_WEIGHT):
    fitness = 0
    knap_weight = 0
    for i,item in enumerate(KNAPSACK_ITEMS[:NUM_ITEMS]):
        if ind[i] == 1:
            value,weight = item[2],item[1]
            fitness += value
            knap_weight += weight
    if knap_weight > MAX_WEIGHT:
        return 0
    return fitness
def validate_population(p,KNAPSACK_ITEMS,NUM_ITEMS,MAX_WEIGHT):
    for ind in p:
        while fitness(ind,KNAPSACK_ITEMS,NUM_ITEMS,MAX_WEIGHT) == 0:
            ones = [i for i,x in enumerate(ind) if x==1]
            ind[random.choice(ones)] = 0
    return p
def zeroOneKnapsackSolverByGeneticAlgo(KNAPSACK_ITEMS,MAX_WEIGHT,NUM_ITEMS,POPULATION_SIZE,ELITISM_PERC,CROSSOVER_PROB,MUTATION_PROB,MAX_STABLE,MAX_GENERATIONS):
    population = [[random.choice((0,1)) for i in xrange(NUM_ITEMS)] for j in xrange(POPULATION_SIZE)]
    population = validate_population(population,KNAPSACK_ITEMS,NUM_ITEMS,MAX_WEIGHT)
    best_solution,best_fitness = get_fittest(population,KNAPSACK_ITEMS,NUM_ITEMS,MAX_WEIGHT)
    start_time = time.time()
    stable_cnt = 0
    generation_cnt = 1
    while True:
        population = evolve(population,KNAPSACK_ITEMS,POPULATION_SIZE,ELITISM_PERC,CROSSOVER_PROB,MUTATION_PROB,NUM_ITEMS,MAX_WEIGHT)
        generation_cnt += 1
        ind,fitness = get_fittest(population,KNAPSACK_ITEMS,NUM_ITEMS,MAX_WEIGHT)
        if fitness > best_fitness:
            best_solution = ind
            best_fitness = fitness
            stable_cnt = 0
        else:
            stable_cnt += 1
        if stable_cnt >= MAX_STABLE:
            break
        if generation_cnt >= MAX_GENERATIONS:
            break
    end_time = time.time()
    print('Solution found in generation %s' % generation_cnt)
    bagged_items=[]
    total_weight = 0
    total_value = 0
    for i in range(0,len(best_solution)):
        if best_solution[i] == 1:
            bagged_items.append(KNAPSACK_ITEMS[i])
            total_value += KNAPSACK_ITEMS[i][2]
            total_weight += KNAPSACK_ITEMS[i][1]
    # print('Fitness : %s'% best_fitness)
    total_time = time.strftime('%Mm %Ss',time.gmtime(end_time-start_time))
    return (bagged_items,total_value,total_weight,total_time)

# MUTATION STRATEGIES START

#BitFlip
def bitFlip(bitstring, numOfBits):
	newBitString = bitstring
	flag = []
	bitIndex = 0
	numOfZeros = numOfBits - oneMax(bitstring)
	while(numOfZeros):
		while True:
			bitIndex = random.randint(0,numOfBits-1)
			if bitIndex in flag:
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
	if bRangeScramble[0] > bRangeScramble[1]:
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
	if bRangeInverse[0] > bRangeInverse[1]:
        temp = bRangeInverse[1]
        bRangeInverse[1] = bRangeInverse[0]
        bRangeInverse[0] = temp
	index = bRangeInverse[1]
	for i in range(bRangeInverse[0], bRangeInverse[1]+1):
		newBitString = newBitString[0:i]+bitstring[index]+newBitString[i+1:numOfBits]
		index -= 1
	return newBitString
# MUTATION STRATEGIES END

def oneMax(temp):
    return temp.count('1')

def binaryTournament(population, popSize):
    i, j = random.randrange(popSize), random.randrange(popSize)
    while j==i:
        j = random.randrange(popSize)
    return population[i] if population[i]["fitness"]>population[j]["fitness"] else population[j]
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
#PARENT SELECTION STRATEGIES END
