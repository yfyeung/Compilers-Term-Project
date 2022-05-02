class Node():
    num = 0
    def __init__(self, id=None):
        if id is not None:
            self.id = id
        else:
            self.id = Node.num
            Node.num += 1

    def __str__(self):
        return str(self.id)


class Edge():
    def __init__(self, node_tail=None, node_head=None, node_type=None):
        self.node_tail = node_tail
        self.node_head = node_head
        self.node_type = node_type

    def __str__(self):
        return f"Edge {self.node_tail} -> {self.node_head}, node_type:{self.node_type}"


class Graph():
    def __init__(self, node_tail=None, node_head=None, node_heads=None):
        self.node_tail = node_tail
        self.node_head = node_head
        self.node_heads = node_heads
        self.edges = []

    def add_star(self, obj=None):
        if isinstance(obj, str):
            centerNode = Node()
            node_tail = Node()
            node_head = Node()
            a = Edge(node_tail=centerNode, node_head=centerNode, node_type=str(obj))
            b = Edge(node_tail=node_tail, node_head=centerNode, node_type="varepsilon")
            c = Edge(node_tail=centerNode, node_head=node_head, node_type="varepsilon")

            self.edges += [a, b, c]
            self.node_tail = node_tail
            self.node_head = node_head

        elif isinstance(obj, Graph):
            node_tail = Node()
            node_head = Node()
            a = Edge(node_tail=node_tail, node_head=node_head, node_type="varepsilon")
            b = Edge(node_tail=node_tail, node_head=obj.node_tail, node_type="varepsilon")
            c = Edge(node_tail=obj.node_head, node_head=node_head, node_type="varepsilon")
            d = Edge(node_tail=obj.node_head, node_head=obj.node_tail, node_type="varepsilon")

            for edge in obj.edges:
                self.edges.append(edge)

            self.edges += [a, b, c, d]
            self.node_tail = node_tail
            self.node_head = node_head

        else:
            raise Exception(f"Unknown Type: {type(obj)}")

    def add_union(self, obj1=None, obj2=None):
        if isinstance(obj1, Graph) and isinstance(obj2, str):
            node_tail = Node()
            node_head = Node()
            a = Edge(node_tail=node_tail, node_head=obj1.node_tail, node_type="varepsilon")
            b = Edge(node_tail=obj1.node_head, node_head=node_head, node_type="varepsilon")
            c = Edge(node_tail=node_tail, node_head=node_head, node_type=str(obj2))

            for edge in obj1.edges:
                self.edges.append(edge)

            self.edges += [a, b, c]
            self.node_tail = node_tail
            self.node_head = node_head

        elif isinstance(obj1, str) and isinstance(obj2, Graph):
            node_tail = Node()
            node_head = Node()
            a = Edge(node_tail=node_tail, node_head=obj2.node_tail, node_type="varepsilon")
            b = Edge(node_tail=obj2.node_head, node_head=node_head, node_type="varepsilon")
            c = Edge(node_tail=node_tail, node_head=node_head, node_type=str(obj1))

            for edge in obj2.edges:
                self.edges.append(edge)

            self.edges += [a, b, c]
            self.node_tail = node_tail
            self.node_head = node_head

        elif isinstance(obj1, Graph) and isinstance(obj2, Graph):
            node_tail = Node()
            node_head = Node()
            a = Edge(node_tail=node_tail, node_head=obj1.node_tail, node_type="varepsilon")
            b = Edge(node_tail=node_tail, node_head=obj2.node_tail, node_type="varepsilon")
            c = Edge(node_tail=obj1.node_head, node_head=node_head, node_type="varepsilon")
            d = Edge(node_tail=obj2.node_head, node_head=node_head, node_type="varepsilon")

            self.node_tail = node_tail
            self.node_head = node_head

            for edge in obj1.edges:
                self.edges.append(edge)

            for edge in obj2.edges:
                self.edges.append(edge)

            self.edges += [a, b, c, d]

        elif isinstance(obj1, str) and isinstance(obj2, str):
            node_tail = Node()
            node_head = Node()
            a = Edge(node_tail=node_tail, node_head=node_head, node_type=str(obj1))
            b = Edge(node_tail=node_tail, node_head=node_head, node_type=str(obj2))

            self.edges += [a, b]
            self.node_tail = node_tail
            self.node_head = node_head

    def add_concat(self, obj1=None, obj2=None):
        if isinstance(obj1, Graph) and isinstance(obj2, str):
            node_head = Node()
            a = Edge(node_tail=obj1.node_head, node_head=node_head, node_type=str(obj2))
            for edge in obj1.edges:
                self.edges.append(edge)

            self.edges += [a]
            self.node_tail = obj1.node_tail
            self.node_head = node_head

        elif isinstance(obj1, str) and isinstance(obj2, Graph):
            node_tail = Node()
            a = Edge(node_tail=node_tail, node_head=obj2.node_tail, node_type=str(obj1))

            for edge in obj2.edges:
                self.edges.append(edge)

            self.edges += [a]
            self.node_tail = node_tail
            self.node_head = obj2.node_head

        elif isinstance(obj1, Graph) and isinstance(obj2, Graph):
            a = Edge(node_tail=obj1.node_head, node_head=obj2.node_tail, node_type="varepsilon")
            self.node_tail = obj1.node_tail
            self.node_head = obj2.node_head

            for edge in obj1.edges:
                self.edges.append(edge)

            for edge in obj2.edges:
                self.edges.append(edge)

            self.edges += [a]

        elif isinstance(obj1, str) and isinstance(obj2, str):
            node_tail = Node()
            centerNode = Node()
            node_head = Node()
            a = Edge(node_tail=node_tail, node_head=centerNode, node_type=str(obj1))
            b = Edge(node_tail=centerNode, node_head=node_head, node_type=str(obj2))

            self.node_tail = node_tail
            self.node_head = node_head
            self.edges += [a, b]

    def __str__(self):
        if self.node_heads is None:
            return_str = f"start_node:{self.node_tail}\nnode_head:{self.node_head} \n"
        else:
            nodes_heads = ' '.join([str(node) for node in self.node_heads])
            return_str = f"start_node:{self.node_tail}\nnode_heads:[{nodes_heads}] \n"
        for edge in self.edges:
            return_str += str(edge) + '\n'
        return return_str


class StateNode():
    id = 0
    def __init__(self, node_set=None):
        self.node_set = node_set
        self.id = StateNode.id
        self.is_begin = False
        self.is_end = False
        StateNode.id += 1

    def __str__(self):
        return 'StateNode' + str(self.id) +' ' + ''.join([str(x) for x in self.node_set])
