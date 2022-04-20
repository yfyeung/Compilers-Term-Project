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

    def __str__(self):
        if self.endNodes is None:
            return_str = "Start={} EndNode={} \n".format(self.beginNode, self.endNode)
        else:
            return_str = "Start={} EndNodes=[{}] \n".format(self.beginNode, ' '.join([str(node) for node in self.endNodes]))
        for edge in self.edges:
            return_str += str(edge) + '\n'
        return return_str