import random


class ElectedList:
    def __init__(self, size):
        self.list = list()
        self.size = size
        self.min_score = 0
        self.min_element_index = 0

    def maintain(self, element):
        if element[2] > 0:
            if element[2] > self.min_score:

                if len(self.list) == 0:
                    self.list += [element]
                else:
                    self.list[self.min_element_index] = element
                score_array = list()
                for x in self.list:
                    score_array += [x[2]]
                self.min_score = min(score_array)

                self.min_element_index = score_array.index(self.min_score)

    def maintain_end(self, x_pool, y_pool):
        if len(self.list) < self.size:
            if len(x_pool) > 0:
                i = random.sample(range(len(x_pool)), 1)[0]
                x, y = self.get_elements()
                if x_pool[i] not in x:
                    self.list += [[x_pool[i], y_pool[i], 0]]
                self.maintain_end(x_pool, y_pool)


    def get_elements(self):
        x = list()
        y = list()
        for element in self.list:
            x += [element[0]]
            y += [element[1]]
        return x, y



