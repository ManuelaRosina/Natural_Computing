import random
import math

class Graph():
    def __init__(self, coords):
        self.points=[(float(node['x']), float(node['y'])) for node in coords]
        self.city_count = len(self.points)
        self.distance_matrix = self.initDistanceMatrix(self.points, self.city_count)
        self.initial_pheromone = 1 / (self.city_count ** 2)
        self.pheromone = [[self.initial_pheromone for j in range(self.city_count)] for i in range(self.city_count)]
        
    def initDistanceMatrix(self, points, city_count):
        distance_matrix = []
        for i in range(city_count):
            row = []
            for j in range(city_count):
                row.append(self.calcEuclideanDistance(points[i], points[j]))
            distance_matrix.append(row)
        return distance_matrix
         
    def calcRouteCost(self, route: list):
        ttl_distance = 0
        for i in range(len(route)-2):
            ttl_distance += self.distance_matrix[route[i]][route[i+1]]
        return ttl_distance
        
    def calcEuclideanDistance(self, a, b):
        return math.sqrt(sum([(a_ - b_) ** 2 for a_, b_ in zip(a, b)]))
    
    def resetPheromoneLevel(self):
        self.pheromone = [[self.initial_pheromone for j in range(self.city_count)] for i in range(self.city_count)]

class Ant():
    def __init__(self, aco, graph: Graph):
        self.graph = graph
        self.aco = aco
        self.total_cost = 0.0
        self.tabu = []
        self.pheromone_delta = []
        self.eta = [[0 if i == j else 1 / graph.distance_matrix[i][j] for j in range(graph.city_count)] for i in range(graph.city_count)]
        start = random.choice(range(graph.city_count))
        self.allowed = [i for i in range(graph.city_count)]
        self.allowed.remove(start)
        self.tabu.append(start)
        self.current = start

    def pickNearest_k(self, k:int):
        return [i[0] for i in sorted([(i, j) for i, j in enumerate(self.graph.distance_matrix[self.current]) if i not in self.tabu and i in self.allowed], key=lambda x: x[1])[:k]]
          
    def edgeSelection(self, q_0=-1):
        denominator = 0
        available = self.pickNearest_k(int(self.graph.city_count*0.1))
        for i in available:
            denominator += self.graph.pheromone[self.current][i] ** self.aco.alpha * self.eta[self.current][i] ** self.aco.beta
        # probabilities for moving to a node in the next step
        probabilities = [0 for i in range(self.graph.city_count)]
        for i in range(self.graph.city_count):
            try:
                available.index(i)
                probabilities[i] = (self.graph.pheromone[self.current][i] ** self.aco.alpha * self.eta[self.current][i] ** self.aco.beta) / denominator
            except ValueError:
                # list(allowed) does not contain i
                pass            
        if random.random()<q_0:
            select=max([(node, self.graph.pheromone[self.current][node]* self.eta[self.current][node]) for node in available], key=lambda x: x[1])[0]
        else:
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
            self.pheromone_delta[i][j] = 1 / self.total_cost

    def localSearch(self, trials=10):
        while trials>0:
            random_vals = (random.randint(0, self.graph.city_count-1), random.randint(0, self.graph.city_count-1))
            while random_vals[0]==random_vals[1]:
                random_vals = (random.randint(0, self.graph.city_count-1), random.randint(0, self.graph.city_count-1))
            i, j = min(random_vals[0], random_vals[1]), max(random_vals[0], random_vals[1]) 
            adjacent_cost = self.graph.calcRouteCost(list(self.tabu)[:i]+list(reversed(list(self.tabu)[i:j]))+list(self.tabu)[j:])  
            if adjacent_cost < self.total_cost:
                self.total_cost=adjacent_cost
                self.tabu=list(self.tabu)[:i]+list(reversed(list(self.tabu[i:j])))+list(self.tabu)[j:]
            else:
                trials-=1
    
class AntSystem():
    def __init__(self, ant_count, generations, alpha, beta, ro):
        self.ant_count = ant_count
        self.generations = generations
        self.alpha = alpha
        self.beta = beta
        self.ro = ro
        
    def pheromoneUpdate(self, graph, ants):
        for i, row in enumerate(graph.pheromone):
            for j in range(len(row)):
                graph.pheromone[i][j] *= self.ro
                ttl_pheromone_delta = 0.0
                for ant in ants:
                    ttl_pheromone_delta += ant.pheromone_delta[i][j]
                graph.pheromone[i][j] += (1-self.ro)*ttl_pheromone_delta
                    
    def solve(self, graph):
        best_cost = float('inf')
        best_solution, best_costs, avg_costs = [], [], []
        for generation in range(self.generations):
            gen_costs = []
            ants = [Ant(self, graph) for i in range(self.ant_count)]
            for ant in ants:
                # generate solutions
                for i in range(graph.city_count-1):
                    ant.edgeSelection()
                # daemon actions
                ant.localSearch()
                ant.total_cost += graph.distance_matrix[ant.tabu[-1]][ant.tabu[0]]
                gen_costs.append(ant.total_cost)
                if ant.total_cost < best_cost:
                    best_cost = ant.total_cost
                    best_solution = list(ant.tabu)
                ant.pheromoneUpdateDelta()
            # update pheromone
            self.pheromoneUpdate(graph, ants)
            best_costs.append(best_cost)
            avg_costs.append(sum(gen_costs)/self.ant_count)
        return best_cost, best_costs, avg_costs, best_solution
    
