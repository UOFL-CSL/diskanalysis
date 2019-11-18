# Uses an RB-tree for the self balancing tree in conjunction with storing intervals
from rb_tree import RedBlackTree

class Interval:
    def __init__(self, minimum, maximum):
        self.minimum = minimum
        self.maximum = maximum

    def __eq__(self, other):
        if other is None:
            return False
            
        return self.minimum == other.minimum and self.maximum == other.maximum

    def __lt__(self, other):
        if self.minimum != other.minimum:
            return self.minimum < other.minimum

        return self.maximum < other.maximum
    
    def __le__(self, other):
        return self.minimum <= other.minimum

    def __gt__(self, other):
        return self.minimum > other.minimum

    def __ge__(self, other):
        return self.minimum >= other.minimum

    def __str__(self):
        return str(self.minimum) + ":" + str(self.maximum)

class IntervalTree:
    rbTree = RedBlackTree()

    def __init__(self):
        pass

    def insert(self, value):
        return self.rbTree.add(value)

    def overlapping(self, i1, i2):
        return i1.minimum <= i2.maximum and i1.maximum >= i2.minimum

    # Return all overlapping intervals
    def find_overlap(self, value: Interval):
        # If the interval is less than root.min, traverse left, otherwise right
        pass



