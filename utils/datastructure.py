class Node():
    def __init__(self, id):
        self.id = id

    def __str__(self):
        return str(self.id)


class Edge():
    def __init__(self, begin, end, weight=None):
        self.begin = begin
        self.end = end
        self.weight = weight

    def __str__(self):
        return f"weight:{weight}, begin:{begin}, end:{end}"


class Graph():
    def __init__(self, source, terminal, endNodes):
        self.source = source
        self.terminal = terminal
        self.endNodes = endNodes
        self.edges = []

    def add_star(self, obj=None):
        if isinstance(obj, str):
            centerNode = Node()
            beginNode = Node()
            endNode = Node()

            edgeLink = Edge(beginNode=centerNode, endNode=centerNode, label=str(obj))
            beginEdgeEpsilon = Edge(beginNode=beginNode, endNode=centerNode, label="epsilon")
            endEdgeEpsilon = Edge(beginNode=centerNode, endNode=endNode, label="epsilon")

            self.edges.append(edgeLink)
            self.edges.append(beginEdgeEpsilon)
            self.edges.append(endEdgeEpsilon)

            self.beginNode = beginNode
            self.endNode = endNode

        elif isinstance(obj, Graph):
            beginNode = Node()
            endNode = Node()
            edgeone = Edge(beginNode=beginNode, endNode=endNode, label="epsilon")
            edgetwo = Edge(beginNode=beginNode, endNode=obj.beginNode, label="epsilon")
            edgethree = Edge(beginNode=obj.endNode, endNode=endNode, label="epsilon")
            edgefour = Edge(beginNode=obj.endNode, endNode=obj.beginNode, label="epsilon")

            for edge in obj.edges:
                self.edges.append(edge)

            self.edges.append(edgeone)
            self.edges.append(edgetwo)
            self.edges.append(edgethree)
            self.edges.append(edgefour)

            self.beginNode = beginNode
            self.endNode = endNode

        else:
            print("Unknown type {}".format(type(obj)))
            exit(-1)

    def add_union(self, obj1=None, obj2=None):
        if isinstance(obj1, Graph) and isinstance(obj2, str):
            beginNode = Node()
            endNode = Node()
            edgeone = Edge(beginNode=beginNode, endNode=obj1.beginNode, label="epsilon")
            edgetwo = Edge(beginNode=obj1.endNode, endNode=endNode, label="epsilon")
            edgethree = Edge(beginNode=beginNode, endNode=endNode, label=str(obj2))

            for edge in obj1.edges:
                self.edges.append(edge)

            self.edges.append(edgeone)
            self.edges.append(edgetwo)
            self.edges.append(edgethree)

            self.beginNode = beginNode
            self.endNode = endNode

        elif isinstance(obj1, str) and isinstance(obj2, Graph):
            beginNode = Node()
            endNode = Node()
            edgeone = Edge(beginNode=beginNode, endNode=obj2.beginNode, label="epsilon")
            edgetwo = Edge(beginNode=obj2.endNode, endNode=endNode, label="epsilon")
            edgethree = Edge(beginNode=beginNode, endNode=endNode, label=str(obj1))

            for edge in obj2.edges:
                self.edges.append(edge)

            self.edges.append(edgeone)
            self.edges.append(edgetwo)
            self.edges.append(edgethree)

            self.beginNode = beginNode
            self.endNode = endNode

        elif isinstance(obj1, Graph) and isinstance(obj2, Graph):
            beginNode = Node()
            endNode = Node()
            edgeone = Edge(beginNode=beginNode, endNode=obj1.beginNode, label="epsilon")
            edgetwo = Edge(beginNode=beginNode, endNode=obj2.beginNode, label="epsilon")
            edgethree = Edge(beginNode=obj1.endNode, endNode=endNode, label="epsilon")
            edgefour = Edge(beginNode=obj2.endNode, endNode=endNode, label="epsilon")


            self.beginNode = beginNode
            self.endNode = endNode

            for edge in obj1.edges:
                self.edges.append(edge)

            for edge in obj2.edges:
                self.edges.append(edge)

            self.edges.append(edgeone)
            self.edges.append(edgetwo)
            self.edges.append(edgethree)
            self.edges.append(edgefour)


        elif isinstance(obj1, str) and isinstance(obj2, str):
            beginNode = Node()
            endNode = Node()

            edgeone = Edge(beginNode=beginNode, endNode=endNode, label=str(obj1))
            edgetwo = Edge(beginNode=beginNode, endNode=endNode, label=str(obj2))

            self.edges.append(edgeone)
            self.edges.append(edgetwo)

            self.beginNode = beginNode
            self.endNode = endNode


    def add_concat(self, obj1=None, obj2=None):
        if isinstance(obj1, Graph) and isinstance(obj2, str):
            endNode = Node()
            edgeone = Edge(beginNode=obj1.endNode, endNode=endNode, label=str(obj2))
            for edge in obj1.edges:
                self.edges.append(edge)

            self.edges.append(edgeone)
            self.beginNode = obj1.beginNode
            self.endNode = endNode

        elif isinstance(obj1, str) and isinstance(obj2, Graph):
            beginNode = Node()
            edgeone = Edge(beginNode=beginNode, endNode=obj2.beginNode, label=str(obj1))

            for edge in obj2.edges:
                self.edges.append(edge)

            self.edges.append(edgeone)
            self.beginNode = beginNode
            self.endNode = obj2.endNode

        elif isinstance(obj1, Graph) and isinstance(obj2, Graph):
            edgeone = Edge(beginNode=obj1.endNode, endNode=obj2.beginNode, label="epsilon")
            self.beginNode = obj1.beginNode
            self.endNode = obj2.endNode

            for edge in obj1.edges:
                self.edges.append(edge)

            for edge in obj2.edges:
                self.edges.append(edge)

            self.edges.append(edgeone)

        elif isinstance(obj1, str) and isinstance(obj2, str):
            beginNode = Node()
            centerNode = Node()
            endNode = Node()

            edge1 = Edge(beginNode=beginNode, endNode=centerNode, label=str(obj1))
            edge2 = Edge(beginNode=centerNode, endNode=endNode, label=str(obj2))

            self.beginNode = beginNode
            self.endNode = endNode

            self.edges.append(edge1)
            self.edges.append(edge2)


    def __str__(self):
        if self.endNodes is None:
            return_str = "Start={} EndNode={} \n".format(self.beginNode, self.endNode)
        else:
            return_str = "Start={} EndNodes=[{}] \n".format(self.beginNode, ' '.join([str(node) for node in self.endNodes]))
        for edge in self.edges:
            return_str += str(edge) + '\n'
        return return_str



if __name__ == '__main__':
    pass
