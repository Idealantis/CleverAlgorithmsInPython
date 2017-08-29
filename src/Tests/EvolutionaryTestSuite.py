'''
Created on July 25, 2017

@author: Sai Panyam

Unit tests that exercise the algorithms. It is a mixture of both real 'unit' tests and functional tests of search
'''
class TestEvolutionaryAlgorithms:
    def test_01KnapsackDynamicProgram(self):
        from EvolutionaryAlgorithms.KnapSackSolver.knapsackDynamic import knapsackSolverDynamicProg
        # available items to choose from
        items =(("map",52,189),("compass",12,25),("water", 12, 133),("sandwich",167,422),("glucose", 150, 29)
        ,("tin", 280, 523),("banana", 19, 33),("apple", 35, 127),("cheese",125,340),("beer",29,43),
        ("suntan cream",63,47),("camera",17,52),("t-shirt",33,97),("trousers",45,101),("umbrella",53,108),
        ("waterproof trousers",33,7),("waterproof overclothes",180,550),("note-case",88,116),
        ("sunglasses",140,167),("towel",31,47),("socks",94,212),("book",5,13),("video-game",57,287),("mobile",60,320),("oxygen",350,27),
        ("tent",99,400),("watch",220,179),("first-aid",89,487),("knife",22,39),("torch",12,199),
        ("gas",23,39),("laptop",143,570))
        limit = 1000 # maximum weight of knapsack
        bagged = knapsackSolverDynamicProg(items,limit)
        print("-------------------------------------------------------------------------------")
        print("   0/1 Knapsack By Dynamic Programming  ")
        print("-------------------------------------------------------------------------------")
        print("Bagged the following items\n" +'\n'.join(sorted(item for item,_,_ in bagged[0])))
        print("For a total value of %i and a total weight of %i" % (bagged[2], bagged[1]))
        print("Solution found in %s"% bagged[3])
    def test_01KnapsackGeneticAlgorithm(self):
        from EvolutionaryAlgorithms.KnapSackSolver.knapsackGenetic import knapsackSolverGeneticAlgorithm
        KNAPSACK_ITEMS =(("map",52,189),("compass",12,25),("water", 12, 133),("sandwich",167,422),("glucose", 150, 29)
        ,("tin", 280, 523),("banana", 19, 33),("apple", 35, 127),("cheese",125,340),("beer",29,43),
        ("suntan cream",63,47),("camera",17,52),("t-shirt",33,97),("trousers",45,101),("umbrella",53,108),
        ("waterproof trousers",33,7),("waterproof overclothes",180,550),("note-case",88,116),
        ("sunglasses",140,167),("towel",31,47),("socks",94,212),("book",5,13),("video-game",57,287),("mobile",60,320),("oxygen",350,27),
        ("tent",99,400),("watch",220,179),("first-aid",89,487),("knife",22,39),("torch",12,199),
        ("gas",23,39),("laptop",143,570))
        MAX_WEIGHT = 1000 # max allowed weight
        NUM_ITEMS = 32 # number of items in Knapsack len(KNAPSACK_ITEMS)
        POPULATION_SIZE = 100 # number of individuals
        ELITISM_PERC = 30 # percentage of elite individuals selected for next generation
        CROSSOVER_PROB = 50 # crossover probability
        MUTATION_PROB = 60 # mutation probability
        MAX_STABLE = 150 # number of stable generations before we quit
        MAX_GENERATIONS = 200 # max number of generations for termination
        # call the function
        values = knapsackSolverGeneticAlgorithm(KNAPSACK_ITEMS,MAX_WEIGHT,NUM_ITEMS,POPULATION_SIZE,ELITISM_PERC,CROSSOVER_PROB,MUTATION_PROB,MAX_STABLE,MAX_GENERATIONS)
        print("-------------------------------------------------------------------------------")
        print("   0/1 Knapsack By Genetic Algorithm ")
        print("-------------------------------------------------------------------------------")
        print("Bagged the following items\n" +'\n'.join(sorted(item for item,_,_ in values[0])))
        print("For a total value of %i and a total weight of %i" % (values[1], values[2]))
        print("Solution found in %s"% values[3])
