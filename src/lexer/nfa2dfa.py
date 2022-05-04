import sys
sys.path.append(".")

from ds.graph import Node, Edge, Graph, StateNode
from rex2nfa import Rex2NFA


class NFA2DFA(object):
    '''NFA转DFA'''
    def __init__(self, NFA=None):
        self.nfa_graph = NFA
        self.alphabet = self._calculate_alphabet() # 字符集合
        self.dfa_graph = self._nfa2dfa()

    def _nfa2dfa(self):
        '''转化为DFA'''
        if self.nfa_graph is None:
            print("NFA not found".center(40, '='))
            return None

        dfa_begin_state = StateNode(self._varepsilon_closure([self.nfa_graph.node_tail]))
        dfa_begin_state.is_begin = True
        if self.nfa_graph.node_head.id in [node.id for node in dfa_begin_state.node_set]:
            dfa_begin_state.is_end = True

        state_list = [] # 新的结点状态
        state_list.append(dfa_begin_state)

        index = 0
        transform_matrix = [] # 存储确定化的矩阵
        while index < len(state_list):
            transform_matrix.append([None for x in range(len(self.alphabet))])
            for col, ch in enumerate(self.alphabet):
                move_set = self._move(state_list[index].node_set, ch)
                end_state = self._varepsilon_closure(move_set)
                if len(end_state) == 0:
                    transform_matrix[index][col] = None
                    continue
                elif end_state in [state.node_set for state in state_list]:
                    row_num = [state.node_set for state in state_list].index(end_state)
                    transform_matrix[index][col] = state_list[row_num]
                else:
                    state_node = StateNode(node_set=end_state)
                    if self.nfa_graph.node_head in state_node.node_set:
                        state_node.is_end = True
                    state_list.append(state_node)
                    row_num = len(state_list) - 1
                    transform_matrix[index][col] = state_list[row_num]
            index += 1

        node_tail = []
        node_heads = []
        edges = []
        for row, row_inst in enumerate(transform_matrix):
            if state_list[row].is_begin:
                node_tail.append(state_list[row].id)
            if state_list[row].is_end:
                node_heads.append(state_list[row].id)
            for col, inst in enumerate(row_inst):
                if inst is not None:
                    edge = Edge(node_tail=Node(id=state_list[row].id),
                                node_head=Node(id=inst.id), node_type=self.alphabet[col])
                    edges.append(edge)

        self.dfa_graph = Graph()
        self.dfa_graph.edges = edges
        self.dfa_graph.node_tail = node_tail[0]
        self.dfa_graph.node_heads = node_heads
        return self.dfa_graph

    def _calculate_alphabet(self):
        ''' 根据输入的nfa获取字符表'''
        if self.nfa_graph is None:
            return

        alphabet = []
        for edge in self.nfa_graph.edges:
            if edge.node_type not in alphabet and edge.node_type != 'varepsilon':
                alphabet.append(edge.node_type)

        return alphabet

    def _move(self, node_set=None, ch=None):
        ''' 获取给定状态集合的移动集合'''
        target_set = []
        for node in node_set:
            for edge in self.nfa_graph.edges:
                if edge.node_tail == node and edge.node_type == ch:
                    target_set.append(edge.node_head)

        return target_set

    def _varepsilon_closure(self, node_set=None):
        ''' 计算varepsilon闭包'''
        target_set = []
        stack = []
        for node in node_set:
            target_set.append(node)
            stack.append(node)

        while len(stack) > 0:
            ele = stack.pop()
            for edge in self.nfa_graph.edges:
                if edge.node_tail == ele and edge.node_type == 'varepsilon':
                    target_set.append(edge.node_head)
                    stack.append(edge.node_head)
        return target_set

    def print_dfa_graph(self):
        '''打印结果'''
        print(' DFA '.center(40, '='))
        print(self.dfa_graph)
        print(''.center(40, '='))

    def get_dfa_graph(self):
        '''获取结果'''
        return self.dfa_graph

    def get_alphabet(self):
        '''获取字母表'''
        return self.alphabet


if __name__ == '__main__':
    input_str = '(ab|c)*abb'
    print(f"Input: {input_str}")
    rex2nfa = Rex2NFA(input_str)
    nfa_graph = rex2nfa.get_nfa_graph()

    nfa2dfa = NFA2DFA(nfa_graph)
    nfa2dfa.print_dfa_graph()
