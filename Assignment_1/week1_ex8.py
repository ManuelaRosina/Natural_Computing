# libraries
import operator
import math
import numpy as np
import matplotlib.pyplot as plt
from deap import algorithms, base, creator, tools, gp

def getDiv(a, b):
    try:
        return math.truediv(a, b)
    except:
        return 100

def getLog(a):
    try:
        return math.log(a)
    except:
        return -1
    
def getExp(a):
	try:
		return math.exp(a)
	except:
		return -1
	
# eval individual
def evalSymbReg(individual):
	x = [-1.0, -0.9, -0.8, -0.7, -0.6, -0.5, -0.4, -0.3, -0.2, -0.1, 0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
	y = [0, -0.1629, -0.2624, -0.3129, -0.3264, -0.3125, -0.2784, -0.2289, -0.1664, -0.0909, 0, 0.1111, 0.2496, 0.4251, 0.6496, 0.9375, 1.3056, 1.7731, 2.3616, 3.0951, 4.000]
	func = toolbox.compile(expr = individual)
	abs_err = (np.abs(func(x[i]) - y[i]) for i in range(20))
	return math.fsum(abs_err)/21,

pset = gp.PrimitiveSet("MAIN", 1)
# function set
pset.addPrimitive(operator.add, 2)
pset.addPrimitive(operator.sub, 2)
pset.addPrimitive(operator.mul, 2)
pset.addPrimitive(getDiv, 2)
pset.addPrimitive(getLog, 1)
pset.addPrimitive(getExp, 1)
pset.addPrimitive(math.cos, 1)
pset.addPrimitive(math.sin, 1)
# terminal set
pset.renameArguments(ARG0='x')

# macro handling
creator.create("FitnessMin", base.Fitness, weights = (-1.0,))
creator.create("Individual", gp.PrimitiveTree, fitness = creator.FitnessMin)
toolbox = base.Toolbox()
toolbox.register("expr", gp.genFull, pset = pset, min_ = 1, max_ = 3)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("compile", gp.compile, pset = pset)
toolbox.register("evaluate", evalSymbReg)
toolbox.register("select", tools.selTournament, tournsize = 5)
toolbox.register("mate", gp.cxOnePoint)
toolbox.decorate("mate", gp.staticLimit(key=operator.attrgetter("height"), max_value=17))
toolbox.register("expr_mut", gp.genFull, min_ = 0, max_ = 2)
toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut, pset=pset)
toolbox.decorate("mutate", gp.staticLimit(key=operator.attrgetter("height"), max_value=17))

def main():
    crossp = 0.7
    population = toolbox.population(n = 1000)
    fitness = np.zeros((51, 1))
    size= np.zeros((51, 1))
    generations = np.linspace(1, 50, 50)
    hof = tools.HallOfFame(1)
    hof.update(population)
	
    # GP
    for gen in range(51):
        # update hall of fame
        hof.remove(0)
        hof.update(population)
        fitness[gen] = evalSymbReg(hof[0])
        size[gen] = len(hof[0])
        # handle offspring
        offspring = toolbox.select(population, 1000)
        offspring = algorithms.varAnd(offspring, toolbox, crossp, 0)
        		
        # eval offsprint
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fits = toolbox.map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fits):
            ind.fitness.values = fit
        population = offspring
	
    # best of generation fitness (y-axis) versus generation (x-axis)
    plt.figure(111)
    plt.plot(generations, fitness[1:51])
    plt.xlabel('Generation')
    plt.ylabel('Fitness of best individual')
    
    # best of generation size (y-axis) versus generation (x-axis)
    plt.figure(222)
    plt.plot(generations, size[1:51])
    plt.xlabel('Generation')
    plt.ylabel('Size of best individual')
    
    plt.show()

if __name__ == "__main__":
    main()