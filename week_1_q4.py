import matplotlib.pyplot as plt
import numpy as np
import random

# Length of binary string
l = 100
# Mutation rate
p = 1/l


fit = []
# Bit sequence
x = np.random.randint(2, size=(l))
for i in range(1500):
    xm = x.copy()
    for j in range(len(x)):
        if random.random() <= p:
            xm[j] = int(not bool(x[j]))
    if xm.sum() > x.sum():
        fit.append((i, xm.sum()))
        if xm.sum() == l:
            break;
        x = xm
# Plot
fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot([i[0] for i in fit], [i[1] for i in fit], color='lightblue', linewidth=3)
ax.set_xlabel('Iterations')
ax.set_ylabel('Fitness')
plt.show()