import numpy as np
import random
import math
import matplotlib.pyplot as plt

def fitness(candidate, city_pos):
    dist = 0
    for i in range(len(candidate)-1):
        c = candidate[i]
        pos_c = city_pos[c-1]
        c2 = candidate[i+1]
        pos_c2 = city_pos[c2-1]
        dist += math.hypot(pos_c2[0] - pos_c[0], pos_c2[1] - pos_c[1])
    return dist

def select_parents(candidates):
    """parent1 = random.choice(candidates)
    parent2 = random.choice(candidates)
    while np.array_equal(parent1, parent2):
        parent2 = random.choice(candidates)"""
    fit_eval = []
    for i in range(len(candidates)):
        fit_eval.append((fitness(candidates[i],city_positions),i))
    fit_eval.sort(key=lambda t:t[0])
    print(fit_eval)
    return candidates[fit_eval[0][1]], candidates[fit_eval[1][1]], fit_eval[3][1], fit_eval[0][1]

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

def plot_result(candidate):
    xpos_order = []
    ypos_order = []
    for c in candidate:
        xpos_order.append(city_positions[c-1][0])
        ypos_order.append(city_positions[c - 1][1])
    plt.plot(xpos_order,ypos_order,'o-')
    plt.show()

cities = [1,2,3,4,5,6,7,8]
city_positions = [[random.randint(0,100), random.randint(0,100)] for x in cities]
print(city_positions)

# starting population:
candidates = [np.random.permutation(cities) for x in range(1,5)]
print(candidates)
for i in range(0,100):
    parent1, parent2, index_worst, best_index = select_parents(candidates)
    if i == 1:
        plot_result(candidates[best_index])
    parents = [parent1, parent2]
    #print(parents)
    child = get_child(parents[0], parents[1])
    child = mutation(child)
    candidates[index_worst] = child
    print(child)
    print(candidates)
    print()
plot_result(candidates[best_index])