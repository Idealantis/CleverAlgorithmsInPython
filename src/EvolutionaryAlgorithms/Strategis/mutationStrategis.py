import random
#BitFlip
def oneMax(temp):
    return temp.count('1')
'''In this bit flip mutation, we select one or more random bits and flip them.
This is used for binary encoded GAs.
https://www.tutorialspoint.com/genetic_algorithms/genetic_algorithms_mutation.htm
'''
def bitFlip(bitstring, numOfBits, popMutation):
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
# swap mutation
'''
In swap mutation, we select two positions on the chromosome at random,
and interchange the values. This is common in permutation based encodings.

'''
def swapMutaion(bitstring, numOfBits, popMutation):
    newBitString = bitstring
    bitsToBeFlipped = random.sample(range(0, numOfBits), 2)
    newBitString = newBitString[ 0 : bitsToBeFlipped[0] ] + bitstring[ bitsToBeFlipped[1] ] + newBitString[ bitsToBeFlipped[0] + 1 : numOfBits ]
    newBitString = newBitString[ 0 : bitsToBeFlipped[1] ] + bitstring[ bitsToBeFlipped[0] ] + newBitString[ bitsToBeFlipped[1] + 1 : numOfBits ]
    return newBitString
# Scramble mutation
'''
Scramble mutation is also popular with permutation representations. In this,
from the entire chromosome, a subset of genes is chosen and their values are scrambled or shuffled randomly.
'''
def scrambleMutation(bitstring, numOfBits, popMutation):
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
# Inversion Mutation
'''
Scramble mutation is also popular with permutation representations. In this, from the entire chromosome,
a subset of genes is chosen and their values are scrambled or shuffled randomly.
'''
def inversionMutation(bitstring, numOfBits, popMutation):
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
def pointMutation(bitstring, numOfBits, popMutation):
    child = ""
    bLen = numOfBits
    for i in range(bLen):
        bit = bitstring[i]
        child += "0" if bit=='1' else "1" if (random.random() < popMutation) else bit
    return child
