import os
import sys
import re

sys.path.append(".")
from utils.utils import *


class LexicalAnalyzer():
    """词法分析器"""

    def __init__(self):  
        self.KW = KW
        self.OP = OP
        self.SE = SE
        self.VOCABULARY = VOCABULARY

        self.Token = []
        self.tests = self._get_tests()


    def lexical_analyze(self):
        self._get_tests()
        if not self.tests:
            raise Exception("tests is empty!")
        else:
            for test in self.tests:
                with open(test) as f:
                    file_content = f.read()
                file_content = self._preprocess(file_content)
                print(file_content)
                # for line_seq, line_content in enumerate(lines):
                #     if line_content.rstrip():
                #         self._preprocess(line_seq, line_content.rstrip())

    def _get_tests(self):
        tests = []
        tests_names = os.listdir(dir_names['tests'])
        tests_names.remove(".DS_Store")
        for tests_name in tests_names[-1:]:
            tests.append(os.path.join(dir_names['tests'], tests_name))
        return tests

    def _preprocess(self, file_content):
        """删除sql的注释"""
        # 状态定义
        CODE = 0	               # 代码
        SLASH = 1	               # 斜杠
        ANNOTATION_MULTI = 2	   # 多⾏注释
        ANNOTATION_MULTI_STAR = 3  # 多⾏注释遇到* 
        ANNOTATION_SINGLELINE = 4  # 单⾏注释
        BACKSLASH = 5	           # 拆⾏注释
        CODE_CHAR = 6	           # 字符
        CHAR_ESCAPE_SEQUENCE = 7   # 字符中的转义字符
        CODE_STRING = 8	           # 字符串
        STRING_ESCAPE_SEQUENCE = 9 # 字符串中的转义字符
        STRIGULA = 10	           # 短横线

        # 有限状态机
        s = ""
        state = CODE
        for c in file_content:
            if state == CODE:
                if c == '/':
                    state = SLASH
                elif c == "-":
                    state = STRIGULA 
                else:
                    s += c
                    if c == '\'':
                        state = CODE_CHAR
                    elif c == '\"':
                        state = CODE_STRING
            
            elif state == STRIGULA:
                if c == '-':
                    state = ANNOTATION_SINGLELINE
                else:
                    s += "-" + c
                    state = CODE
            
            elif state == SLASH:
                if c == '*':
                    state = ANNOTATION_MULTI
                elif c == '/':
                    state = ANNOTATION_SINGLELINE
                else:
                    s += "/"
                    s += c
                    state = CODE
            
            elif state == ANNOTATION_MULTI:
                if c == '*':
                    state = ANNOTATION_MULTI_STAR
                else:
                    if c == '\n':
                        s += '\r\n'
                    state = ANNOTATION_MULTI
            
            elif state == ANNOTATION_MULTI_STAR:
                if c == '/':
                    state = CODE
                elif c == '*':
                    state = ANNOTATION_MULTI_STAR
                else:
                    state = ANNOTATION_MULTI
            
            elif state == ANNOTATION_SINGLELINE: 
                if c == '\\':
                    state = BACKSLASH
                elif c == '\n':
                    s += '\r\n'
                    state = CODE
                else:
                    state = ANNOTATION_SINGLELINE
            
            elif state == BACKSLASH:
                if c == '\\' or c == '\r' or c == '\n':
                    if c == '\n':
                        s += '\r\n'
                    state = BACKSLASH
                else:
                    state = ANNOTATION_SINGLELINE
            
            elif state == CODE_CHAR:
                s += c
                if c == '\\':
                    state = CHAR_ESCAPE_SEQUENCE
                elif c == '\'':
                    state = CODE
                else:
                    state = CODE_CHAR
            elif state == CHAR_ESCAPE_SEQUENCE:
                s += c
                state = CODE_CHAR
            elif state == CODE_STRING:
                s += c
                if c == '\\':
                    state = STRING_ESCAPE_SEQUENCE
                elif c == '\"':
                    state = CODE
                else:
                    state = CODE_STRING
            elif state == STRING_ESCAPE_SEQUENCE:
                s += c
                state = CODE_STRING 
        
        return s
        


if __name__ == '__main__':
    lex = LexicalAnalyzer()
    lex.lexical_analyze()