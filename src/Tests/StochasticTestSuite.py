from ResultHelpers import TSPResult, BasinResult
class runTests:
    def __init__(self):
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
    def testRandomSearch(self):
        from StochasticAlgorithms.randomsearch import randomSearch
        # Problem Configuration
        searchVector = [-5,5]
        problem_size = 2
        # Algorithm Configuration
        max_iter = 10000
        # Execute the random search algorithm
        # Outputs a tuple containing the best cost and best input values
        # search_space = []
        # for i in range(0,problem_size):
        #     search_space.append(searchVector)
        result = randomSearch(searchVector,max_iter,problem_size)
        basin = BasinResult("Random Search")
        print(basin.FormattedOutput(result))
        # print("Done. Best Solution: Cost = "+str(result["cost"])+", Vector = "+str(result["vector"]))
    def testAdaptiveRandomSearch(self):
        from StochasticAlgorithms.adaptiveRandomSearch import adaptiveRandomSearch
        # Problem Configuration
        searchVector = [-5,5]
        problem_size = 2
        # Algorithm Configuration
        max_iter = 10000
        initFactor =0.05
        lFactor =3.0
        sFactor =1.3
        iterFactor =10
        maxNoChange =25
        # Execute the adaptive random search algorithm
        # Outputs a tuple containing the best cost and best input values
        result = adaptiveRandomSearch(searchVector,max_iter,problem_size,initFactor,lFactor,sFactor,iterFactor,maxNoChange)
        basin = BasinResult("Adaptive Random Search")
        print(basin.FormattedOutput(result))
    def testStochasticHillClimbingSearch(self):
        from StochasticAlgorithms.stochasticHillClimbing import stochasticHillClimbing
        # Problem Configuration
        numBits = 64
        # Algorithm Configuration
        maxIterations = 1000
        # Execute the SHC algorithm
        result = stochasticHillClimbing(numBits, maxIterations)
        print('Stochastic Hill Climbing Search Results : ')
        print('*' * 20)
        print('Stochastic Hill Climbing Iteration ')
        print('*' * 20)
        print(result['iteration'])
        print('*' * 20)
        print('*' * 20)
        print('Initial One Max Count')
        print('*' * 20)
        print(result['initialCost'])
        print('*' * 20)
        print('Final One Max Count')
        print('*' * 20)
        print(result['cost'])
        print('*' * 20)
        print('*' * 20)
        print('*' * 20)
        print('Search FormattedOutput : (Final- Initial)/Iteration')
        print('*' * 20)
        efficacy = float(result['cost'] - result['initialCost'])/float(result['iteration'])
        # print("%.2f" % round(efficacy,2))
        print("{:.2f}".format(round(efficacy,2)))
    def testIteratedLocalSearch(self):
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
