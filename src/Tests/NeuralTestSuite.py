'''
Created on Sep 14, 2017

@author: Sai Panyam

Unit tests that exercise the algorithms. It is a mixture of both real 'unit' tests and functional tests of search
'''
class TestNeuralAlgorithms:
    def test_Perceptron(self):
        from NeuralAlgorithms.Perceptron import perceptron
        #algorithm configuration
        trainData = [[0,0,0],[0,1,1], [1,0,1], [1,1,1]]
        inputSize=2
        epochs=20
        learningRate=0.1
        weights, accuracy = perceptron(trainData, inputSize, epochs, learningRate)
        print("*"*30)
        print("")
        print("Weights:",weights)
        print("Accuracy :",accuracy)
        print("")
        print("*"*30)
    def test_Backpropagation(self):
        from NeuralAlgorithms.Backpropagation import createBPN,trainBPN,predict
        trainset = [[0,0,0],[0,1,1],[1,0,1],[1,1,0]]
        lrate = 0.5
        epoch = 150
        nInputs = len(trainset[0]) - 1
        nOutputs = len(set([row[-1] for row in trainset]))
        network = createBPN(nInputs, 2, nOutputs)
        trainBPN(network,trainset,lrate,epoch,nOutputs)
        for layer in network:
            print(layer)
        print('Complted the training')
        testset = [[0,0,0],[0,1,1],[1,0,1]]
        for row in testset:
            prediction = predict(network, row)
            print('Expected=%d, Got=%d' % (row[-1], prediction))
