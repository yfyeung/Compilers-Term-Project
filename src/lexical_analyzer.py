import os
import sys
import re

sys.path.append(".")
from utils.utils import *
from utils.datastructure import *


class LexicalAnalyzer():
    """词法分析器"""

    def __init__(self):  
        self.token_line = TokenLine()
        self.token_table = TokenTable()
        self.tests = self._get_tests()
        self.current_test = None

    def lexical_analyze(self):
        if not self.tests:
            raise Exception("tests is empty!")
        else:
            for test in self.tests[:1]:
                self.token_table.reset()
                self.current_test = test
                with open(test) as f:
                    file_content = f.read()
                file_content = self._preprocess(file_content)
                raw_lines = file_content.split("\n", -1)
                
                for line_seq, line_content in enumerate(raw_lines):
                    if line_content.strip():
                        self._process_line(line_seq, line_content.strip())

    def _get_tests(self):
        tests = []
        tests_names = os.listdir(dir_names['tests'])
        tests_names.remove(".DS_Store")
        for tests_name in tests_names:
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

    def _process_line(self, line_seq, line_content):

        if line_content is None:
            return
        
        current_word = ""
        i = 0
        
        while i < len(line_content):
            if line_content[i] == " ":
                i += 1
                continue
            if line_content[i] == "\n":
                return

            # KW IDN AND OR XOR NOT
            if line_content[i] in letter + "_":
                current_word += line_content[i]
                i += 1

                while i < len(line_content) and line_content[i] in letter + digit + "_":
                    current_word += line_content[i]
                    i += 1

                if current_word == "ORDER":
                    if i + 2 < len(line_content) and line_content[i : i+3] == " BY":
                        current_word += " BY"
                        self.save_word(current_word, "SE+1KW+3OP")
                        current_word = ""
                        i += 3
                    else:
                        print("ERROR ORDER BY")
                        break
                
                else:
                    self.save_word(current_word, "kW+IDN+4OP")
                    current_word = ""

            # 单符号
            elif line_content[i] in ["(", ")", ",", "*", "=", "-", "."]:
                current_word += line_content[i]
                self.save_word(current_word, "SE+1KW+3OP")
                current_word = ""
                i += 1
            
            # 字符串
            elif line_content[i] == '"':
                current_word += line_content[i]
                i += 1

                while line_content[i] != '"':
                    current_word += line_content[i]
                    i += 1
                
                current_word += line_content[i]
                self.save_word(current_word, "STR")
                current_word = ""
                i += 1

            # > >=
            elif line_content[i] == '>':
                current_word += line_content[i]
                i += 1

                if i < len(line_content) and line_content[i] == '=':
                    current_word += line_content[i]
                    self.save_word(current_word, "OP")
                    current_word = ""
                    i += 1
                else:
                    self.save_word(current_word, "OP")
                    current_word = ""

            # != !
            elif line_content[i] == '!':
                current_word += line_content[i]
                i += 1

                if i < len(line_content) and line_content[i] == '=':
                    current_word += line_content[i]
                    self.save_word(current_word, "OP")
                    current_word = ""
                    i += 1
                else:
                    self.save_word(current_word, "OP")
                    current_word = ""

            # < <= <=>
            elif line_content[i] == '<':
                current_word += line_content[i]
                i += 1

                if i < len(line_content) and line_content[i] == '=':
                    current_word += line_content[i]
                    i += 1
                    if line_content[i] == '>':
                        current_word += line_content[i]
                        self.save_word(current_word, "OP")
                        current_word = ""
                        i += 1
                    else:
                        self.save_word(current_word, "OP")
                        current_word = ""
                else:
                    self.save_word(current_word, "OP")
                    current_word = ""

            # &&
            elif line_content[i] == '&':
                current_word += line_content[i]
                i += 1
                
                if i < len(line_content) and line_content[i] == '&':
                    current_word += line_content[i]
                    self.save_word(current_word, "OP")
                    current_word = ""
                    i += 1
                else:
                    print("Error &")
                    break
            
            # ||
            elif line_content[i] == '|':
                current_word += line_content[i]
                i += 1
                
                if i < len(line_content) and line_content[i] == '|':
                    current_word += line_content[i]
                    self.save_word(current_word, "OP")
                    current_word = ""
                    i += 1
                else:
                    print("Error |")
                    break
            
            # 数字
            elif line_content[i] in digit:
                current_word += line_content[i]
                i += 1

                while i < len(line_content) and line_content[i] in digit:
                    current_word += line_content[i]
                    i += 1
                
                if i < len(line_content) and line_content[i] == '.':
                    current_word += line_content[i]
                    i += 1
                    while i < len(line_content) and line_content[i] in digit:
                        current_word += line_content[i]
                        i += 1 
                    self.save_word(current_word, "FLOAT")
                    current_word = ""
                else:
                    self.save_word(current_word, "INT")
                    current_word = ""

            else:
                print("Error else")
                break

    def save_word(self, word_content, word_type):
        self.token_line.input_raw_line(word_content, word_type)
        self.token_table.add_token_line(self.token_line.output_token_line())
    
    def print_token_table(self):
        self.token_table.print()
    
    def save_token_table(self):
        self.token_table.save(self.current_test)







        
        
        




        

if __name__ == '__main__':
    lex = LexicalAnalyzer()
    lex.lexical_analyze()
    lex.print_token_table()
    lex.save_token_table()