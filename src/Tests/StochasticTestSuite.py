'''
Created on July 8, 2017

@author: Sai Panyam

Unit tests that exercise the algorithms. It is a mixture of both real 'unit' tests and functional tests of search
'''
from Helpers.Utilities import basinFunction
from ResultHelpers import TSPResult, BasinResult
class TestClass:
    def setup_method(self):
        self.Vector = [1,2]
        # Problem Configuration
        berlin52 = [[565,575],[25,185],[345,750],[945,685],[845,655],
                    [880,660],[25,230],[525,1000],[580,1175],[650,1130],[1605,620],
                    [1220,580],[1465,200],[1530,5],[845,680],[725,370],[145,665],
                    [415,635],[510,875],[560,365],[300,465],[520,585],[480,415],
                    [835,625],[975,580],[1215,245],[1320,315],[1250,400],[660,180],
                    [410,250],[420,555],[575,665],[1150,1160],[700,580],[685,595],
                    [685,610],[770,610],[795,645],[720,635],[760,650],[475,960],
                    [95,260],[875,920],[700,500],[555,815],[830,485],[1170,65],
                    [830,610],[605,625],[595,360],[1340,725],[1740,245]
                   ]
        self.TSPLIB = berlin52
    def teardown_method(self):
        self.Vector = []
    def test_RandomSearch(self):
        from StochasticAlgorithms.randomSearch import randomSearch
        # Problem Configuration
        searchVector = [-5,5]
        size = 2
        # Algorithm Configuration
        iterations = 10000
        # Execute the random search algorithm
        # Outputs a tuple containing the best cost and best input values
        result = randomSearch(searchVector, iterations, size)
        basin = BasinResult('Random Search')
        print(basin.FormattedOutput(result))
    def test_AdaptiveRandomSearch(self):
        from StochasticAlgorithms.adaptiveRandomSearch import adaptiveRandomsearch
        # Problem Configuration
        searchVector = [-5,5]
        size = 2
        # Algorithm Configuration
        maxIterations = 10000
        initFactor =0.05
        lFactor =3.0
        sFactor =1.3
        iterFactor =10
        maxNoChange =25
        # Execute the adaptive random search algorithm
        # Outputs a tuple containing the best cost and best input values
        result = adaptiveRandomsearch(maxIterations, size, searchVector, initFactor, sFactor, lFactor, iterFactor, maxNoChange)
        basin = BasinResult('Adaptive Random Search')
        print(basin.FormattedOutput(result))
    def test_StochasticHillClimbingSearch(self):
        from StochasticAlgorithms.stochasticHillClimbing import stochasticHillClimbingSearch
        # Problem Configuration
        numBits = 64
        # Algorithm Configuration
        maxIterations = 1000
        # Execute the SHC algorithm
        result = stochasticHillClimbingSearch(numBits, maxIterations)
        print('Stochastic Hill Climbing Search Results : ')
        print('*' * 20)
        print('SHC Iteration ')
        print('*' * 20)
        print(result["iteration"])
        print('*' * 20)
        print('*' * 20)
        print('Initial One Max Count')
        print('*' * 20)
        print(result["initialCost"])
        print('*' * 20)
        print('Final One Max Count')
        print('*' * 20)
        print(result["cost"])
        print('*' * 20)
        print('*' * 20)
        print('*' * 20)
        print('Search FormattedOutput : (Final- Initial)/Iteration')
        print('*' * 20)
        efficacy = round(float(result["cost"] - result["initialCost"])/float(result["iteration"]),2)
        print(efficacy)
    def test_ScatterSearch(self):
        from StochasticAlgorithms.scatterSearch import scatterSearch
        # Problem Configuration
        searchVector = [-5,5]
        problemSize = 2
        # Algorithm Configuration
        maxIterations = 100
        stepSize = (searchVector[1]-searchVector[0]) * 0.05  # 5 percent of search space
        maxNoImprove =30
        refSetSize = 10
        diverseSetSize =20
        eliteCount = 5
        # execute the algorithm
        result = scatterSearch(searchVector, problemSize, refSetSize, diverseSetSize, maxIterations, maxNoImprove, eliteCount, stepSize)
        basin = BasinResult("Scatter Search")
        print(basin.FormattedOutput(result))
    #@unittest.skip("Don't run FOR NOW!")
    def test_IteratedLocalSearch(self):
        from StochasticAlgorithms.iteratedLocalSearch import iteratedLocalSearch
        # Problem Configuration
        # Use Berlin52 instance of TSPLIB
        # Algorithm Configuration
        maxIterations = 100
        maxNoImprove = 50
        searchHistoryToKeep =1 # since we don't plan to use it now
        # Execute the Algorithm
        result = iteratedLocalSearch(self.TSPLIB, maxIterations, maxNoImprove,searchHistoryToKeep)
        tspResult = TSPResult(7542,'Iterated Local Search Results')
        print(tspResult.FormattedOutput(result))
    #@unittest.skip("Don't run FOR NOW!")
    def test_VariableNeighborhoodSearch(self):
        from StochasticAlgorithms.variableNeighborhoodSearch import variableNeighborhoodSearch
        # Problem Configuration
        # Use Berlin52 instance of TSPLIB
        # Algorithm Configuration
        maxNoImprove =50
        maxNoImproveLocal =70
        neighborhoods = range(1,21) # since we want 20 runs for neighborhood starting with 1
        # Execute the algorithm
        result = variableNeighborhoodSearch(self.TSPLIB,neighborhoods, maxNoImprove, maxNoImproveLocal)
        tspResult = TSPResult(7542,'Variable Neighborhood Search Results')
        print(tspResult.FormattedOutput(result))
    #@unittest.skip("Don't run FOR NOW!")
    def test_GreedyRandomizedAdaptiveSearch(self):
        from StochasticAlgorithms.greedyRandomizedAdaptiveSearch import greedyRandomizedAdaptiveSearch
        # Problem Configuration
        # Use Berlin52 instance of TSPLIB
        # Algorithm Configuration
        maxNoImprove =50
        maxIterations =50
        greedinessFactor =0.3 # should be in the range [0,1]. 0 is more greedy and 1 is more generalized
        # Execute the algorithm
        result = greedyRandomizedAdaptiveSearch(self.TSPLIB,maxIterations, maxNoImprove, greedinessFactor)
        tspResult = TSPResult(7542,'Greedy Randomized Adaptive Search Results')
        print(tspResult.FormattedOutput(result))
    def test_TabuSearch(self):
        from StochasticAlgorithms.tabuSearch import tabuSearch
        # Problem Configuration
        # Use Berlin52 instance of TSPLIB
        # Algorithm Configuration
        maxIterations = 100
        maxTabuCount = 15
        maxCandidates = 50
        # Execute the algorithm
        result = tabuSearch(self.TSPLIB,maxIterations, maxTabuCount, maxCandidates)
        tspResult = TSPResult(7542,'Tabu Search Results')
        print(tspResult.FormattedOutput(result))
    def test_GuidedLocalSearch(self):
        from StochasticAlgorithms.guidedLocalSearch import guidedLocalSearch
        # Problem Configuration
        # Use Berlin52 instance of TSPLIB
        # Algorithm Configuration
        maxIterations = 150
        maxNoImprove = 20
        localSearchOptima = 12000.0
        alpha =0.3
        scalingFactor = alpha * (localSearchOptima/float(len(self.TSPLIB)))
        # Execute the algorithm
        result = guidedLocalSearch(self.TSPLIB, maxIterations, maxNoImprove, scalingFactor)
        tspResult = TSPResult(7542,'Guided Local Search Results')
        print(tspResult.FormattedOutput(result))
    def test_ReactiveTabuSearch(self):
        from StochasticAlgorithms.reactiveTabuSearch import reactiveTabuSearch
        # Problem Configuration
        # Use Berlin52 instance of TSPLIB
        # Algorithm Configuration
        maxIterations =100
        maxCandidates =50
        increase =1.3
        decrease =0.9
        #Execute the algorithm
        result = reactiveTabuSearch(self.TSPLIB, maxIterations, increase, decrease, maxCandidates)
        tspResult = TSPResult(7542,'Reactive Tabu Search')
        print(tspResult.FormattedOutput(result))
