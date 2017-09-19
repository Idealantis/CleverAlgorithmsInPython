from math import exp
from random import seed
from random import random
# Initialize a network
def createBPN(nInputs, nHidden, nOutputs):
	network = list()
	hiddenLayer = [{'weights':[random() for i in range(nInputs + 1)]} for j in range(nHidden)]
	network.append(hiddenLayer)
	outputLayer = [{'weights':[random() for i in range(nHidden + 1)]} for j in range(nOutputs)]
	network.append(outputLayer)
	return network
# Calculate neuron activation for an input
def activate(weights, inputs):
	activation = weights[-1]
	for i in range(len(weights)-1):
		activation += weights[i] * inputs[i]
	return activation

# Transfer neuron activation
def transfer(activation):
	return 1.0 / (1.0 + exp(-activation))

# Forward propagate input to a network output
def forwardPropagate(network, row):
	inputs = row
	for layer in network:
		newInputs = []
		for neuron in layer:
			activation = activate(neuron['weights'], inputs)
			neuron['output'] = transfer(activation)
			newInputs.append(neuron['output'])
		inputs = newInputs
	return inputs

# Calculate the derivative of an neuron output
def transferDerivative(output):
	return output * (1.0 - output)

# Backpropagate error and store in neurons
def backwardPropagateError(network, expected):
	for i in reversed(range(len(network))):
		layer = network[i]
		errors = list()
		if i != len(network)-1:
			for j in range(len(layer)):
				error = 0.0
				for neuron in network[i + 1]:
					error += (neuron['weights'][j] * neuron['delta'])
				errors.append(error)
		else:
			for j in range(len(layer)):
				neuron = layer[j]
				errors.append(expected[j] - neuron['output'])
		for j in range(len(layer)):
			neuron = layer[j]
			neuron['delta'] = errors[j] * transferDerivative(neuron['output'])

# Update network weights with error
def updateWeights(network, row, lrate):
	for i in range(len(network)):
		inputs = row[:-1]
		if i != 0:
			inputs = [neuron['output'] for neuron in network[i - 1]]
		for neuron in network[i]:
			for j in range(len(inputs)):
				neuron['weights'][j] += lrate * neuron['delta'] * inputs[j]
			neuron['weights'][-1] += lrate * neuron['delta']

# Train a network for a fixed number of epochs
def trainBPN(network, train, lrate, epoch, nOutputs):
	for epoch in range(epoch):
		sumError = 0
		for row in train:
			outputs = forwardPropagate(network, row)
			expected = [0 for i in range(nOutputs)]
			expected[row[-1]] = 1
			sumError += sum([(expected[i]-outputs[i])**2 for i in range(len(expected))])
			backwardPropagateError(network, expected)
			updateWeights(network, row, lrate)
		print('>epoch=%d, lrate=%.3f, error=%.3f' % (epoch, lrate, sumError))
# Make a prediction with a network
def predict(network, row):
	outputs = forwardPropagate(network, row)
	return outputs.index(max(outputs))
