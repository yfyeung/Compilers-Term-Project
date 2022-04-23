import sys
import os

sys.path.append(".")
from utils.utils import *
from utils.datastructure import *
from src.rex2nfa import Regex
from src.nfa2dfa import NFA2DFA




class DFAMinimizer(object):
    def __init__(self, DFA=None, alphabet=None):
        self.DFA = DFA
        self.dfa_mini = None
        # 行是起始结点序号，列是字符 元素是终止结点序号
        self.matrix = []
        self.P = None
        self.alphabet = alphabet

    def transformDFAMini(self):
        if self.DFA is None:
            print("DFA not found".center(50, '='))
            return None
        self.store_matrix()
        self.init_division()
        print("P0", self.P)
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
                if len(values) == 1:
                    pass
                else:
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

        print("Final", self.P)
        print("".center(50, '='))

        dfa_mini_dict = {}

        init_node = -1
        terminal_nodes = []

        for cluster in self.P:
            repr = cluster[0]
            for inst in cluster:
                if self.DFA.beginNode == inst:
                    init_node = repr
                if inst in self.DFA.endNodes:
                    if repr not in terminal_nodes:
                        terminal_nodes.append(repr)
                dfa_mini_dict[inst] = repr

        edges = []
        for edge in self.DFA.edges:
            begin_node = Node(id=dfa_mini_dict[edge.beginNode.id])
            end_node = Node(id=dfa_mini_dict[edge.endNode.id])
            new_edge = Edge(beginNode=begin_node, endNode=end_node, label=edge.label)
            edges.append(new_edge)

        print("before remove duplicate".center(50, '='))
        for edge in edges:
            print(edge)
        print()
        unique_edges = self.remove_duplicate(edges=edges)
        reachable_edges = self.remove_unreachable(edges=unique_edges)

        self.dfa_mini = Graph()
        self.dfa_mini.edges = reachable_edges
        self.dfa_mini.beginNode = init_node
        self.dfa_mini.endNodes = terminal_nodes

        print(' Finish transformation from dfa to mini dfa '.center(50, '='))

        print(self.dfa_mini)
        return self.dfa_mini

    def find_set_id(self, node_id):
        for i, subset in enumerate(self.P):
            if node_id in subset:
                return i
        return -1

    def remove_unreachable(self, edges=None):
        return edges

    # 去掉重复结点
    def remove_duplicate(self, edges=None):
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
        node_list = []
        for edge in self.DFA.edges:
            begin_node = edge.beginNode
            if begin_node.id not in node_list:
                node_list.append(begin_node.id)
            end_node = edge.endNode
            if end_node.id not in node_list:
                node_list.append(end_node.id)
        num_node = len(node_list)
        [self.matrix.append([-1 for i in range(len(self.alphabet))]) for i in range(num_node)]
        for edge in self.DFA.edges:
            begin_node = edge.beginNode
            end_node = edge.endNode
            col = self.alphabet.index(edge.label)
            self.matrix[begin_node.id][col] = end_node.id

        print(' Construct matrix '.center(50, '='))
        print(self.alphabet)
        for x in self.matrix:
            print(x)
        print(''.center(50, '='))

    def init_division(self):
        self.P = [[], []]
        nodes = []
        for edge in self.DFA.edges:
            begin_node = edge.beginNode
            end_node = edge.endNode
            nodes.append(begin_node)
            nodes.append(end_node)

        for node in nodes:
            if node.id in self.DFA.endNodes:
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
        next_node = None
        for edge in self.DFA.edges:
            if edge.beginNode == node and edge.label == ch:
                next_node = edge.endNode
        return next_node


if __name__ == '__main__':
    # 0 代表 0 1 代表 1-9
    int_num = "((0)|(1(0|1)*))"
    # 1. .1 1.1 三种形式
    float_num = "( ((0|1)(0|1)*.)|((0|1)*.(0|1)(0|1)*) )"
    # *用x替代， &用$替代
    op = "(!|+|-|x|/|%|=|>|<|(==)|(<=)|(>=)|(!=)|(++)|(--)|($$)|(+=)|(-=)|(x=)|(/=)|(%=) )"
    # 用中文（）替代()
    se = "( (（)|(）)|({)|(})|(;)|[|]|(,))"
    # a代表a-z A-Z @ 代表转义字符 文 代表其他字符
    ch = "( ('(0|1|a|文)') | ('(@(0|n|r|t|v|a|b|f|'|\"|@))') )"
    # a代表a-z A-Z @ 代表转义字符 文 代表其他字符
    string = '( "((0|1|a|文) | (@(0|n|r|t|v|a|b|f|\'|"|@)) )*" )'
    idn = '( (_|a)(_|0|1|a)* )'

    regex_c = int_num + "|" + float_num + "|" + op + "|" + se + "|" + ch + "|" + string + "|" + idn

    regex_string = regex_c
    regex_string = '(ab*|c)ca'

    regexer = Regex(regex=regex_string)
    nfa_graph = regexer.transformNFA()

    nfa2dfa = NFA2DFA(NFA=nfa_graph)
    dfa_graph = nfa2dfa.transformDFA()

    alphabet = nfa2dfa.alphabet

    dfa2mini = DFAMinimizer(DFA=dfa_graph, alphabet=alphabet)
    dfa_mini_graph = dfa2mini.transformDFAMini()