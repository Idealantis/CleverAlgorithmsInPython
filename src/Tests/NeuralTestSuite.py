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