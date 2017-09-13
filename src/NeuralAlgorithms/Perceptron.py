import numpy as np

def activate(weights, pattern):
    sum = weights[len(weights)-1]*1.0
    for index, element in enumerate(pattern):
        sum += weights[index]*element
    return sum
def updateWeights(inputSize, weights, pattern, expected, output, learningRate):
    for index in range(inputSize):
        weights[index] += learningRate*(expected-output)*pattern[index]
    weights[inputSize] += learningRate*(expected-output)*1.0
    return weights
def getOutput(weights, pattern):
    activation = activate(weights, pattern)
    return 1.0 if activation >= 0 else 0.0
def train(weights, trainInput, trainExpected, inputSize, epochs, learningRate):
    for epoch in range(epochs):
        print("Epoch #"+str(epoch))
        error = 0.0
        for i, pattern in enumerate(trainInput):
            pattern = pattern.astype(float)
            output = getOutput(weights, pattern)
            expected = float(trainExpected[i])
            error += np.absolute(output - expected)
            weights = updateWeights(inputSize, weights, pattern, expected, output, learningRate)
        print("Weights",weights)
        print("Error rate :",error)
    return weights
def test(weights, testInput, testExpected, learningRate):
    accuracy = 0
    for index, pattern in enumerate(testInput):
        output = getOutput(weights, pattern)
        if output == testExpected[index]:
            accuracy += 1
    return (accuracy*100.0)/len(testInput)

def perceptron(trainData, inputSize, epochs=20, learningRate=0.01):
    trainData = np.array(trainData)
    # divide the train data as input and output
    trainInput = trainData[:,:inputSize]
    trainExpected = trainData[:,inputSize]
    # Initialize weights randomly
    weights = np.random.uniform(-1,1,inputSize+1)
    # train weights with trainData
    weights = train(weights, trainInput, trainExpected, inputSize, epochs, learningRate)
    # In our case testData and trainData are same
    testInput, testExpected = trainInput, trainExpected
    accuracy = test(weights, testInput, testExpected, learningRate)
    return list(weights), accuracy