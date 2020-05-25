import random

class Graph():
    def __init__(self, distance_matrix, city_count):
        self.distance_matrix = distance_matrix
        self.city_count = city_count
        self.pheromone = [[1 / (city_count ** 2) for j in range(city_count)] for i in range(city_count)]

class Ant():
    def __init__(self, aco, graph):
        self.aco = aco
        self.graph = graph
        self.total_cost = 0.0
        self.tabu = []
        self.pheromone_delta = []
        self.eta = [[0 if i == j else 1 / graph.distance_matrix[i][j] for j in range(graph.city_count)] for i in range(graph.city_count)]
        start = random.choice(range(graph.city_count))
        self.allowed = [i for i in range(graph.city_count)]
        self.allowed.remove(start)
        self.tabu.append(start)
        self.current = start

    def edgeSelection(self):
        denominator = 0
        for i in self.allowed:
            denominator += self.graph.pheromone[self.current][i] ** self.aco.alpha * self.eta[self.current][i] ** self.aco.beta
        # probabilities for moving to a node in the next step
        probabilities = [0 for i in range(self.graph.city_count)]
        for i in range(self.graph.city_count):
            try:
                self.allowed.index(i)
                probabilities[i] = (self.graph.pheromone[self.current][i] ** self.aco.alpha * self.eta[self.current][i] ** self.aco.beta) / denominator
            except ValueError:
                # list(allowed) does not contain i
                pass
        # roulette selection for next node
        select = 0
        rand = random.random()
        for i, probability in enumerate(probabilities):
            rand -= probability
            if rand <= 0:
                select = i
                break          
        self.allowed.remove(select)
        self.tabu.append(select)
        self.total_cost += self.graph.distance_matrix[self.current][select]
        self.current = select
        
       
    def pheromoneUpdateDelta(self):
        self.pheromone_delta = [[0 for j in range(self.graph.city_count)] for i in range(self.graph.city_count)]            
        for visit in range(len(self.tabu)-1):
            i = self.tabu[visit]
            j = self.tabu[visit+1]
            self.pheromone_delta[i][j] = self.aco.pheromone_intensity / self.graph.distance_matrix[i][j]

    
class AntColony():
    def __init__(self, ant_count, generations, alpha, beta, pheromone_residual_coefficient, pheromone_intensity):
        self.ant_count = ant_count
        self.generations = generations
        self.alpha = alpha
        self.beta = beta
        self.pheromone_residual_coefficient = pheromone_residual_coefficient
        self.pheromone_intensity = pheromone_intensity
        
    def pheromoneUpdate(self, graph, ants):
        for i, row in enumerate(graph.pheromone):
            for j in range(len(row)):
                graph.pheromone[i][j] *= self.pheromone_residual_coefficient
                for ant in ants:
                    graph.pheromone[i][j] += ant.pheromone_delta[i][j]
                    
    def solve(self, graph):
        best_cost = float('inf')
        best_solution, best_costs = [], []
        for generation in range(self.generations):
            ants = [Ant(self, graph) for i in range(self.ant_count)]
            for ant in ants:
                # generate solutions
                for i in range(graph.city_count-1):
                    ant.edgeSelection()
                # daemon actions
                ant.total_cost += graph.distance_matrix[ant.tabu[-1]][ant.tabu[0]]
                if ant.total_cost < best_cost:
                    best_cost = ant.total_cost
                    best_solution = list(ant.tabu)
                ant.pheromoneUpdateDelta()
            # update pheromone
            self.pheromoneUpdate(graph, ants)
            best_costs.append(best_cost)
        return best_cost, best_costs, best_solution
            
class AntColonySystem():
    def __init__(self):
        pass
    
    def pheromoneUpdate(self):
        pass
    
    def solve(self):
        pass
        

class MaxMinAntColony():
    def __init__(self):
        pass
    
    def pheromoneUpdate(self):
        pass
    
    def solve(self):
        pass