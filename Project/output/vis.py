import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import ast

df2a = pd.read_csv('w_out_ClosestNeighbours/as_results.csv')
df2b = pd.read_csv('w_out_ClosestNeighbours/acs_results.csv')
df2c = pd.read_csv('w_out_ClosestNeighbours/mmas_results.csv')

df1a = pd.read_csv('w_ClosestNeighbours/as_results.csv')
df1b = pd.read_csv('w_ClosestNeighbours/acs_results.csv')
df1c = pd.read_csv('w_ClosestNeighbours/mmas_results.csv')

print(df1a.time_s.mean())
print(df1b.time_s.mean())
print(df1c.time_s.mean())
print(df1a.time_s.sum()/60)
print(df1b.time_s.sum()/60)
print(df1c.time_s.sum()/60)

best_as=df1a[df1a.best_cost_found==df1a.best_cost_found.min()]
best_acs=df1b[df1b.best_cost_found==df1b.best_cost_found.min()]
best_mmas=df1c[df1c.best_cost_found==df1c.best_cost_found.min()]

def avg_of_avgPerGen(list_of_average_costs_for_each_gen):
    x = ast.literal_eval(list_of_average_costs_for_each_gen)
    return np.mean(x)

df1a['ams'] = df1a.avg_costs_found.apply(lambda x: avg_of_avgPerGen(x))
df1b['ams'] = df1b.avg_costs_found.apply(lambda x: avg_of_avgPerGen(x))
df1c['ams'] = df1c.avg_costs_found.apply(lambda x: avg_of_avgPerGen(x))

# best costs
df1a['label']='AS'
df1b['label']='ACS'
df1c['label']='MMAS'
dfs = [pd.DataFrame(df1a.loc[:, ['best_cost_found', 'label']]), pd.DataFrame(df1b.loc[:, ['best_cost_found', 'label']]), pd.DataFrame(df1c.loc[:, ['best_cost_found', 'label']])]
all_dfs = pd.concat(dfs)
all_dfs.boxplot(by='label')
plt.title('Best costs')
plt.suptitle('')
plt.savefig('best_costs.png')

# time
mean_time_w_cn = [df1a.time_s.mean(), df1b.time_s.mean(), df1c.time_s.mean()]
mean_time_wout_cn = [df2a.time_s.mean(), df2b.time_s.mean(), df2c.time_s.mean()]
index = ['AS', 'ACS', 'MMAS']
df = pd.DataFrame({'mean_time': mean_time_w_cn, 'mean_time_wout_cn': mean_time_wout_cn}, index=index)
ax = df.plot.barh()
ax.legend(['w/ Closest Neighbours', 'w/out Closest Neighbours'])
plt.xlabel('average time in seconds')
plt.savefig('time.png')

# alpha
x = df1b.alpha.unique()
y1 = df1a.groupby('alpha')['ams'].mean()
y2 = df1b.groupby('alpha')['ams'].mean()
y3 = df1c.groupby('alpha')['ams'].mean()
plt.plot(x, y1)
plt.plot(x, y2)
plt.plot(x, y3)
plt.legend(['Ant System', 'Ant Colony System', 'Min-Max Ant System'])
plt.xlabel('alpha')
plt.ylabel('Mean Average Best costs')
plt.savefig('alpha.png')
plt.show()

# beta
x = df1b.beta.unique()
y1 = df1a.groupby('beta')['ams'].mean()
y2 = df1b.groupby('beta')['ams'].mean()
y3 = df1c.groupby('beta')['ams'].mean()
plt.plot(x, y1)
plt.plot(x, y2)
plt.plot(x, y3)
plt.legend(['Ant System', 'Ant Colony System', 'Min-Max Ant System'])
plt.xlabel('beta')
plt.ylabel('Mean Average Best costs')
plt.savefig('beta.png')
plt.show()

# rho
x = df1b.ro.unique()
y1 = df1a.groupby('pheromone_residual_coefficient')['ams'].mean()
y2 = df1b.groupby('ro')['ams'].mean()
y3 = df1c.groupby('pheromone_residual_coefficient')['ams'].mean()
plt.plot(x, y1)
plt.plot(x, y2)
plt.plot(x, y3)
plt.legend(['Ant System', 'Ant Colony System', 'Min-Max Ant System'])
plt.xlabel('Pheromone residual coefficient')
plt.ylabel('Mean Average Best costs')
plt.savefig('rho.png')
plt.show()

# q0
x = df1b.q_0.unique()
y2 = df1b.groupby('q_0')['ams'].mean()
plt.plot(x, y2)
plt.xlabel('Select closest city with probability p')
plt.ylabel('Mean Average Best costs')
plt.savefig('q_0.png')
plt.show()

# fi
x = df1b.fi.unique()
y2 = df1b.groupby('fi')['ams'].mean()
plt.plot(x, y2)
plt.xlabel('Local pheromone residual coefficient')
plt.ylabel('Mean Average Best costs')
plt.savefig('fi.png')
plt.show()

# min
df1a['diff'] = df1a.apply(lambda x: x.max - x.min)
df1b['diff'] = df1b.apply(lambda x: x.max - x.min)
df1c['diff'] = df1c.apply(lambda x: x.max - x.min)

x = df1c['min'].unique()
y2 = df1c.groupby('min')['ams'].mean()
plt.plot(x, y2)
plt.xlabel('Minimum pheromone limitation on trails')
plt.ylabel('Mean Average Best costs')
plt.savefig('min.png')
plt.show()

# max
x = df1c['max'].unique()
y2 = df1c.groupby('max')['ams'].mean()
plt.plot(x, y2)
plt.xlabel('Maximum pheromone limitation on trails')
plt.ylabel('Mean Average Best costs')
plt.savefig('max.png')
plt.show()
