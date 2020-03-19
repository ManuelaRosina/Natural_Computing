import numpy as np
from sklearn.metrics import roc_auc_score

# load the two text files with the scores
english_pred = np.loadtxt('english.test.out')
tagalog_pred = np.loadtxt('tagalog.test.out')

# assign the labels
y = [1 for x in english_pred]
y2 = [0 for x in tagalog_pred]

# merge lists to one
y_true = np.array(y + y2)
scores = np.concatenate((english_pred,tagalog_pred))

# compute and print the score
print(roc_auc_score(y_true, scores))
