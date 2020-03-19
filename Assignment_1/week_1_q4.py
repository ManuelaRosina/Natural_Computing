# Import libraries
import matplotlib.pyplot as plt
import numpy as np
import random

# Show plot
def createPlot(x, xlabel = 'Iterations', ylabel = 'Fitness'):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot([i[0] for i in x], [i[1] for i in x], color='lightblue', linewidth=3)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.show()

# GA (1+1)
def run(l, mutp, iters, alternative_option = False):
    # Keep fitness history
    fitness = []
    # Generate Random bit sequence
    x = np.random.randint(2, size=(l))
    for i in range(1500):
        xm = x.copy()
        for j in range(len(x)):
            if random.random() <= p:
                xm[j] = int(not bool(x[j]))
        if xm.sum() > x.sum() or alternative_option:
            # Fitness history
            fitness.append((i, xm.sum()))
            if xm.sum() == l:
                # Optimum has been reached
                break;
            x = xm
    return fitness

if __name__ == '__main__':
    # Length of binary string
    l = 100
    # Mutation rate
    p = 1/l
    # Iterations
    iters = 1500
    
    # A. Main Run 
    print('A. Main Run\nMutation Probability = {0}\nBit Sequence Length = {1}\nIterations = {2}\n----'.format(p, l, iters))
    createPlot(run(l, p, iters))
    
    # B. 10 Runs 
    print('----\nB. Begin 10-Run Marathon')
    history= []
    for i in range(1, 11):
        print('----\n- Run No.', i)
        r = run(l, p, iters)
        createPlot(r)
        history.append((i, r[-1][0]))
    print('----')
    createPlot(history, 'Run', 'Iterations')
        
    # C. Run using alternative strategy
    print('----\nC. Alternative Run\nMutation Probability = {0}\nBit Sequence Length = {1}\nIterations = {2}'.format(p, l, iters))
    createPlot(run(l, p, iters, alternative_option = True))