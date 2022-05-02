from ds.graph import Graph


class Rex2NFA:
    '''rex转NFA'''
    def __init__(self, regex):
        self.regex = regex
        self.preprocess_regex = self.preprocess(self.regex)
        self.nfa_graph = self.rex2nfa(self.preprocess_regex)

    def preprocess(self, regex):
        '''预处理, 补上省略的&'''
        preprocess_regex = ""
        regex_list = list(regex)
        for i in range(len(regex_list)):
            if i != 0 and regex_list[i] != '*' and \
                    regex_list[i] != '|' and regex_list[i-1] != '|' and \
                    regex_list[i] != ')' and regex_list[i-1] != '(':
                preprocess_regex += '&'
            preprocess_regex += regex_list[i]
    
        return preprocess_regex

    def rex2nfa(self, preprocess_regex):
        '''rex转nfa'''
        if not preprocess_regex:
            raise Exception("preprocess_regex is empty!")

        OPTR = []
        OPTR.append("#")
        OPND = []
        regex = list(preprocess_regex) + ['#']

        i = 0
        while not (OPTR[-1] == '#' and regex[i] == '#'):
            if self.isOperator(regex[i]):
                if self.priority_cmp(OPTR[-1], regex[i]) == 1:
                    ch = OPTR.pop()
                    MyGraph = Graph()
                    if ch == '*':
                        a = OPND.pop()
                        MyGraph.add_star(a)
                    elif ch == '&':
                        b = OPND.pop()
                        a = OPND.pop()
                        MyGraph.add_concat(a, b)
                    elif ch == '|':
                        b = OPND.pop()
                        a = OPND.pop()
                        MyGraph.add_union(a, b)
                    OPND.append(MyGraph)

                elif self.priority_cmp(OPTR[-1], regex[i]) == 0:
                    OPTR.pop()
                    i += 1

                elif self.priority_cmp(OPTR[-1], regex[i]) == -1:
                    OPTR.append(regex[i])
                    i += 1

            else:
                OPND.append(regex[i])
                i += 1

        return OPND[-1]

    def isOperator(self, ch):
        '''判断是否是操作符'''
        return ch in ['*', '&', '|', '(', ')', '#']

    def priority_cmp(self, a, b):
        '''比较a, b的优先级'''
        if a == '*':
            if b == '(':
                return -1
            else:
                return 1

        elif a == '&':
            if b == '*' or b == '(':
                return -1
            else:
                return 1

        elif a == '|':
            if b == '*' or b == '&' or b == '(':
                return -1
            else:
                return 1

        elif a == '(':
            if b == ')':
                return 0
            elif b == '#':
                return 2
            else:
                return -1

        elif a == ')':
            return 1

        elif a == '#':
            return -1
    
    def print_nfa_graph(self):
        '''打印结果'''
        print(' NFA '.center(50, '='))
        print(self.nfa_graph)
        print(''.center(50, '='))

    def get_nfa_graph(self):
        '''获取结果'''
        return self.nfa_graph


if __name__ == '__main__':
    input_str = '(ab|c)*abb'
    print(f"Input: {input_str}")
    rex2nfa = Rex2NFA(input_str)
    rex2nfa.print_nfa_graph()
