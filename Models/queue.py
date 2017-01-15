import numpy as np

__author__ = 'Albert'

class Queue:
    def __init__(self,size):
        self.size = size
        self.items = []

    def isEmpty(self):
        return self.items == []

    def isFull(self):
        return len(self.items) == self.size

    def push(self,item):
        if(len(self.items)< self.size):
            self.enqueue(item)
        elif (len(self.items) == self.size):
            self.dequeue()
            self.enqueue(item)
        else:
            print("This is impossible, something went wrong!")

    def enqueue(self, item):
        self.items.insert(0,item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)

    def mean(self):
        return np.mean(self.items)

    def get_list(self):
        return self.items

    def clear(self):
        self.items = []

    def get_max(self):
        return np.max(self.items)

    def get_min(self):
        return np.min(self.items)