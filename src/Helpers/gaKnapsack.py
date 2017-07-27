import random
import time
KNAPSACK_ITEMS =(("map",52,189),("compass",12,25),("water", 12, 133),("sandwich",167,422),("glucose", 150, 29)
        ,("tin", 280, 523),("banana", 19, 33),("apple", 35, 127),("cheese",125,340),("beer",29,43),
    ("suntan cream",63,47),("camera",17,52),("t-shirt",33,97),("trousers",45,101),("umbrella",53,108),
    ("waterproof trousers",33,7),("waterproof overclothes",180,550),("note-case",88,116),
    ("sunglasses",140,167),("towel",31,47),("socks",94,212),("book",5,13),("video-game",57,287),("mobile",60,320),("oxygen",350,27),
    ("tent",99,400),("watch",220,179),("first-aid",89,487),("knife",22,39),("torch",12,199),
    ("gas",23,39),("laptop",143,570))
MAX_WEIGHT = 1000
NUM_ITEMS = 32
POPULATION_SIZE = 100
ELITISM_PERC = 15
CROSSOVER_PROB = 55
MUTATION_PROB = 60
MAX_STABLE = 100
MAX_GENERATIONS = 200
def crossover(ind1,ind2):
    cop = random.randint(1,NUM_ITEMS-2)
    new_ind1 = ind1[0:cop] + ind2[cop:NUM_ITEMS]
    new_ind2 = ind2[0:cop] + ind1[cop:NUM_ITEMS]
    while fitness(new_ind1) == 0:
        ones = [i for i,x in enumerate(new_ind1) if x==1]
        new_ind1[random.choice(ones)] = 0
    while fitness(new_ind2) == 0:
        ones = [i for i,x in enumerate(new_ind2) if x==1]
        new_ind2[random.choice(ones)] = 0
    return new_ind1,new_ind2
def select(p):
    ind1,ind2 = random.sample(p,2)
    if fitness(ind1) > fitness(ind2):
        return ind1
    else:
        return ind2
def mutate(ind):
    chrom = random.randint(0,NUM_ITEMS - 1)
    ind[chrom] = int(not ind[chrom])
    while fitness(ind) == 0:
        ones = [i for i,x in enumerate(ind) if x==1]
        ind[random.choice(ones)] = 0
def evolve(p):
    elite_elements = POPULATION_SIZE * ELITISM_PERC / 100.0
    crossover_float = CROSSOVER_PROB / 100.0
    mutation_float = MUTATION_PROB / 100.0
    sorted_p = [ind for fitn,ind in reversed(sorted([(fitness(ind),ind) for ind in p]))]
    new_population = []
    for i in xrange(POPULATION_SIZE/2):
        if i < elite_elements:
            mother = sorted_p[i]
            father = sorted_p[i+1]
        else:
            mother = select(p)
            father = select(p)
        if random.random() < crossover_float:
            child1,child2 = crossover(mother,father)
        else:
            child1 = mother
            child2 = father
        if random.random() < mutation_float:
            mutate(child1)
        if random.random() < mutation_float:
            mutate(child2)
        new_population.append(child1)
        new_population.append(child2)
    return new_population
def get_fittest(p):
    best_fitness,fittest_ind = max([(fitness(ind),ind) for ind in p])
    return fittest_ind,best_fitness
def fitness(ind):
    fitness = 0
    knap_weight = 0
    for i,item in enumerate(KNAPSACK_ITEMS[:NUM_ITEMS]):
        if ind[i] == 1:
            value,weight = item[2],item[1]
            fitness += value
            knap_weight += weight
    if knap_weight > MAX_WEIGHT:
        return 0
    return fitness
def validate_population(p):
    for ind in p:
        while fitness(ind) == 0:
            ones = [i for i,x in enumerate(ind) if x==1]
            ind[random.choice(ones)] = 0
def zeroOneKnapsackSolverByGeneticAlgo():
    population = [[random.choice((0,1)) for i in xrange(NUM_ITEMS)] for j in xrange(POPULATION_SIZE)]
    validate_population(population)
    best_solution,best_fitness = get_fittest(population)
    start_time = time.time()
    stable_cnt = 0
    generation_cnt = 1
    while True:
        population = evolve(population)
        generation_cnt += 1
        ind,fitness = get_fittest(population)
        if fitness > best_fitness:
            best_solution = ind
            best_fitness = fitness
            stable_cnt = 0
        else:
            stable_cnt += 1
        if stable_cnt >= MAX_STABLE:
            break
        if generation_cnt >= MAX_GENERATIONS:
            break
    end_time = time.time()
    print('Solution found in generation %s' % generation_cnt)
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
    return (bagged_items,total_value,total_weight,total_time)
