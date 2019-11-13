import time
from collections import deque
from collections import OrderedDict
from itree import Interval
from itree import IntervalTree

class ItemsetCache:
    # Oldest item cache
    queue = deque()
    # LRU cache
    lru = OrderedDict()

    # L1 cache: Stores timestamp and frequency of an item
    items = {}

    # L2 cache: Stores frequent items if they are evicted from L1
    frequentItems = {}

    # 0 = LRU, 1 = Oldest item
    method = 0

    def __init__(self, size, minsupport):
        self.size = size
        self.minsupport = minsupport

    def add(self, item):
        # If the cache is full, remove the item based on the method
        if self.method == 0:
            if len(self.lru) == self.size:
                for i in range(10000):
                    itemName, _ = self.lru.popitem(last=False)

                    # If the support is greater than the minimum, add it to the frequent item set
                    if self.items[itemName][1] >= self.minsupport:
                        self.frequentItems[itemName] = self.items[itemName]

                    del self.items[itemName]

        if self.method == 1:
            if len(self.queue) == self.size:
                itemName = self.queue.popleft()

                # If the support is greater than the minimum, add it to the frequent item set
                if self.items[itemName][1] >= self.minsupport:
                    self.frequentItems[itemName] = self.items[itemName]

                del self.items[itemName]

        # Increment the frequency of the current item
        if item in self.items:
            self.items[item] = [time.time(), self.items[item][1]+1]

            return

        # Add the new item
        self.items[item] = [time.time(), 1]

        if self.method == 0:
            self.lru[item] = 1
        if self.method == 1:
            self.queue.append(item)

    # Clear the cache
    def flush(self):
        self.queue = []
        self.items = {}

class IntervalCache:
    tree = IntervalTree()
    lru = OrderedDict()

    frequentItems = {}

    def __init__(self, size, threshold):
        self.size = size
        self.threshold = threshold

    def add(self, min, max):
        self.tree.insert(Interval(min, max))

        key = str(min) + " " + str(max)

        if key not in self.lru:
            self.lru[key] = 1
        else:
            value = self.lru[key]
            del self.lru[key]
            self.lru[key] = value + 1