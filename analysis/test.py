from tracer import Tracer
from itree import IntervalTree, Interval
from cache import IntervalCache, ARC
import random

def bufferSize(): 
    tracer = Tracer()

    # Increase max buffer size to 1MB
    tracer.createPipe()
    tracer.setPipeSize(1000000)

def itreeTest():
    tree = IntervalTree()

    tree.insert(Interval(100, 150))
    tree.insert(Interval(70, 80))
    tree.insert(Interval(70,80))
    tree.insert(Interval(50, 60))
    tree.insert(Interval(30, 40))
    tree.insert(Interval(200, 250))
    tree.insert(Interval(260, 310))
    tree.insert(Interval(260, 300))

    for node in tree.rbTree:
        print(node)

def iTreeCacheTest():
    cache = IntervalCache(3, 5)

    cache.add(0, 10)
    cache.add(5, 10)
    cache.add(6, 10)
    cache.add(8, 10)
    cache.add(12, 15)
    cache.add(12, 15)
    cache.add(12, 15)

    print(cache.lru)
    print([str(x) for x in cache.tree.rbTree])


def arcTest():
    def evict(v):
        print(v)

    cache = ARC(10, evict)

    cache.add(1, 0)
    cache.add(1, 0)
    cache.add(2, 0)
    
    data = [random.randint(0, 100) for x in range(1000)]
    values = [0]*100

    for d,v in zip(data, values):
        cache.add(d,v)

    print(cache.t1)
    print(cache.t2)

#arcTest()

def cacheTest():
    cache = IntervalCache(10, 2)

    cache.add(0,10)
    cache.add(2,10)
    cache.add(0,10)
    cache.add(10,20)
    cache.add(0,10)


    print(len(cache.l1.t1))
    print(len(cache.l1.t2))

    print(cache.frequentItems)

cacheTest()
