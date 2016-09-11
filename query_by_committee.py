import random
from ElectedList import ElectedList
import numpy as np

class QueryByCommittee:
    def __init__(self, c_list, class_list, X_pool, Y_pool, X_evaluate, Y_evaluate, start_X=None, start_Y=None, random_start_number=None):
        self.c_list = c_list
        self.track_items = []
        self.track_best_entropy = []
        self.track_entropy = []
        self.max_entropy = None
        self.best_item_index = None
        self.score_ = [[] for clf in self.c_list]
        self.start_X = list()
        self.start_Y = list()
        self.t_X = []
        self.t_Y = []
        self.predict = [None] * 2
        self.X_pool = X_pool
        self.Y_pool = Y_pool
        self.X_evaluate = X_evaluate
        self.Y_evaluate = Y_evaluate
        self.class_list = class_list
        if random_start_number is None:
            if (start_X is None) or (start_Y is None):
                print "Start_X or start_Y or both are not given, we will select randomly 10 elements from pools to start..."
                self.random_start(10)
            else:
                self.start_X = start_X
                self.start_Y = start_Y
                self.t_X = start_X
                self.t_Y = start_Y
        else:
            self.random_start(random_start_number)

    def extend_training_set(self, elements_in_x, elements_in_y):
        self.t_X += elements_in_x
        self.t_Y += elements_in_y

    def random_start(self, size):
        rn = np.random.choice(len(self.X_pool), size, replace=False)
        for i in rn:
            self.start_X += [self.X_pool[i]]
            self.start_Y += [self.Y_pool[i]]
            self.t_X += [self.X_pool[i]]
            self.t_Y += [self.Y_pool[i]]

    def update_pool(self, elements_out):
        for element in elements_out:
            best_item_index = self.X_pool.index(element)
            for i in range(best_item_index, len(self.X_pool) - 1):
                self.X_pool[i] = self.X_pool[i + 1]
                self.Y_pool[i] = self.Y_pool[i + 1]
            del self.X_pool[len(self.X_pool) - 1]
            del self.Y_pool[len(self.Y_pool) - 1]

    def committee_votes(self, element):
        key_value_predictions = list()
        s = list()
        for clf in self.c_list:
            prediction = clf.predict(element)
            key_value_predictions.append([prediction, 0])

        for e_1 in key_value_predictions:
            for e_2 in key_value_predictions:
                if e_1[0] == e_2[0]:
                    e_1[1] += 1

        for e in key_value_predictions:
            if e not in s:
                s.append(e)
        return s

    def committee_vote_entropy(self, element):
        class_list = self.class_list
        votes_list = self.committee_votes(element)
        vote_entropy = 0
        for c in class_list:
            p = votes_list.count(c)/len(class_list)
            if p != 0:
                vote_entropy += p*np.log(p)
            else:
                vote_entropy += 0
        return vote_entropy

    def committee_predict(self, element):
        max_votes = 0
        votes_list = self.committee_votes(self.c_list, element)
        b = list()
        for e in votes_list:
            if e[1] > max_votes:
                b = list()
                b.append(e[0])
                max_votes = e[1]
            else:
                if e[1] == max_votes:
                    b.append(e[0])
                    max_votes = e[1]
        if len(b) > 1:
            return random.choice(b)
        else:
            if len(b) == 1:
                return b[0]
            else:
                return False
                print logging.warning('No element is selected, something is wrong !!!')

    def query(self, budget=None, step=1):
        if budget is None:
            budget = len(self.X_pool)
        for a in range(0, budget):
            for clf in self.c_list:
                clf = clf.fit(self.t_X, self.t_Y)
                actual_score = clf.score(self.X_evaluate, self.Y_evaluate)
                self.score_[self.c_list.index(clf)].append(actual_score)
            best_elements = ElectedList(size=step)

            for item in self.X_pool:
                item_entropy = self.committee_vote_entropy(item)
                best_elements.maintain([item, self.Y_pool[self.X_pool.index(item)], item_entropy])
            best_elements.maintain_end(self.X_pool, self.Y_pool)
            x, y = best_elements.get_elements()
            self.extend_training_set(x, y)
            self.update_pool(x)

            a += 1
        return {'start_X': self.start_X, 'start_Y': self.start_Y, 'scores_list': self.score_, 'classifier': self.c_list, 'x_pool': self.X_pool, 'y_pool': self.Y_pool, 'x_training': self.t_X, 'y_training': self.t_Y}



