import time
import random
def crossover(ind1,ind2,KNAPSACK_ITEMS,NUM_ITEMS,MAX_WEIGHT):
    '''crossover two individuals using single point crossover  method
    returns two new individuals'''
    # randomly select crossover point
    cop = random.randint(1,NUM_ITEMS-2)
    # create new individuals
    new_ind1 = ind1[0:cop] + ind2[cop:NUM_ITEMS]
    new_ind2 = ind2[0:cop] + ind1[cop:NUM_ITEMS]
    # make sure genomes are valid
    while fitness(new_ind1,KNAPSACK_ITEMS,NUM_ITEMS,MAX_WEIGHT) == 0:
        # set random '1' chromosome to 0 (i.e remove an item)
        ones = [i for i,x in enumerate(new_ind1) if x==1]
        new_ind1[random.choice(ones)] = 0
    while fitness(new_ind2,KNAPSACK_ITEMS,NUM_ITEMS,MAX_WEIGHT) == 0:
        # set random '1' chromosome to 0 (i.e remove an item)
        ones = [i for i,x in enumerate(new_ind2) if x==1]
        new_ind2[random.choice(ones)] = 0
    return new_ind1,new_ind2
def select(p,KNAPSACK_ITEMS,NUM_ITEMS,MAX_WEIGHT):
    '''select individual based on tournament returns fittest of randomly selected individuals'''
    # sample two individuals
    ind1,ind2 = random.sample(p,2)
    # return the fitter one
    if fitness(ind1,KNAPSACK_ITEMS,NUM_ITEMS,MAX_WEIGHT) > fitness(ind2,KNAPSACK_ITEMS,NUM_ITEMS,MAX_WEIGHT):
        return ind1
    else:
        return ind2
def mutate(ind,KNAPSACK_ITEMS,NUM_ITEMS,MAX_WEIGHT):
    '''mutate individual by inverting a randomly selected chromosome '''
    chrom = random.randint(0,NUM_ITEMS - 1)
    ind[chrom] = int(not ind[chrom])
    # makesure the genome is valid
    while fitness(ind,KNAPSACK_ITEMS,NUM_ITEMS,MAX_WEIGHT) == 0:
        # set random '1' chromosome to 0 (i.e remove an item)
        ones = [i for i,x in enumerate(ind) if x==1]
        ind[random.choice(ones)] = 0
    return ind
def evolve(p,KNAPSACK_ITEMS,POPULATION_SIZE,ELITISM_PERC,CROSSOVER_PROB,MUTATION_PROB,NUM_ITEMS,MAX_WEIGHT):
    '''create next generation population by using selection crossover and mutations
    returns new population'''
    # calculate how many elitist we want to select
    elite_elements = POPULATION_SIZE * ELITISM_PERC / 100.0
    # get crossover probability as float
    crossover_float = CROSSOVER_PROB / 100.0
    # get mutation probability as float
    mutation_float = MUTATION_PROB / 100.0
    # sort population by fitness
    sorted_p = [ind for fitn,ind in reversed(sorted([(fitness(ind,KNAPSACK_ITEMS,NUM_ITEMS,MAX_WEIGHT),ind) for ind in p]))]
    new_population = []
    for i in xrange(POPULATION_SIZE/2):
        # Selection
        # A number of elite elements are selected from elite population
        if i < elite_elements:
            mother = sorted_p[i]
            father = sorted_p[i+1]
        # parents are selected
        else:
            mother = select(p,KNAPSACK_ITEMS,NUM_ITEMS,MAX_WEIGHT)
            father = select(p,KNAPSACK_ITEMS,NUM_ITEMS,MAX_WEIGHT)
        # crossover
        # crossover with likelihood of crossover probability
        if random.random() < crossover_float:
            child1,child2 = crossover(mother,father,KNAPSACK_ITEMS,NUM_ITEMS,MAX_WEIGHT)
        # otherwise select mother and father for new generation
        else:
            child1 = mother
            child2 = father
        # mutation
        # mutate first child with likelihood of mutation probability
        if random.random() < mutation_float:
            child1=mutate(child1,KNAPSACK_ITEMS,NUM_ITEMS,MAX_WEIGHT)
        # mutate second child with likelihood of mutation probability
        if random.random() < mutation_float:
            child2=mutate(child2,KNAPSACK_ITEMS,NUM_ITEMS,MAX_WEIGHT)
        new_population.append(child1)
        new_population.append(child2)
    return new_population
