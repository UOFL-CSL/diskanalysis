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

    # Clear the cache
    def flush(self):
        self.queue = []
        self.items = {}

class IntervalCache:
    # Tree is the L1 cache
    tree = IntervalTree()

    # L2 cache: frequent items
    frequentItems = {}

    # L2 eviction cache
    evictedItems = {}

    def __init__(self, size, threshold):
        self.size = size
        self.threshold = threshold

        self.l1 = ARC(size, self.evict)

    def evict(self, node):
        pass
        #self.tree.rbTree.remove(node)

    # TODO: check overlaps to update frequency on overlapping items
    def add(self, min, max):
        # Update the L1 cache and the interval tree when an item is added 
        key = str(min) + " " + str(max)

        if not self.l1.contains(key):
            #node = self.tree.insert(Interval(min, max))
            self.l1.add(key, True)            
        # Check the support if the item should be moved to the L2 cache
        else:
            self.l1.add(key, None)

            if key in self.l1.t2:
                if self.l1.t2[key][0] > self.threshold:
                    self.frequentItems[key] = time.time()

# Adaptive Replacement Cache
# Modified to store support/node reference
# T1 = recency
# T2 = frequency (min 2 support)
class ARC():
    # T1 and T2, LRU caches
    t1 = OrderedDict()
    t2 = OrderedDict()

    # B1 and B2, ghost/eviction caches
    b1 = OrderedDict()
    b2 = OrderedDict()

    # target size
    p = 0

    # C is the fixed size portion
    def __init__(self, c, evictCallback):
        self.c = c
        self.evictCallback = evictCallback

    def adapt(self, b1miss):
        sigma = 0
        
        if b1miss:
            if len(self.b1) >= len(self.b2):
                sigma = 1
            else:
                sigma = int(len(self.b2)/len(self.b1))

            self.p = min(self.p + sigma, self.c)
        else:
            if len(self.b2) >= len(self.b1):
                sigma = 1
            else:
                sigma = int(len(self.b1)/len(self.b2))

            self.p = max(self.p - sigma, 0)

    # Moves LRU item from the t1/t2 cache to b1/b2
    def replace(self, item):
        t1len = len(self.t1)
        
        if t1len > 0 and (t1len > self.p or (item in self.b2 and t1len == self.p)):
            k,v = self.t1.popitem(last=False)

            self.b1[k] = v
        else:
            k,v = self.t2.popitem(last=False)

            self.b2[k] = v

    def add(self, item, value):
        # Case 1, cache hit
        # Move to t2
        if item in self.t1:
            self.t1[item][0] += 1
            self.t2[item] = self.t1[item]
            del self.t1[item]

            return

        if item in self.t2:
            value = self.t2[item]
            value[0] += 1
            del self.t2[item]
            self.t2[item] = value

            return

        # Case 2 partial miss
        # B1
        if item in self.b1:
            self.adapt(True)
            self.replace(item)

            self.t2[item] = self.b1[item]
            del self.b1[item]

            return

        if item in self.b2:
            self.adapt(False)
            self.replace(item)

            self.t2[item] = self.b2[item]
            del self.b2[item]

            return

        # Case 3 complete miss
        l1len = len(self.t1) + len(self.b1)
        if l1len == self.c:
            if len(self.t1) < self.c:
                k,v = self.b1.popitem(last=False)
                self.evictCallback(v[1])

                self.replace(item)
            else:
                self.t1.popitem(last=False)
        if l1len < self.c:
            totallen = l1len + len(self.t2) + len(self.b2)

            if totallen >= self.c:
                if totallen == 2*self.c:
                    k,v = self.b2.popitem(last=False)
                    self.evictCallback(v[1])

                self.replace(item)

        self.t1[item] = [1, value]

    def contains(self, item):
        return (item in self.t1) or (item in self.t2) or (item in self.b1) or (item in self.b2)
