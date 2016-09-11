import random
import numpy as np


class RandomQuery:
    def __init__(self, c_list, X_pool, Y_pool, X_evaluate, Y_evaluate, start_X=None, start_Y=None,
                 random_start_number=None):
        self.c_list = c_list
        self.track_items = []
        self.track_best_entropy = []
        self.track_entropy = []
        self.max_entropy = None
        self.best_item_index = None
        self.score_ = [[] for clf in self.c_list]
        self.t_X = []
        self.t_Y = []
        self.predict = [None] * 2
        self.X_pool = X_pool
        self.Y_pool = Y_pool
        self.X_evaluate = X_evaluate
        self.Y_evaluate = Y_evaluate
        if random_start_number is None:
            if (start_X is None) or (start_Y is None):
                print "Start_X or start_Y or both are not given, we will select randomly 10 elements from pools to start..."
                self.random_start(10)
            else:
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

    def query_random(self, budget=None):
        if budget is None:
            budget = len(self.X_pool)
        for a in range(0, budget):
            for clf in self.c_list:
                clf = clf.fit(self.t_X, self.t_Y)
                actual_score = clf.score(self.X_evaluate, self.Y_evaluate)
                self.score_[self.c_list.index(clf)].append(actual_score)

            best_item_index = self.X_pool.index(random.choice(self.X_pool))
            x, y = [self.X_pool[best_item_index]], [self.Y_pool[best_item_index]]
            print x
            print y
            self.extend_training_set(x, y)
            self.update_pool(x)

            a += 1
        return {'scores_list': self.score_, 'classifier': self.c_list, 'x_pool': self.X_pool, 'y_pool': self.Y_pool,
            'x_training': self.t_X, 'y_training': self.t_Y}