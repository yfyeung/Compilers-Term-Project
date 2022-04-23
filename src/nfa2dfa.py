import sys
import os

sys.path.append(".")
from utils.utils import *
from utils.datastructure import *
from src.rex2nfa import Regex


class NFA2DFA(object):
    def __init__(self, NFA=None):
        self.NFA = NFA
        # 字符集合
        self.alphabet = []
        # 新的结点状态
        self.state_list = []

        # 结点从0开始标号
        Node.num = 0
        # 存储确定化的矩阵
        self.transform_matrix = []
        # 根据输入的nfa获取到字符表
        self.calculate_alphabet()

        self.dfa_graph = Graph()

    def transformDFA(self):
        if self.NFA is None:
            print("NFA not found".center(50, '='))
            return None
        nfa_begin_node = self.NFA.beginNode

        dfa_begin_state = self.epsilon_closure(node_set=[nfa_begin_node])
        dfa_begin_state = StateNode(node_set=dfa_begin_state)
        if self.NFA.endNode.id in [node.id for node in dfa_begin_state.node_set]:
            dfa_begin_state.is_end = True

        dfa_begin_state.is_begin = True
        self.state_list.append(dfa_begin_state)

        index = 0
        nfa_end_node = self.NFA.endNode

        while index < len(self.state_list):
            self.transform_matrix.append([None for x in range(len(self.alphabet))])
            begin_state = self.state_list[index]
            for col, ch in enumerate(self.alphabet):
                move_set = self.move(node_set=begin_state.node_set, ch=ch)
                end_state = self.epsilon_closure(node_set=move_set)
                if len(end_state) == 0:
                    self.transform_matrix[index][col] = None
                    continue
                elif end_state in [state.node_set for state in self.state_list]:
                    row_num = [state.node_set for state in self.state_list].index(end_state)
                    self.transform_matrix[index][col] = self.state_list[row_num]
                else:
                    state_node = StateNode(node_set=end_state)
                    if nfa_end_node in state_node.node_set:
                        state_node.is_end = True
                    self.state_list.append(state_node)
                    row_num = len(self.state_list) - 1
                    self.transform_matrix[index][col] = self.state_list[row_num]
            index += 1

        edges = []
        endNodes = []
        beginNode = []
        for row, row_inst in enumerate(self.transform_matrix):
            if self.state_list[row].is_end:
                endNodes.append(self.state_list[row].id)
            if self.state_list[row].is_begin:
                beginNode.append(self.state_list[row].id)
            for col, inst in enumerate(row_inst):
                if inst is not None:
                    begin_node_id = self.state_list[row].id
                    end_node_id = inst.id
                    label = self.alphabet[col]
                    edge = Edge(beginNode=Node(id=begin_node_id), endNode=Node(id=end_node_id), label=label)
                    edges.append(edge)

        self.dfa_graph.edges = edges
        self.dfa_graph.beginNode = beginNode[0]
        self.dfa_graph.endNodes = endNodes

        print(" Finish transformation from nfa to dfa ".center(50, '='))
        print(self.dfa_graph)
        return self.dfa_graph

    def calculate_alphabet(self):
        if self.NFA is None:
            return
        for edge in self.NFA.edges:
            if edge.label not in self.alphabet and edge.label != 'epsilon':
                self.alphabet.append(edge.label)

    def move(self, node_set=None, ch=None):
        target_set = []
        for node in node_set:
            for edge in self.NFA.edges:
                if edge.beginNode == node and edge.label == ch:
                    target_set.append(edge.endNode)

        return target_set

    def epsilon_closure(self, node_set=None):
        target_set = []
        stack = []
        for node in node_set:
            target_set.append(node)
            stack.append(node)

        while len(stack) > 0:
            ele = stack.pop()
            for edge in self.NFA.edges:
                if edge.beginNode == ele and edge.label == 'epsilon':
                    target_set.append(edge.endNode)
                    stack.append(edge.endNode)
        return target_set


if __name__ == '__main__':
    regex_string = '(ab|c)*abb'
    regexer = Regex(regex=regex_string)
    nfa_graph = regexer.transformNFA()
    nfa2dfa = NFA2DFA(NFA=nfa_graph)
    nfa2dfa.transformDFA()
