from ElectedList import ElectedList
import random


class UncertaintyBased:
    def __init__(self, clf, X_pool, Y_pool, X_evaluate, Y_evaluate):

        self.track_items = []
        self.track_best_entropy = []
        self.track_entropy = []
        self.max_entropy = None
        self.best_item_index = None
        self.score_ = []
        self.predict = [None] * 2
        self.t_X = []
        self.t_Y = []
        self.X_pool = X_pool
        self.Y_pool = Y_pool
        self.X_evaluate = X_evaluate
        self.Y_evaluate = Y_evaluate
        self.clf = clf

    def extend_training_set(self, elements_in_x, elements_in_y):
        self.t_X += elements_in_x
        self.t_Y += elements_in_y

    def update_pool(self, elements_out):
        for element in elements_out:
            best_item_index = self.X_pool.index(element)
            for i in range(best_item_index, len(self.X_pool) - 1):
                self.X_pool[i] = self.X_pool[i + 1]
                self.Y_pool[i] = self.Y_pool[i + 1]
            del self.X_pool[len(self.X_pool) - 1]
            del self.Y_pool[len(self.Y_pool) - 1]

    def query(self, budget=None, step=1):
        if budget is None:
            budget = len(self.X_pool)
        for a in range(0, budget):

            self.clf = self.clf.fit(self.t_X, self.t_Y)
            actual_score = self.clf.score(self.X_evaluate, self.Y_evaluate)
            self.score_.append(actual_score)
            best_elements = ElectedList(size=step)

            for item in self.X_pool:
                predict = self.clf.predict_proba(item)
                predict_log_proba = self.clf.predict_log_proba(item)
                item_entropy = 0
                for i in range(0, len(predict[0])):
                    if predict[0][i] > 0:
                        item_entropy = item_entropy - predict[0][i] * predict_log_proba[0][i]
                best_elements.maintain([item, self.Y_pool[self.X_pool.index(item)], item_entropy])

            best_elements.maintain_end(self.X_pool, self.Y_pool)
            self.extend_training_set(best_elements.get_elements()[0], best_elements.get_elements()[1])
            self.update_pool(best_elements.get_elements()[0])

        budget -= 1

