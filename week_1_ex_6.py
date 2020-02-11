import numpy as np
import random
import math
import matplotlib.pyplot as plt

cities = [x for x in range(1,9)]
# random city positions
city_positions = [[random.randint(0,100), random.randint(0,100)] for x in cities]

# number of iterations to run the algorithms
runs = 1000

pop_size = 5

def fitness(candidate):
    # claculate the distance of all neighbouring cities and add them
    dist = 0
    for i in range(len(candidate)-1):
        c = candidate[i]
        pos_c = city_positions[c-1]
        c2 = candidate[i+1]
        pos_c2 = city_positions[c2-1]
        dist += math.hypot(pos_c2[0] - pos_c[0], pos_c2[1] - pos_c[1])
    return dist

def select_parents(population, nr_of_parents = 2):
    """select parents using tournament selection"""
    candidates = random.sample(population, k=min((nr_of_parents*2), len(population)))
    return evaluate(candidates, nr_of_parents)

def evaluate(candidates, nr_of_parents = 2):
    fit_eval = []
    for i in range(len(candidates)):
        fit_eval.append((fitness(candidates[i]),i))
    fit_eval.sort(key=lambda t:t[0])
    #print(fit_eval)
    return [candidates[fit_eval[x][1]] for x in range(min(nr_of_parents,len(candidates)))], fit_eval[3][1], fit_eval[0][1]

def local_search(population):
    new_population = []
    for candidate in population:
        best_distance = fitness(candidate)
        improved = True
        while improved:
            improved = False
            for i in range(1,len(candidate)-2):
                for j in range(i+1, len(candidate)):
                    if i != j:
                        new_candidate = candidate
                        new_candidate[i:j] = candidate[j-1:i-1:-1]
                        if fitness(new_candidate) < best_distance:
                            candidate = new_candidate
                            best_distance = fitness(new_candidate)
                            improved = True
        new_population.append(candidate)
    return new_population

def get_child(parent1, parent2):
    cutpoint2 = random.randint(1,len(parent2)-1)
    cutpoint1 = random.randint(0,cutpoint2-1)
    #cutme = parent1[cutpoint1:cutpoint2]
    child = [0 for x in range(len(parent2))]
    for i in range(cutpoint1,cutpoint2):
        child[i] = parent1[i]
    j = cutpoint2
    for i in range(cutpoint2,len(parent2)):
        while parent2[j] in child:
            j = (j+1)%len(parent2)
        child[i] = parent2[j]
        j = (j+1)%len(parent2)

    for i in range(0,cutpoint1):
        while parent2[j] in child:
            j = (j+1)%len(parent2)
        child[i] = parent2[j]
        j = (j+1)%len(parent2)
    return child

def mutation(child):
    a,j = random.randint(0,len(child)-1), random.randint(0,len(child)-1)
    tmp = child[a]
    child[a] = child[j]
    child[j] = tmp
    return child

def plot_result(candidate, caption=''):
    xpos_order = []
    ypos_order = []
    for c in candidate:
        xpos_order.append(city_positions[c-1][0])
        ypos_order.append(city_positions[c - 1][1])
    plt.plot(xpos_order,ypos_order,'o-')
    plt.title(caption)
    plt.show()

def ea(candidates):
    for i in range(0, runs):
        parents, index_worst, best_index = select_parents(candidates)
        #print(parents)
        child = get_child(parents[0], parents[1])
        child = mutation(child)
        parents, index_worst, best_index = evaluate(candidates)
        candidates[index_worst] = child
        #print(child)
        #print(candidates)
        #print()
    parents, index_worst, best_index = evaluate(candidates)
    plot_result(candidates[best_index], "EA best solution")
    print("EA: " + str(fitness(candidates[best_index])))

def memetic(candidates):
    candidates = local_search(candidates)
    for i in range(0, runs):
        parents, index_worst, best_index = select_parents(candidates, 5)
        for i,p1 in enumerate(parents):
            for j, p2 in enumerate(parents):
                if i != j:
                    child = get_child(p1, p2)
                    child = mutation(child)
                    candidates.append(child)
        candidates = local_search(candidates)
        parents, index_worst, best_index = evaluate(candidates,pop_size)
        candidates = parents
        # print(candidates)
        # print()
    parents, index_worst, best_index = evaluate(candidates)
    plot_result(candidates[best_index], "memetic best")
    print("memetic best: " + str(fitness(candidates[best_index])))

def main():
    print(city_positions)

    # starting population:
    candidates = [np.random.permutation(cities) for x in range(0,pop_size)]
    print(candidates)
    parents, index_worst, best_index = evaluate(candidates)
    plot_result(candidates[best_index], "Initial best")
    print("initial best: "+ str(fitness(candidates[best_index])))
    ea(candidates)
    memetic(candidates)

if __name__ == "__main__":
    main()

