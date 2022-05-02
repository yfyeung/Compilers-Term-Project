from ds.graph import Node, Edge, Graph
from rex2nfa import Rex2NFA
from nfa2dfa import NFA2DFA


class DFA2Min(object):
    '''DFA最小化'''
    def __init__(self, DFA=None, alphabet=None):
        self.dfa_graph = DFA
        self.alphabet = alphabet
        self.matrix = [] # 行是起始结点序号, 列是字符, 元素是终止结点序号
        self.P = None
        self.dfa_min_graph = self.transformDFAMin()

    def transformDFAMin(self):
        '''DFA最小化'''
        if self.dfa_graph is None:
            print("DFA not found".center(50, '='))
            return None

        self.store_matrix()
        self.init_division()

        index = 0
        while index < len(self.P):
            subset = self.P[index]
            dct = {}
            for num, node_id in enumerate(subset):
                dct[node_id] = -1

            flag = True
            for idx, ch in enumerate(self.alphabet):
                if not flag:
                    break
                for node_id in subset:
                    point_node_id = self.matrix[node_id][idx]
                    set_id = self.find_set_id(node_id=point_node_id)
                    dct[node_id] = set_id
                values = list(set(dct.values()))
                if len(values) != 1:
                    flag = False
                    divide_sets = [[] for i in range(len(values))]
                    for k, v in dct.items():
                        i = values.index(v)
                        divide_sets[i].append(k)
                    self.P.pop(index)
                    for st in divide_sets:
                        if len(st):
                            self.P.insert(index, st)
            if flag:
                index += 1

        dfa_min_dict = {}
        terminal_nodes = []
        init_node = -1
        for cluster in self.P:
            repr = cluster[0]
            for inst in cluster:
                if self.dfa_graph.beginNode == inst:
                    init_node = repr
                if inst in self.dfa_graph.endNodes and repr not in terminal_nodes:
                    terminal_nodes.append(repr)
                dfa_min_dict[inst] = repr

        edges = []
        for edge in self.dfa_graph.edges:
            begin_node = Node(id=dfa_min_dict[edge.beginNode.id])
            end_node = Node(id=dfa_min_dict[edge.endNode.id])
            new_edge = Edge(beginNode=begin_node, endNode=end_node, label=edge.label)
            edges.append(new_edge)

        unique_edges = self.remove_duplicate(edges=edges)
        reachable_edges = self.remove_unreachable(edges=unique_edges)

        self.dfa_min_graph = Graph()
        self.dfa_min_graph.edges = reachable_edges
        self.dfa_min_graph.beginNode = init_node
        self.dfa_min_graph.endNodes = terminal_nodes

        return self.dfa_min_graph

    def find_set_id(self, node_id):
        '''找到集合id'''
        for i, subset in enumerate(self.P):
            if node_id in subset:
                return i
        return -1

    def remove_unreachable(self, edges=None):
        '''移除不可达的边'''
        return edges

    def remove_duplicate(self, edges=None):
        '''去掉重复结点'''
        if edges is None:
            print("edges is None".center(50, '='))
            exit(-1)

        remove_list = []
        for i in range(len(edges)):
            for j in range(i + 1, len(edges)):
                if str(edges[i]) == str(edges[j]):
                    remove_list.append(i)
        remove_list.sort(reverse=True)

        unique_edges = []
        for idx, inst in enumerate(edges):
            if idx not in remove_list:
                unique_edges.append(inst)

        return unique_edges

    def store_matrix(self):
        '''存储构造矩阵'''
        node_list = []
        for edge in self.dfa_graph.edges:
            begin_node = edge.beginNode
            if begin_node.id not in node_list:
                node_list.append(begin_node.id)
            end_node = edge.endNode
            if end_node.id not in node_list:
                node_list.append(end_node.id)

        num_node = len(node_list)
        [self.matrix.append([-1 for i in range(len(self.alphabet))]) for i in range(num_node)]

        for edge in self.dfa_graph.edges:
            begin_node = edge.beginNode
            end_node = edge.endNode
            col = self.alphabet.index(edge.label)
            self.matrix[begin_node.id][col] = end_node.id

    def init_division(self):
        '''初始化P'''
        self.P = [[], []]
        nodes = []
        for edge in self.dfa_graph.edges:
            begin_node = edge.beginNode
            end_node = edge.endNode
            nodes.append(begin_node)
            nodes.append(end_node)

        for node in nodes:
            if node.id in self.dfa_graph.endNodes:
                if node.id not in self.P[1]:
                    self.P[1].append(node.id)
            else:
                if node.id not in self.P[0]:
                    self.P[0].append(node.id)

        if len(self.P[0]) == 0:
            self.P.pop(0)
        elif len(self.P[1]) == 0:
            self.P.pop(1)

    def move(self, node=None, ch=None):
        '''获取next node'''
        next_node = None
        for edge in self.dfa_graph.edges:
            if edge.beginNode == node and edge.label == ch:
                next_node = edge.endNode
        return next_node

    def print_dfa_min_graph(self):
        '''打印结果'''
        print(' Minimized DFA '.center(50, '='))
        print(self.dfa_min_graph)
        print(''.center(50, '='))

    def get_dfa_min_graph(self):
        '''获取结果'''
        return self.dfa_min_graph

    def print_construct_matrix(self):
        '''打印构造矩阵'''
        print(' Construct matrix '.center(50, '='))
        print(self.alphabet)
        for x in self.matrix:
            print(x)
        print(''.center(50, '='))

if __name__ == '__main__':
    input_str = '(ab*|c)ca'
    print(f"Input: {input_str}")
    rex2nfa = Rex2NFA(input_str)
    nfa_graph = rex2nfa.get_nfa_graph()

    nfa2dfa = NFA2DFA(nfa_graph)
    dfa_graph = nfa2dfa.get_dfa_graph()
    alphabet = nfa2dfa.get_alphabet()

    dfa2min = DFA2Min(dfa_graph, alphabet)
    dfa2min.print_construct_matrix()
    dfa2min.print_dfa_min_graph()
