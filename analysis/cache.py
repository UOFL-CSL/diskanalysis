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
    # LRU to remove old items from the cache
    lru = OrderedDict()

    # L2 cache: frequent items
    frequentItems = {}

    # L2 eviction cache
    evictedItems = {}

    def __init__(self, size, threshold):
        self.size = size
        self.threshold = threshold

    # TODO: check overlaps to update frequency on overlapping items
    # implement ARC like solution to adapt the cache size

    def add(self, min, max):
        # Update the LRU cache and the interval tree when an item is added 
        key = str(min) + " " + str(max)

        # Insert isn't needed if it is already in the tree
        if key not in self.lru:
            # Save reference to the node to make deletions O(N)
            node = self.tree.insert(Interval(min, max))
            self.lru[key] = (1, node)
        else:
            value = self.lru[key][0]
            node = self.lru[key][1]
            del self.lru[key]
            self.lru[key] = (value+1, node)

            if value+1 > self.threshold:
                self.frequentItems[key] = 1

        if len(self.lru) > self.size:
            self.purge()
 
    def purge(self):
        key, value = self.lru.popitem(last=False)

        self.tree.rbTree.remove(value[1])

# Adaptive Replacement Cache
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
    def __init__(self, c):
        self.c = c

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

    def add(self, item):
        # Case 1, cache hit
        # Move to t2
        if item in self.t1:
            del self.t1[item]
            self.t2[item] = time.time()

            return

        if item in self.t2:
            del self.t2[item]
            self.t2[item] = time.time()

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
                self.b1.popitem(last=False)

                self.replace(item)
            else:
                self.t1.popitem(last=False)
        if l1len < self.c:
            totallen = l1len + len(self.t2) + len(self.b2)

            if totallen >= self.c:
                if totallen == 2*self.c:
                    self.b2.popitem(last=False)

                self.replace(item)

        self.t1[item] = time.time()