def get_fittest(p,KNAPSACK_ITEMS,NUM_ITEMS,MAX_WEIGHT):
    # returns the fittest individual and its fitness
    best_fitness,fittest_ind = max([(fitness(ind,KNAPSACK_ITEMS,NUM_ITEMS,MAX_WEIGHT),ind) for ind in p])
    return fittest_ind,best_fitness
def fitness(ind,KNAPSACK_ITEMS,NUM_ITEMS,MAX_WEIGHT):
    ''' returns fitness of individual
    0 if weight of all items in knapsack is higher than allowed max weight'''
    fitness = 0
    knap_weight = 0
    for i,item in enumerate(KNAPSACK_ITEMS[:NUM_ITEMS]):
        # is item included
        if ind[i] == 1:
            value,weight = item[2],item[1] # unpack the tuple
            fitness += value
            knap_weight += weight
    # is weight greater than allowed limit if true return fitness of 0
    if knap_weight > MAX_WEIGHT:
        return 0
    return fitness
def validate_population(p,KNAPSACK_ITEMS,NUM_ITEMS,MAX_WEIGHT):
    '''validate population by calculating each individuals fitness and adjusting it if needed'''
    for ind in p:
        while fitness(ind,KNAPSACK_ITEMS,NUM_ITEMS,MAX_WEIGHT) == 0:
            # set random '1' chromosome to 0 (i.e remove an item)
            ones = [i for i,x in enumerate(ind) if x==1]
            ind[random.choice(ones)] = 0
    return p
def knapsackSolverGeneticAlgorithm(KNAPSACK_ITEMS,MAX_WEIGHT,NUM_ITEMS,POPULATION_SIZE,ELITISM_PERC,CROSSOVER_PROB,MUTATION_PROB,MAX_STABLE,MAX_GENERATIONS):
    # generate population
    population = [[random.choice((0,1)) for i in xrange(NUM_ITEMS)] for j in xrange(POPULATION_SIZE)]
    # validate population
    population = validate_population(population,KNAPSACK_ITEMS,NUM_ITEMS,MAX_WEIGHT)
    # get fittest individual so far
    best_solution,best_fitness = get_fittest(population,KNAPSACK_ITEMS,NUM_ITEMS,MAX_WEIGHT)
    # start time
    start_time = time.time()
    stable_cnt = 0 # count stable iterations
    generation_cnt = 1 # count generations
    while True:
        # create new population by using mutation,crossover and selection
        population = evolve(population,KNAPSACK_ITEMS,POPULATION_SIZE,ELITISM_PERC,CROSSOVER_PROB,MUTATION_PROB,NUM_ITEMS,MAX_WEIGHT)
        generation_cnt += 1
        # get fittest individual
        ind,fitness = get_fittest(population,KNAPSACK_ITEMS,NUM_ITEMS,MAX_WEIGHT)
        if fitness > best_fitness:
            # if a better solution is found
            best_solution = ind
            best_fitness = fitness
            stable_cnt = 0
        else:
            stable_cnt += 1
        # check termination conditions
        if stable_cnt >= MAX_STABLE:
            # solution has not improved for max stable generations then quit
            break
        if generation_cnt >= MAX_GENERATIONS:
            # if we reach max number of generations then quit
            break
    end_time = time.time()
    # print('Solution found in generation %s' % generation_cnt)
    bagged_items=[]
    total_weight = 0
    total_value = 0
    for i in range(0,len(best_solution)):
        if best_solution[i] == 1:
            bagged_items.append(KNAPSACK_ITEMS[i])
            total_value += KNAPSACK_ITEMS[i][2]
            total_weight += KNAPSACK_ITEMS[i][1]
    # print('Fitness : %s'% best_fitness)
    total_time = time.strftime('%Mm %Ss',time.gmtime(end_time-start_time))
    # return the results
    return (bagged_items,total_value,total_weight,total_time)
