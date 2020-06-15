from input_tsp.handle_coords import readCoords
from swarm_intelligence.aco import *
import matplotlib.pyplot as plt
import os
import numpy as np
import pandas as pd
import time
import operator
from datetime import datetime

def outputCsv(df, filename: str):
    output_path = os.path.join(os.path.dirname(os.path.realpath('__file__')), 'output_f', 'output_'+datetime.now().strftime('%m_%d'))
    if not os.path.exists(output_path):
        os.mkdir(output_path)
    df.to_csv(os.path.join(output_path, filename+'.csv'))   
   
def outputTxt(text: str, filename: str):
    output_path = os.path.join(os.path.dirname(os.path.realpath('__file__')), 'output_f', 'output_'+datetime.now().strftime('%m_%d'))
    if not os.path.exists(output_path):
        os.mkdir(output_path)
    with open(os.path.join(output_path, filename+'.txt'),"w") as file:
        file.write(text)  
        
def outputFig(filename: str):
    output_path = os.path.join(os.path.dirname(os.path.realpath('__file__')), 'output_f', 'output_'+datetime.now().strftime('%m_%d'))
    if not os.path.exists(output_path):
        os.mkdir(output_path)
    plt.savefig(os.path.join(output_path, filename+'.png')) 
    
def showScatterplot(df, output_fig=False):
    plt.scatter(df.x, df.y, color='black', alpha=0.002)
    plt.title('Coordinates')
    if output_fig:
        outputFig('scatter_coords')
    plt.show()
    plt.close()

def plotRoute(points, path: list):
    x = []
    y = []
    for point in points:
        x.append(point[0])
        y.append(point[1])
    # noinspection PyUnusedLocal
    y = list(map(operator.sub, [max(y) for i in range(len(points))], y))
    plt.plot(x, y, 'co')
    for city_index in range(1, len(path)):
        i = path[city_index- 1]
        j = path[city_index]
        plt.arrow(x[i], y[i], x[j] - x[i], y[j] - y[i], color='r', length_includes_head=True)
    plt.xlim(0, max(x) * 1.1)
    plt.ylim(0, max(y) * 1.1)
    plt.show()
    
def simplifyGraph(coords):
    points = [coord['x'] for coord in coords] + [coord['y'] for coord in coords]
    maximum, minimum = max(points), min(points)
    frames = 35
    virtual_view_unit = (maximum - minimum) / frames
    new_coordinates = []
    for coord in coords:
        if (
                coord['x'] > minimum + 17*virtual_view_unit and 
                coord['x'] < maximum - 17*virtual_view_unit and 
                coord['y'] > minimum + 17*virtual_view_unit and 
                coord['y'] < maximum - 17*virtual_view_unit
            ):
            new_coordinates.append(coord)
    return (new_coordinates, {'maximum': maximum, 'minimum': minimum, 'total_points': len(new_coordinates)})
 
if __name__ == '__main__':
    coords = readCoords()
    coords, summary = simplifyGraph(coords)
    outputTxt(str(summary), 'summary')
    ant_count = 10
    generations = 100
    alpha_vals = [0.2, 0.4, 0.6, 0.8, 1.0]
    beta = [1.5. 2.0, 2.5]
    pheromone_residual_coefficients = [0.2, 0.4, 0.6, 0.8]
    pheromone_residual_coefficients_local = [0.2, 0.4, 0.6, 0.8]
    q_0 = [0.2, 0.4, 0.6]
    print('Start -', str(datetime.now()))
    # Ant System
    as_results=pd.DataFrame(columns=['alpha','beta','pheromone_residual_coefficient','best_cost_found','update_count','lowest_cost_update_count','lowest_costs_found','best_solution_found','time_s'])
    for alpha in alpha_vals:
        for ro in pheromone_residual_coefficients:
            start = time.time()
            graph = Graph(coords)
            aco = AntSystem(ant_count, generations, alpha, beta, ro)
            best_cost, best_costs, avg_costs, best_solution = aco.solve(graph)
            new_row = {
                    'alpha': alpha,
                    'beta': beta,
                    'pheromone_residual_coefficient': ro,
                    'best_cost_found': best_cost,
                    'avg_costs_found': avg_costs,
                    'best_costs_found': best_costs,                        
                    'update_count': len(best_costs),
                    'lowest_cost_update_count': len(set(best_costs))-1,
                    'lowest_costs_found': list(set(best_costs)),
                    'best_solution_found': best_solution,
                    'time_s': time.time()-start
                    }
            as_results = as_results.append(new_row, ignore_index=True)
    outputCsv(as_results, 'as_results')
    print('AS end -', str(datetime.now()))
    # Ant Colony System
    acs_results=pd.DataFrame(columns=['alpha','beta','fi','ro','q_0','best_cost_found','update_count','lowest_cost_update_count','lowest_costs_found','best_solution_found','time_s'])
    for alpha in alpha_vals:
        for fi in pheromone_residual_coefficients_local:
           for ro in pheromone_residual_coefficients:
                start = time.time()
                graph = Graph(coords)
                aco = AntColonySystem(ant_count, generations, alpha, beta, fi, ro, q_0)
                best_cost, best_costs, avg_costs, best_solution = aco.solve(graph)
                new_row = {
                        'alpha': alpha,
                        'beta': beta,
                        'fi': fi,
                        'ro': ro,
                        'q_0':q_0,
                        'best_cost_found': best_cost,
                        'avg_costs_found': avg_costs,
                        'best_costs_found': best_costs,                        
                        'update_count': len(best_costs),
                        'lowest_cost_update_count': len(set(best_costs))-1,
                        'lowest_costs_found': list(set(best_costs)),
                        'best_solution_found': best_solution,
                        'time_s': time.time()-start
                        }
                acs_results = acs_results.append(new_row, ignore_index=True)
    outputCsv(acs_results, 'acs_results')
    print('ACS end -', str(datetime.now()))
    # MinMax Ant System
    mmas_results=pd.DataFrame(columns=['alpha','beta','pheromone_residual_coefficient','best_cost_found','update_count','lowest_cost_update_count','lowest_costs_found','best_solution_found','time_s'])
    for alpha in alpha_vals:
        for ro in pheromone_residual_coefficients:
            for q_0 in q_0s:
                start = time.time()
                graph = Graph(coords)
                aco = MinMaxAntSystem(ant_count, generations, alpha, beta, ro)
                best_cost, best_costs, avg_costs, best_solution = aco.solve(graph)
                new_row = {
                        'alpha': alpha,
                        'beta': beta,
                        'pheromone_residual_coefficient': ro,
                        'best_cost_found': best_cost,
                        'avg_costs_found': avg_costs,
                        'best_costs_found': best_costs,                        
                        'update_count': len(best_costs),
                        'lowest_cost_update_count': len(set(best_costs))-1,
                        'lowest_costs_found': list(set(best_costs)),
                        'best_solution_found': best_solution,
                        'time_s': time.time()-start
                        }
                mmas_results = mmas_results.append(new_row, ignore_index=True)
    outputCsv(mmas_results, 'as_results')
    print('MMAS end -', str(datetime.now()))