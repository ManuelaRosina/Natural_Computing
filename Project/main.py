from input_tsp.handle_coords import readCoords
from swarm_intelligence.aco import *
import os
import numpy as np
import pandas as pd
import time
from datetime import datetime

def outputCsv(df, filename: str):
    output_path = os.path.join(os.path.dirname(os.path.realpath('__file__')), 'output_'+datetime.now().strftime('%m_%d'))
    if not os.path.exists(output_path):
        os.mkdir(output_path)
    df.to_csv(os.path.join(output_path, filename+'.csv'))   
    
if __name__ == '__main__':
    coords = readCoords()
    graph = Graph(coords)
    ant_count = 10000
    generations = 1000
    alpha_vals = np.round(np.linspace(0, 1, 11), 2)
    beta_vals = [1.5, 2, 2.5]
    pheromone_residual_coefficients = np.round(np.linspace(0.1, 1, 10), 2)
    pheromone_residual_coefficients_local = np.round(np.linspace(0.1, 1, 10), 2)
    q_0s = np.round(np.linspace(0, 1, 11), 2)
    # Ant System
    as_results=pd.DataFrame(columns=['alpha','beta','pheromone_residual_coefficient','best_cost_found','update_count','lowest_cost_update_count','lowest_costs_found','best_solution_found','time_s'])
    for alpha in alpha_vals:
        for beta in beta_vals:
            for ro in pheromone_residual_coefficients:
                start = time.time()
                aco = AntSystem(ant_count, generations, alpha, beta, ro)
                try:
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
                except:
                    print('Exception-AS')
    outputCsv(as_results, 'as_results')
    # Ant Colony System
    acs_results=pd.DataFrame(columns=['alpha','beta','fi','ro','q_0','best_cost_found','update_count','lowest_cost_update_count','lowest_costs_found','best_solution_found','time_s'])
    for alpha in alpha_vals:
        for beta in beta_vals:
            for fi in pheromone_residual_coefficients_local:
               for ro in pheromone_residual_coefficients:
                    for q_0 in q_0s:
                        start = time.time()
                        aco = AntColonySystem(ant_count, generations, alpha, beta, fi, ro, q_0)
                        try:
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
                        except:
                            print('Exception-ACS')
    outputCsv(acs_results, 'acs_results')
    # MinMax Ant System
    mmas_results=pd.DataFrame(columns=['alpha','beta','pheromone_residual_coefficient','best_cost_found','update_count','lowest_cost_update_count','lowest_costs_found','best_solution_found','time_s'])
    for alpha in alpha_vals:
        for beta in beta_vals:
            for ro in pheromone_residual_coefficients:
                start = time.time()
                aco = MinMaxAntSystem(ant_count, generations, alpha, beta, ro)
                try:
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
                except:
                    print('Exception-MMAS')
    outputCsv(mmas_results, 'as_results')