import numpy as np
from sklearn.metrics import roc_auc_score

def compute_score(y, y2, pred1, pred2):
    y_true = np.array(y + y2)
    scores = np.concatenate((pred1,pred2))

    return roc_auc_score(y_true, scores)

# load the two text files with the scores
folder = "out2/"
outfile = '.test.out'
english_pred = np.loadtxt(folder+'english'+outfile)
tagalog_pred = np.loadtxt(folder+'tagalog'+outfile)
hiligaynon_pred = np.loadtxt(folder+'hiligaynon'+outfile)
middle_english_pred = np.loadtxt(folder+'middle-english'+outfile)
plautdietsch_pred = np.loadtxt(folder+'plautdietsch'+outfile)
xhosa_pred = np.loadtxt(folder+'xhosa'+outfile)

# assign the labels
y = [1 for x in english_pred]
y2 = [0 for x in tagalog_pred]
y3 = [0 for x in hiligaynon_pred]
y4 = [0 for x in middle_english_pred]
y5 = [0 for x in plautdietsch_pred]
y6 = [0 for x in xhosa_pred]

# compute and print the score
print('tagalog:')
print(compute_score(y, y2, english_pred, tagalog_pred))
print('hiligaynon:')
print(compute_score(y, y3, english_pred, hiligaynon_pred))
print('middle-english:')
print(compute_score(y, y4, english_pred, middle_english_pred))
print('plautdietsch:')
print(compute_score(y, y5, english_pred, plautdietsch_pred))
print('xhosa:')
print(compute_score(y, y6, english_pred, xhosa_pred))
