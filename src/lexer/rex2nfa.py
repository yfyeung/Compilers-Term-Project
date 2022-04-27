import os
import sys

sys.path.append(".")
from utils.Configs import Configs
from utils.datastructure import *


class Rex2Nfa:
    def __init__(self, raw_regex):
        self.raw_regex = raw_regex
        self.preprocess_regex = self._preprocess(self.raw_regex)
        self.regex = self._rex2nfa(self.preprocess_regex)

    def _preprocess(self, raw_regex):
        preprocess_regex = ""
        raw_regex = list(raw_regex)
        for i in range(len(raw_regex)):
            if i != 0:
                if raw_regex[i] == '*' or raw_regex[i] == '|' or raw_regex[i] == ')':
                    preprocess_regex += raw_regex[i]
                else:
                    if raw_regex[i-1] == '|' or raw_regex[i-1] == '(':
                        preprocess_regex += raw_regex[i]
                    else:
                        preprocess_regex += '&' 
                        preprocess_regex += raw_regex[i]
            else:
                preprocess_regex += raw_regex[i]
    
        return preprocess_regex

    def _rex2nfa(self, preprocess_regex):
        OPTR = []
        OPND = []

        if not preprocess_regex:
            raise Exception("raw_regex is empty!")
        
        OPTR.append("#")
        regex = list(preprocess_regex) + ['#']

        i = 0
        while not (OPTR[-1] == '#' and regex[i] == '#'):
            if not self._isOperator(regex[i]):
                OPND.append(regex[i])
                i += 1

            else:
                if self._priority_cmp(OPTR[-1], regex[i]) == -1:
                    OPTR.append(regex[i])
                    i += 1
    
                elif self._priority_cmp(OPTR[-1], regex[i]) == 0:
                    OPTR.pop()
                    i += 1

                elif self._priority_cmp(OPTR[-1], regex[i]) == 1:
                    ch = OPTR.pop()

                    MyGraph = Graph()
                    if ch == '&':
                        b = OPND.pop()
                        a = OPND.pop()
                        MyGraph.add_concat(a, b)
                        
                    elif ch == '*':
                        a = OPND.pop()
                        MyGraph.add_star(a)

                    elif ch == '|':
                        b = OPND.pop()
                        a = OPND.pop()
                        MyGraph.add_union(a, b)

                    OPND.append(MyGraph)

        if len(OPND):
            print(OPND[-1])
            return OPND[-1]

    def _isOperator(self, ch):
        if ch in ['*', '&', '|', '(', ')', '#']:
            return True
        else:
            return False

    def _priority_cmp(self, a, b):
        if a == '*':
            if b == '*':
                return 1
            elif b == '&':
                return 1
            elif b == '|':
                return 1
            elif b == '(':
                return -1
            elif b == ')':
                return 1
            elif b == '#':
                return 1
                
        elif a == '&':
            if b == '*':
                return -1
            elif b == '&':
                return 1
            elif b == '|':
                return 1
            elif b == '(':
                return -1
            elif b == ')':
                return 1
            elif b == '#':
                return 1

        elif a == '|':
            if b == '*':
                return -1
            elif b == '&':
                return -1
            elif b == '|':
                return 1
            elif b == '(':
                return -1
            elif b == ')':
                return 1
            elif b == '#':
                return 1

        elif a == '(':
            if b == '*':
                return -1
            elif b == '&':
                return -1
            elif b == '|':
                return -1
            elif b == '(':
                return -1
            elif b == ')':
                return 0
            elif b == '#':
                return 2

        elif a == ')':
            if b == '*':
                return 1
            elif b == '&':
                return 1
            elif b == '|':
                return 1
            elif b == '(':
                return 1
            elif b == ')':
                return 1
            elif b == '#':
                return 1

        elif a == '#':
            if b == '*':
                return -1
            elif b == '&':
                return -1
            elif b == '|':
                return -1
            elif b == '(':
                return -1
            elif b == ')':
                return -1
            elif b == '#':
                return -1



if __name__ == '__main__':
    demo = "a|b*abb"
    print(f"Input: {demo}")
    
    regexer = Rex2Nfa('(ab|c)*abb')
    
