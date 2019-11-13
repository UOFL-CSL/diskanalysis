from collections import deque

# Graph Data Structure that utilizes Adjacency Lists
class Graph:
    lists = {}

    # Adds a vertex to the graph
    def add(self, id):
        self.lists[id] = []

    # Removes a vertex from the graph
    def remove(self, id):
        del self.lists[id]

    def addEdge(self, id1, id2):
        self.lists[id1].append(id2)
        self.lists[id2].append(id1)

    def removeEdge(self, id1, id2):
        self.lists[id1].remove(id2)
        self.lists[id2].remove(id1)

    def connections(self, id):
        return self.lists[id]

    def exists(self, id):
        return id in self.lists

    # DFS to find all groups
    def connectedGroups(self):
        visited = {}

        groups = []

        for vertex in self.lists.keys():
            grouping = []

            if vertex not in visited:
                visited[vertex] = 1
            else:
                continue

            stack = deque()

            stack.append(vertex)

            while len(stack) != 0:
                currentNode = stack.pop()

                grouping.append(currentNode)

                if currentNode not in visited:
                    visited[currentNode] = 1

                for adjNode in self.lists[currentNode]:
                    if adjNode not in visited:
                        stack.append(adjNode)

            groups.append(grouping)

        return groups

    def __str__(self):
        output = ""
        for k, v in self.lists.items():
            output += str(k) + " " + str(v) + "\n"

            return output