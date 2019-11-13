# Uses an RB-tree for the self balancing tree in conjunction with storing intervals
from rb_tree import RedBlackTree

class Interval:
    def __init__(self, minimum, maximum):
        self.minimum = minimum
        self.maximum = maximum

    def __eq__(self, other):
        if other is None:
            return False
            
        return self.minimum == other.minimum

    def __lt__(self, other):
        return self.minimum < other.minimum
    
    def __le__(self, other):
        return self.minimum <= other.minimum

    def __gt__(self, other):
        return self.minimum > other.minimum

    def __ge__(self, other):
        return self.maximum >= other.maximum

class IntervalTree:
    rbTree = RedBlackTree()

    def __init__(self):
        pass

    def insert(self, value):
        self.rbTree.add(value)
