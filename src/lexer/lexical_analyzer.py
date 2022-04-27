import os
import sys
import re

sys.path.append(".")
from utils.Configs import Configs
from utils.datastructure import *


class LexicalAnalyzer():
    """词法分析器"""

    def __init__(self,Configs):
        """初始化"""
        self.Configs = Configs
        self.token_line = TokenLine()
        self.token_table = TokenTable()
        self.test = None

    def reset(self):
        self.Configs = Configs
        self.token_line = TokenLine()
        self.token_table = TokenTable()
        self.test = None

    def lexical_analyze(self, test_name, Print, Save):
        self.test = os.path.join(Configs.dir_names['tests'], test_name)
        """词法分析"""
        if not self.test:
            raise Exception("tests is empty!")
        else:
            # for test in self.test:
            self.token_table.reset()
            # self.current_test = test
            with open(self.test) as f:
                file_content = f.read()
            file_content = self._preprocess(file_content)
            raw_lines = file_content.split("\n", -1)
            
            for line_seq, line_content in enumerate(raw_lines):
                if line_content.strip():
                    self._process_line(line_seq, line_content.strip())
        if Print:
            self.print_token_table()
        if Save:
            self.save_token_table()
    def _get_tests(self):
        """获取测试文件"""
        # tests_names = os.listdir(self.Configs.dir_names['tests'])

        # # tests_names.remove(".DS_Store")
        # for tests_name in tests_names[-1:]:
        #     tests.append(os.path.join(self.Configs.dir_names['tests'], tests_name))
        test_name = self.Configs.test_name
        test = os.path.join(self.Configs.dir_names['tests'], test_name)
        return test

    def _preprocess(self, file_content):
        """删除sql的注释"""
        # 状态定义
        STATE_0 = 0	  # 代码
        STATE_1 = 1	  # 斜杠
        STATE_2 = 2	  # 多⾏注释
        STATE_3 = 3   # 多⾏注释遇到* 
        STATE_4 = 4   # 单⾏注释
        STATE_5 = 5	  # 拆⾏注释
        STATE_6 = 6	  # 字符
        STATE_7 = 7   # 字符中的转义字符
        STATE_8 = 8	  # 字符串
        STATE_9 = 9   # 字符串中的转义字符
        STATE_10 = 10 # 短横线

        # 有限状态机
        current_string = ""
        state = STATE_0
        for ch in file_content:
            if state == STATE_0:
                if ch == '/':
                    state = STATE_1
                elif ch == "-":
                    state = STATE_10 
                else:
                    current_string += ch
                    if ch == '\'':
                        state = STATE_6
                    elif ch == '\"':
                        state = STATE_8
            
            elif state == STATE_10:
                if ch == '-':
                    state = STATE_4
                else:
                    current_string += "-" + ch
                    state = STATE_0
            
            elif state == STATE_1:
                if ch == '*':
                    state = STATE_2
                elif ch == '/':
                    state = STATE_4
                else:
                    current_string += "/"
                    current_string += ch
                    state = STATE_0
            
            elif state == STATE_2:
                if ch == '*':
                    state = STATE_3
                else:
                    if ch == '\n':
                        current_string += '\r\n'
                    state = STATE_2
            
            elif state == STATE_3:
                if ch == '/':
                    state = STATE_0
                elif ch == '*':
                    state = STATE_3
                else:
                    state = STATE_2
            
            elif state == STATE_4: 
                if ch == '\\':
                    state = STATE_5
                elif ch == '\n':
                    current_string += '\r\n'
                    state = STATE_0
                else:
                    state = STATE_4
            
            elif state == STATE_5:
                if ch == '\\' or ch == '\r' or ch == '\n':
                    if ch == '\n':
                        current_string += '\r\n'
                    state = STATE_5
                else:
                    state = STATE_4
            
            elif state == STATE_6:
                current_string += ch
                if ch == '\\':
                    state = STATE_7
                elif ch == '\'':
                    state = STATE_0
                else:
                    state = STATE_6
            elif state == STATE_7:
                current_string += ch
                state = STATE_6
            elif state == STATE_8:
                current_string += ch
                if ch == '\\':
                    state = STATE_9
                elif ch == '\"':
                    state = STATE_0
                else:
                    state = STATE_8
            elif state == STATE_9:
                current_string += ch
                state = STATE_8 
        
        return current_string

    def _process_line(self, line_seq, line_content):
        """处理每一行"""
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
            if line_content[i] in self.Configs.letter + "_":
                current_word += line_content[i]
                i += 1

                while i < len(line_content) and line_content[i] in self.Configs.letter + self.Configs.digit + "_":
                    current_word += line_content[i]
                    i += 1

                if current_word == "ORDER":
                    if i + 2 < len(line_content) and line_content[i : i+3] == " BY":
                        current_word += " BY"
                        self._process_word(current_word, "SE+1KW+3OP")
                        current_word = ""
                        i += 3
                    else:
                        print("ERROR ORDER BY")
                        break
                
                elif current_word == "GROUP":
                    if i + 2 < len(line_content) and line_content[i : i+3] == " BY":
                        current_word += " BY"
                        self._process_word(current_word, "SE+1KW+3OP")
                        current_word = ""
                        i += 3
                    else:
                        print("ERROR GROUP BY")
                        break
                
                else:
                    self._process_word(current_word, "kW+IDN+4OP")
                    current_word = ""

            # 单符号
            elif line_content[i] in ["(", ")", ",", "*", "=", "-", "."]:
                current_word += line_content[i]
                self._process_word(current_word, "SE+1KW+3OP")
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
                self._process_word(current_word, "STR")
                current_word = ""
                i += 1

            # > >=
            elif line_content[i] == '>':
                current_word += line_content[i]
                i += 1

                if i < len(line_content) and line_content[i] == '=':
                    current_word += line_content[i]
                    self._process_word(current_word, "OP")
                    current_word = ""
                    i += 1
                else:
                    self._process_word(current_word, "OP")
                    current_word = ""

            # != !
            elif line_content[i] == '!':
                current_word += line_content[i]
                i += 1

                if i < len(line_content) and line_content[i] == '=':
                    current_word += line_content[i]
                    self._process_word(current_word, "OP")
                    current_word = ""
                    i += 1
                else:
                    self._process_word(current_word, "OP")
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
                        self._process_word(current_word, "OP")
                        current_word = ""
                        i += 1
                    else:
                        self._process_word(current_word, "OP")
                        current_word = ""
                else:
                    self._process_word(current_word, "OP")
                    current_word = ""

            # &&
            elif line_content[i] == '&':
                current_word += line_content[i]
                i += 1
                
                if i < len(line_content) and line_content[i] == '&':
                    current_word += line_content[i]
                    self._process_word(current_word, "OP")
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
                    self._process_word(current_word, "OP")
                    current_word = ""
                    i += 1
                else:
                    print("Error |")
                    break
            
            # 数字
            elif line_content[i] in self.Configs.digit:
                current_word += line_content[i]
                i += 1

                while i < len(line_content) and line_content[i] in self.Configs.digit:
                    current_word += line_content[i]
                    i += 1
                
                if i < len(line_content) and line_content[i] == '.':
                    current_word += line_content[i]
                    i += 1
                    while i < len(line_content) and line_content[i] in self.Configs.digit:
                        current_word += line_content[i]
                        i += 1 
                    self._process_word(current_word, "FLOAT")
                    current_word = ""
                else:
                    self._process_word(current_word, "INT")
                    current_word = ""

            else:
                print("Error else")
                break

    def _process_word(self, word_content, word_type):
        """处理并保存单词"""
        self.token_line.input_raw_line(word_content, word_type)
        self.token_table.add_token_line(self.token_line.output_token_line())
    
    def print_token_table(self):
        """打印token表"""
        self.token_table.print()
    
    def save_token_table(self):
        """保存token表"""
        self.token_table.save(self.test)







        
        
        




        

if __name__ == '__main__':
    lex = LexicalAnalyzer(Configs)
    lex.lexical_analyze()
    lex.print_token_table()
    lex.save_token_table()