from tracer import Tracer
from itree import IntervalTree, Interval
from cache import IntervalCache

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

itreeTest()

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

