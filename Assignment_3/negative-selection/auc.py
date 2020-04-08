import numpy as np
from sklearn.metrics import roc_auc_score

def compute_score(y, y2, pred1, pred2):
    y_true = np.array(y + y2)
    scores = np.concatenate((pred1,pred2))

    return roc_auc_score(y_true, scores)

def language():
    # load the two text files with the scores
    folder = "out4/"
    outfile = '.test.out'
    english_pred = np.loadtxt(folder+'english'+outfile)
    tagalog_pred = np.loadtxt(folder+'tagalog'+outfile)
    hiligaynon_pred = np.loadtxt(folder+'hiligaynon'+outfile)
    middle_english_pred = np.loadtxt(folder+'middle-english'+outfile)
    plautdietsch_pred = np.loadtxt(folder+'plautdietsch'+outfile)
    xhosa_pred = np.loadtxt(folder+'xhosa'+outfile)

    # assign the labels
    y = [0 for x in english_pred]
    y2 = [1 for x in tagalog_pred]
    y3 = [1 for x in hiligaynon_pred]
    y4 = [1 for x in middle_english_pred]
    y5 = [1 for x in plautdietsch_pred]
    y6 = [1 for x in xhosa_pred]

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

def syscall_auc(r):
    path_unm = '/home/manuela/Uni/jaar_1_Master/Natural_Computing/negative-selection/syscalls/snd-unm/'
    path_cert = '/home/manuela/Uni/jaar_1_Master/Natural_Computing/negative-selection/syscalls/snd-cert/'
    label = np.loadtxt(path_cert+'snd-cert.1.labels')
    pred = np.loadtxt('syscalls_out'+r+'/snd-cert.1.test.out.p')
    for i in range(2,4):
        label = np.concatenate((label, np.loadtxt(path_cert+'snd-cert.'+str(i)+'.labels')))
        pred = np.concatenate((pred, np.loadtxt('syscalls_out'+r+'/snd-cert.'+str(i)+'.test.out.p')))

    print('cert')
    print(roc_auc_score(label, pred))
    print()

    label2 = np.loadtxt(path_unm+'snd-unm.1.labels')
    pred2 = np.loadtxt('syscalls2_out'+r+'/snd-unm.1.test.out.p')
    for i in range(2,4):
        label2 = np.concatenate((label2, np.loadtxt(path_unm+'snd-unm.'+str(i)+'.labels')))
        pred2 = np.concatenate((pred2, np.loadtxt('syscalls2_out'+r+'/snd-unm.'+str(i)+'.test.out.p')))

    print('unm')
    print(roc_auc_score(label2, pred2))
    print()
    print('both')
    print(roc_auc_score(np.concatenate((label,label2)), np.concatenate((pred,pred2))))

rs = ['3','4','6']
for r in rs:
    print('r = '+r)
    syscall_auc(r)
    print()
