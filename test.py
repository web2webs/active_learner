import warnings

warnings.filterwarnings("ignore")
from query_by_committee import QueryByCommittee
from random_query import RandomQuery
from ActiveLearner import UncertaintyBased
from sklearn import tree
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn import linear_model
from sklearn import datasets
import numpy as np
import matplotlib.pyplot as plt


training_X = np.loadtxt(open("data/dataset_filtered_equationV2/data_t_X_multiclass.csv", "r"), delimiter=",").tolist()
training_Y = np.loadtxt(open("data/dataset_filtered_equationV2/data_t_Y_multiclass.csv", "r"), delimiter=",").tolist()

validation_X = np.loadtxt(open("data/dataset_filtered_equationV2/data_e_X_multiclass.csv", "r"), delimiter=",").tolist()
validation_Y = np.loadtxt(open("data/dataset_filtered_equationV2/data_e_Y_multiclass.csv", "r"), delimiter=",").tolist()

# import some data to play with
iris = datasets.load_iris()
X = iris.data[:, :2].tolist()  # we only take the first two features.
Y = iris.target.tolist()
#clfs = [SVC(), GaussianNB(), linear_model.LogisticRegression(C=1e5), tree.DecisionTreeClassifier()]
clf = GaussianNB()
training_r_X = list(training_X)
training_r_Y = list(training_Y)
validation_r_X = list(validation_X)
validation_r_Y = list(validation_Y)
al = UncertaintyBased(clf,training_X, training_Y, validation_X, validation_Y)
result = al.query()
rndom = RandomQuery(list(clf), training_r_X, training_r_Y, validation_r_X, validation_r_Y, start_X=result['start_X'], start_Y=result['start_Y'] )
result2= rndom.query_random()
for i,j in zip(result['scores_list'], result2['scores_list']):
    print i
    plt.figure()
    random_x = np.linspace(0, len(i), len(i))
    plt.plot(random_x, i, 'g')
    random_x = np.linspace(0, len(j), len(j))
    plt.plot(random_x, j, 'r')

plt.show()