class AntColonySystem():
    def __init__(self, ant_count: int, generations: int, alpha: float, beta: float, fi: float, ro: float, q_0: float):
        self.ant_count = ant_count
        self.generations = generations
        self.alpha = alpha
        self.beta = beta
        self.fi = fi
        self.ro = ro
        self.q_0 = q_0
        
    def pheromoneUpdateLocal(self, graph, ant):
        for row_index, row in enumerate(graph.pheromone):
            for column_index in range(len(row)):
                if {row_index,column_index} in [{list(ant.tabu)[_], list(ant.tabu)[_+1]} for _ in range(len(list(ant.tabu))-1)]:
                    graph.pheromone[row_index][column_index] *= self.fi
                    graph.pheromone[row_index][column_index] += (1-self.fi)*(graph.initial_pheromone)

        
    def pheromoneUpdateGlobal(self, graph, best_cost: float, best_solution: list):
        for row_index, row in enumerate(graph.pheromone):
            for column_index in range(len(row)):
                graph.pheromone[row_index][column_index] *= self.ro
                if {row_index, column_index} in [{best_solution[_], best_solution[_+1]} for _ in range(len(best_solution)-1)]:
                    best_pheromone_delta = 1/best_cost
                else:
                    best_pheromone_delta=0
                graph.pheromone[row_index][column_index] += (1-self.ro)*best_pheromone_delta
            
    def solve(self, graph):
        best_cost = float('inf')
        best_solution, best_costs, avg_costs = [], [], []
        for generation in range(self.generations):
            gen_costs = []
            ants = [Ant(self, graph) for i in range(self.ant_count)]
            for ant in ants:
                # generate solutions
                for i in range(graph.city_count-1):
                    ant.edgeSelection(self.q_0)
                # daemon actions
                ant.localSearch()
                ant.total_cost += graph.distance_matrix[ant.tabu[-1]][ant.tabu[0]]
                gen_costs.append(ant.total_cost)
                if ant.total_cost < best_cost:
                    best_cost = ant.total_cost
                    best_solution = list(ant.tabu)
                self.pheromoneUpdateLocal(graph, ant)
            # update pheromone
            self.pheromoneUpdateGlobal(graph, best_cost, best_solution)
            best_costs.append(best_cost)
            avg_costs.append(sum(gen_costs)/self.ant_count)
        return best_cost, best_costs, avg_costs, best_solution
    
class MinMaxAntSystem():
    def __init__(self, ant_count, generations, alpha, beta, ro):
        self.ant_count = ant_count
        self.generations = generations
        self.alpha = alpha
        self.beta = beta
        self.ro = ro
        
    def pheromoneUpdate(self, graph, best_cost: float, best_solution: list):
        for row_index, row in enumerate(graph.pheromone):
            for column_index in range(len(row)):
                graph.pheromone[row_index][column_index] *= self.ro
                # if edge in best solution
                if {row_index, column_index} in [{best_solution[_], best_solution[_+1]} for _ in range(len(best_solution)-1)]:
                    best_pheromone_delta = 1/best_cost
                else:
                    best_pheromone_delta=0
                graph.pheromone[row_index][column_index] += (1-self.ro)*best_pheromone_delta
                if graph.pheromone[row_index][column_index] > 1/graph.city_count:
                    graph.pheromone[row_index][column_index] = 1/graph.city_count 
                if graph.pheromone[row_index][column_index] < 1/(graph.city_count**2):
                    graph.pheromone[row_index][column_index] = 1/(graph.city_count**2)
 
    def solve(self, graph):
        best_cost = float('inf')
        best_solution, best_costs, avg_costs = [], [], []
        for generation in range(self.generations):
            gen_costs = []
            ants = [Ant(self, graph) for i in range(self.ant_count)]
            for ant in ants:
                # generate solutions
                for i in range(graph.city_count-1):
                    ant.edgeSelection()
                # daemon actions
                ant.localSearch()
                ant.total_cost += graph.distance_matrix[ant.tabu[-1]][ant.tabu[0]]
                gen_costs.append(ant.total_cost)
                if ant.total_cost < best_cost:
                    best_cost = ant.total_cost
                    best_solution = list(ant.tabu) 
            # update pheromone
            self.pheromoneUpdate(graph, best_cost, best_solution)
            best_costs.append(best_cost)
            avg_costs.append(sum(gen_costs)/self.ant_count)
        return best_cost, best_costs, avg_costs, best_solution