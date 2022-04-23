import os
import sys

sys.path.append(".")
from utils.utils import *
from utils.datastructure import *


class Regex:
    def __init__(self, regex=None):
        self.input = regex
        self.regex = ""
        self.operatorStack = []
        self.operandStack = []
        self.priority = [
            [1, 1, 1, -1, 1, 1],
            [-1, 1, 1, -1, 1, 1], [-1, -1, 1, -1, 1, 1],
            [-1, -1, -1, -1, 0, 2], [1, 1, 1, 1, 1, 1],
            [-1, -1, -1, -1, -1, -1]
        ]
        self.prepare_string(_regex=regex)

    def transformNFA(self):
        print("Input: {}".format(self.input))
        print("Processed Input: {}".format(self.regex))
        if not self.regex:
            return None
        else:
            self.operatorStack.append("#")
            i = 0
            _regex = [x for x in self.regex] + ['#']
            print("Regex: {} ".format(_regex))
            while _regex[i] != '#' or self.operatorStack[-1] != '#':
                if not self.is_operator(ch=_regex[i]):
                    self.operandStack.append(_regex[i])
                    i += 1
                else:
                    value = self.priority_operator(self.operatorStack[-1], _regex[i])
                    if value == 1:
                        ch = self.operatorStack.pop()
                        if ch == '*':
                            obj = self.operandStack.pop()
                            graph1 = Graph()
                            graph1.add_star(obj=obj)
                            self.operandStack.append(graph1)
                        elif ch == '&':

                            obj2 = self.operandStack.pop()
                            obj1 = self.operandStack.pop()
                            graph2 = Graph()
                            graph2.add_concat(obj1=obj1, obj2=obj2)

                            self.operandStack.append(graph2)
                        elif ch == '|':
                            obj4 = self.operandStack.pop()
                            obj3 = self.operandStack.pop()
                            graph3 = Graph()

                            graph3.add_union(obj1=obj3, obj2=obj4)

                            self.operandStack.append(graph3)
                        else:
                            pass

                    elif value == 0:
                        self.operatorStack.pop()
                        i += 1
                        pass
                    elif value == -1:
                        self.operatorStack.append(_regex[i])
                        i += 1
                        pass
                    else:
                        pass
            print(" Finish transformation from regex to nfa ".center(50, '='))
            if len(self.operandStack):
                print(self.operandStack[-1])
                return self.operandStack[-1]
            else:
                return None

    def is_operator(self, ch=None):
        return ch in ['*', '&', '|', '(', ')', '#']

    def priority_operator(self, ch1=None, ch2=None):
        priority_str = '*&|()#'
        return self.priority[priority_str.find(ch1)][priority_str.find(ch2)]

    # 添加连接符
    # (a|b)*abb转换成 (a|b)*&a&b&b
    def prepare_string(self, _regex=None):
        self.regex = ""
        temp = [x for x in _regex if x != " "]
        _regex = temp
        for i in range(len(_regex)):
            if i == 0:
                self.regex += _regex[i]
            else:
                if _regex[i] == '|' or _regex[i] == '*' or _regex[i] == ')':
                    self.regex += _regex[i]
                else:
                    if _regex[i - 1] == '(' or _regex[i - 1] == '|':
                        self.regex += _regex[i]
                    else:
                        self.regex += ('&' + _regex[i])


if __name__ == '__main__':
    regex_string = '(ab|c)*abb'
    regexer = Regex(regex=regex_string)
    regexer.transformNFA()
