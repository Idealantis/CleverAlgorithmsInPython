import random
def oneMax(temp):
    return temp.count('1')
# helper function to make copy contents one to other, from parents to children
def makeCrossOver(child1, child2, parent1, parent2, startIndex, endIndex,flag):
    if(flag % 2):
        child1 += parent1[startIndex:endIndex]
        child2 += parent2[startIndex:endIndex]
    else:
        child1 += parent2[startIndex:endIndex]
        child2 += parent1[startIndex:endIndex]
    return child1, child2
# Multipoing CrossOver
'''
Multi point crossover is a generalization of the one-point crossover wherein alternating
segments are swapped to get new off-springs. '''
def multiPointCrossOver(parent1, parent2, popCrossOver):
	if random.random() >= popCrossOver:
		return parent1
	length = len(parent1) + 1
	numOfPoints = random.randint(1, len(parent1)/2)
	pointsToMakeCrossOver = sorted(random.sample( range( 1, length ), numOfPoints ))
	child1, child2, startIndex, startIndex = '', '', 0, 0
	flag = 0
	for endIndex in pointsToMakeCrossOver:
		child1, child2 = makeCrossOver(child1, child2, parent1, parent2, startIndex, endIndex, flag)
		startIndex = endIndex
		flag += 1
	child1, child2 = makeCrossOver(child1, child2, parent1, parent2, startIndex, length-1, flag)
	if oneMax(child1) > oneMax(child1):
		return child1
	return child2
# Uniform Crossover - written this crossover strategy in basic way
# We can make this crossover so it can have maximum fitness
'''
In a uniform crossover, we dont divide the chromosome into segments,
rather we treat each gene separately. In this, we essentially flip a coin
for each chromosome to decide whether or not it will be included in the off-spring.
We can also bias the coin to one parent, to have more genetic material in the child from that parent.'''
def uniformCrossOver(parent1, parent2, popCrossOver):
	child1, child2 = '',''
	length = len(parent1)
	for i in range(length):
		if random.random() > 0.5:
			child1 += parent2[i]
			child2 += parent1[i]
		else:
			child1 += parent1[i]
			child2 += parent2[i]
	if oneMax(child1)>oneMax(child2):
		return child1
	return child2
# one point crossover
'''
In this one-point crossover, a random crossover point is
selected and the tails of its two parents are swapped to get new off-springs.
'''
def onePointCrossOver(parent1, parent2, popCrossOver):
    if random.random()> popCrossOver:
        return parent1
    point = 1 + random.randint(1,len(parent1) - 2)
    return parent1[0:point]+parent2[point:len(parent1)]
