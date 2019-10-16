import math
from cache import ItemsetCache
from graph import Graph

def pair_unmap(z):
    flooredRoot = math.floor(math.sqrt(z))
    condition = z - flooredRoot**2

    if condition < flooredRoot:
        return condition, flooredRoot
    else:
        return flooredRoot, condition - flooredRoot

class StreamProvider:
    numStreams = 16
    stream = {}

    def generateStreams(self, cache: ItemsetCache):
        self.stream = {}
        graph = Graph()

        for item in cache.frequentItems.keys():
            item1, item2 = pair_unmap(item)

            if not graph.exists(item1):
                graph.add(item1)

            if not graph.exists(item2):
                graph.add(item2)

            graph.addEdge(item1, item2)

        groups = graph.connectedGroups()

        for i in range(0, len(groups)):
            id = i % self.numStreams

            for block in groups[i]:
                self.stream[block] = id

    def queryStream(self, blockId):
        return self.stream[blockId]



