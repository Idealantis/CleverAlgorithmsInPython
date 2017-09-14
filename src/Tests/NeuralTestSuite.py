'''
Created on Sep 14, 2017

@author: Sai Panyam

Unit tests that exercise the algorithms. It is a mixture of both real 'unit' tests and functional tests of search
'''
class TestNeuralAlgorithms:
    def test_Perceptron(self):
        from NeuralAlgorithms.Perceptron import perceptron
        #algorithm configuration
        trainData = [[1,0,1],[0,1,1], [1,0,1], [1,1,0]]
        inputSize=2
        epochs=20
        learningRate=0.01
        weights, accuracy = perceptron(trainData, inputSize, epochs, learningRate)
        print("*"*30)
        print("")
        print("Weights:",weights)
        print("Accuracy :",accuracy)
        print("")
        print("*"*30)
    def test_Backpropagation(self):
        from NeuralAlgorithms.Backpropagation import createBPN,trainBPN,predict
        trainset = [[2.7810836,2.550537003,0],
	                [1.465489372,2.362125076,0],
	                [3.396561688,4.400293529,0],
	                [1.38807019,1.850220317,0],
	                [3.06407232,3.005305973,0],
	                [7.627531214,2.759262235,1],
	                [5.332441248,2.088626775,1],
	                [6.922596716,1.77106367,1],
	                [8.675418651,-0.242068655,1],
	                [7.673756466,3.508563011,1]]
        lrate = 0.6
        epoch = 250
        nInputs = len(trainset[0]) - 1
        nOutputs = len(set([row[-1] for row in trainset]))
        network = createBPN(nInputs, 2, nOutputs)
        trainBPN(network,trainset,lrate,epoch,nOutputs)
        for layer in network:
            print(layer)
        print('Complted the training')
        testset = [[2.7810836,2.550537003,0],
	                [1.465489372,2.362125076,0],
	                [3.396561688,4.400293529,0],
	                [1.38807019,1.850220317,0],
	                [3.06407232,3.005305973,0],
	                [7.627531214,2.759262235,1],
	                [5.332441248,2.088626775,1]]
        for row in testset:
            prediction = predict(network, row)
            print('Expected=%d, Got=%d' % (row[-1], prediction))
