import random


class ElectedList:
    def __init__(self, size):
        self.list = list()
        self.size = size
        self.min_score = None
        self.min_element_index = None

    def maintain(self, element):
        if element[2] > 0:
            if element[2] > self.min_score:
                self.list[self.min_element_index] = element
                score_array = None
                for x in self.list:
                    score_array += x[2]
                self.min_score = min(score_array)
                self.min_element_index = self.list.index(self.min_score)

    def maintain_end(self, x_pool, y_pool):
        if len(self.list) < self.size:
            i = random.sample(range(len(x_pool)), 1)
            if x_pool[i] not in self.get_elements()[0]:
                self.list += [x_pool[i], y_pool[i], 0]
            self.maintain_end()

    def get_elements(self):
        x = list()
        y = list()
        for element in self.list:
            x += element[0]
            y += element[1]
        return [x, y]



