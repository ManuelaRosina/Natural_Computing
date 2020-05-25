from input_tsp.handle_coords import readCoords
from swarm_intelligence.aco import Graph, AntColony, AntColonySystem, MaxMinAntColony
import matplotlib.pyplot as plt
import os
import math

def outputFig(filename = 'x', foldername = 'output', extension = '.png'):
    plt.savefig(os.path.join(os.path.dirname(os.path.realpath('__file__')), foldername, filename+extension)) 

def showScatterplot(df, output_fig=False):
    plt.scatter(df.x, df.y, color='black', alpha=0.002)
    plt.title('Coordinates')
    if output_fig:
        outputFig('scatter_coords')
    plt.show()
    plt.close()

def initDistanceMatrix(points, city_count):
    distance_matrix = []
    for i in range(city_count):
        row = []
        for j in range(city_count):
            row.append(calcEuclideanDistance(points[i], points[j]))
        distance_matrix.append(row)
    return distance_matrix
     
def calcEuclideanDistance(a, b):
    return math.sqrt(sum([(a_ - b_) ** 2 for a_, b_ in zip(a, b)]))
   
def main():
    coords = readCoords(50) # load all data points by default
    city_count = len(coords)
    points = [(float(node['x']), float(node['y'])) for node in coords]
    distance_matrix = initDistanceMatrix(points, city_count)
    ant_count = 10
    generations = 100
    alpha=1
    beta=10
    pheromone_residual_coefficient=0.5
    pheromone_intensity=10
    aco = AntColony(ant_count, generations, alpha, beta, pheromone_residual_coefficient, pheromone_intensity)
    graph = Graph(distance_matrix, city_count)
    best_cost, best_costs, best_solution = aco.solve(graph)
    print(('='*8+'\n'+'Best cost found:'.ljust(20)+'{0}\n'
          + 'Lowest costs found:\n'+' '*4
          +'{1}\nBest solution found:\n'+' '*4+'{2}\n'+'='*8).format(best_cost, best_costs, best_solution))
    
if __name__ == '__main__':
    main()