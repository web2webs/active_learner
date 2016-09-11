import warnings

warnings.filterwarnings("ignore")
from query_by_committee import QueryByCommittee
from random_query import RandomQuery
from sklearn import tree
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn import linear_model
from sklearn import datasets
import numpy as np
import matplotlib.pyplot as plt
import os



def run_main(i, X, Y_r):
    exp_path = "experiments/committee_based_syntactic" + str(i)

    if not os.path.exists(exp_path):
        os.makedirs(exp_path)
    list_X = None
    list_Y = None
    list_X = list()
    list_Y = list()
    X_evaluate = list()
    Y_evaluate = list()

    l1 = list()
    l2 = list()
    l3 = list()
    l4 = list()
    l_1 = list()
    l_2 = list()
    l_3 = list()
    l_4 = list()
    l = list()
    for i in range(0, len(Y_r)):
        if Y_r[i] == 1:
            l1.append(i)
        if Y_r[i] == 2:
            l2.append(i)
        if Y_r[i] == 3:
            l3.append(i)

    rndom = np.random.choice(len(l1), 50, replace=False)

    for j in range(0, len(l1)):
        if j in rndom:
            l.append(l1[j])
            l_1.append(l1[j])

    rndom = np.random.choice(len(l2), 50, replace=False)
    for j in range(0, len(l2)):
        if j in rndom:
            l.append(l2[j])
            l_2.append(l2[j])
    rndom = np.random.choice(len(l3), 50, replace=False)
    for j in range(0, len(l3)):
        if j in rndom:
            l.append(l3[j])
            l_3.append(l3[j])

    for j in range(0, len(X)):
        if j in l:
            Y_evaluate.append(Y_r[j])
            X_evaluate.append(X[j])
        else:
            list_Y.append(Y_r[j])
            list_X.append(X[j])

    # import some data to play with
    iris = datasets.load_iris()
    X = iris.data[:, :2].tolist()  # we only take the first two features.
    Y = iris.target.tolist()
    clfs = [SVC(), GaussianNB(), linear_model.LogisticRegression(C=1e5), tree.DecisionTreeClassifier()]
    list_r_X = list(list_X)
    list_r_Y = list(list_Y)
    X_r_evaluate = list(X_evaluate)
    Y_r_evaluate = list(Y_evaluate)
    al = QueryByCommittee(clfs, [0, 1, 2], list_X, list_Y, X_evaluate, Y_evaluate)
    result = al.query()
    rndom = RandomQuery(clfs, [0, 1, 2], list_r_X, list_r_Y, X_r_evaluate, Y_r_evaluate, start_X=result['start_X'], start_Y=result['start_Y'] )
    result2= rndom.query_random()

    for i,j,k in zip(result['scores_list'], result2['scores_list'], ['SVM', 'NaiveBayes', 'LogisticRegression', 'DecisionTree']):
        print i
        #plt.figure()
        #random_x = np.linspace(0, len(i), len(i))
        #plt.plot(random_x, i, 'g')
        #random_x = np.linspace(0, len(j), len(j))
        #plt.plot(random_x, j, 'r')
        with open(exp_path + '/score_of_model'+ k , 'w') as f:
            for s in i:
                f.write(str(s) + '\n')
        with open(exp_path + '/score_of_random'+ k , 'w') as f:
            for s in j:
                f.write(str(s) + '\n')
    #plt.show()


X = list()
for i in xrange(0, 10):
    for j in xrange(0, 10):
        for k in xrange(0, 10):
            X.append([i, j, k])


Y_r = list()
for i in range(0, len(X)):
    item = X[i]
    x = item[0] + item[1] + item[2]
    if x < 10:
        Y_r.append(1)
    if 10 <= x < 20:
        Y_r.append(2)
    if 20 <= x < 30:
        Y_r.append(3)

for i in range(106, 130):
    run_main(i, X, Y_r)