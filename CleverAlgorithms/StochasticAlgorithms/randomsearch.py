import random
def random_vector(min_max):
    b = []
    for i in range(0,len(min_max)):
        b.append(min_max[i][0] + ((min_max[i][1] - min_max[i][0]) * random.random()))
    return b
def objective_function(vector):
    sum = 0
    for i in vector:
        sum += i ** 2.00
    return sum
def search(search_space,max_iter):
    best = None
    for iter in range(0,max_iter):
        candidate = {}
        candidate['vector'] = random_vector(search_space)
        candidate['cost'] = objective_function(candidate['vector'])
        if best == None or candidate['cost'] < best['cost']:
            best = candidate
        print(' > iteration = ' + str(iter+1) + ', best = '+str(best["cost"]))
    return best
if __name__ == '__main__':
    problem_size = 2;
    search_space = []
    a = [-5,5]
    for i in range(0,problem_size):
        search_space.append(a)
    max_iter = 100
    best = search(search_space,max_iter)
    print("Done. Best Solution: Cost = "+str(best["cost"])+", Vector = "+str(best["vector"]))