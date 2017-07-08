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