import numpy as np
from sklearn.metrics import roc_auc_score
from sklearn.metrics import roc_curve
import matplotlib.pyplot as plt

<<<<<<< HEAD
def compute_score(y, y2, pred1, pred2):
    y_true, scores = merge_lists(y, y2, pred1, pred2)

    return roc_auc_score(y_true, scores)

def plot_results(y, y2, pred1, pred2)
    y_true, scores = merge_lists(y, y2, pred1, pred2)
    fpr, tpr, thresholds = roc_curve(y_true, scores)
    plt.plot(fpr, tpr)
    plt.title("ROC Curve")
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.show()

def merge_lists(y, y2, pred1, pred2)
    y_true = np.array(y + y2)
    scores = np.concatenate((pred1,pred2))

    return y_true, scores

# load the two text files with the scores
outfile = '.test6.out'
english_pred = np.loadtxt('english'+outfile)
tagalog_pred = np.loadtxt('tagalog'+outfile)
hiligaynon_pred = np.loadtxt('hiligaynon'+outfile)
middle_english_pred = np.loadtxt('middle-english'+outfile)
plautdietsch_pred = np.loadtxt('plautdietsch'+outfile)
xhosa_pred = np.loadtxt('xhosa'+outfile)

# assign the labels
y = [1 for x in english_pred]
y2 = [0 for x in tagalog_pred]
y3 = [0 for x in hiligaynon_pred]
y4 = [0 for x in middle_english_pred]
y5 = [0 for x in plautdietsch_pred]
y6 = [0 for x in xhosa_pred]

# plot curve
plot_results(y, y2, english_pred, tagalog_pred)

# compute and print the score
print('tagalog:')
print(compute_score(y, y2, english_pred, tagalog_pred))
<<<<<<< HEAD
#print('hiligaynon:')
#print(compute_score(y, y3, english_pred, hiligaynon_pred))
#print('middle-english:')
#print(compute_score(y, y4, english_pred, middle_english_pred))
#print('plautdietsch:')
#print(compute_score(y, y5, english_pred, plautdietsch_pred))
#print('xhosa:')
#print(compute_score(y, y6, english_pred, xhosa_pred))
<<<<<<< HEAD
=======

# load the two text files with the scores
english_pred = np.loadtxt('english.test.out')
tagalog_pred = np.loadtxt('lang/xhosa.out')
#tagalog_pred = np.loadtxt('tagalog.test.out')

# assign the labels
y = [1 for x in english_pred]
y2 = [0 for x in tagalog_pred]

# merge lists to one
y_true = np.array(y + y2)
scores = np.concatenate((english_pred,tagalog_pred))

fpr, tpr, thresholds = roc_curve(y_true, scores)
plt.plot(fpr, tpr)
plt.title("ROC Curve")
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.show()

# compute and print the score
print(roc_auc_score(y_true, scores))
=======
>>>>>>> parent of 53bf86e... Part 2
=======
print('hiligaynon:')
print(compute_score(y, y3, english_pred, hiligaynon_pred))
print('middle-english:')
print(compute_score(y, y4, english_pred, middle_english_pred))
print('plautdietsch:')
print(compute_score(y, y5, english_pred, plautdietsch_pred))
print('xhosa:')
print(compute_score(y, y6, english_pred, xhosa_pred))
>>>>>>> parent of 761c305... fixed auc computation
