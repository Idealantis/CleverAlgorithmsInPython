from ResultHelpers import TSPResult, BasinResult
class runTests:
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
        print basin.FormattedOutput(result)