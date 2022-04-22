import sys
import os

sys.path.append(".")
from utils.utils import *


class TokenLine():
    def __init__(self, word_content=None, word_type=None):
        self.word_content = None
        self.word_type = None
        self.token_type = None
        self.token_content = None
    
    def __str__(self):
        return f'{self.word_content}   <{self.token_type},{self.token_content}>'
    
    def input_raw_line(self, word_content, word_type):
        self.word_content = word_content
        self.word_type = word_type
        self._process_raw_line()

    def output_token_line(self):
        return f'{self.word_content}   <{self.token_type},{self.token_content}>'
    
    def _process_raw_line(self):
        if self.word_type == 'kW+IDN+4OP':
            if self.word_content in KW:
                self.token_type = 'KW'
                self.token_content = self._get_token_id(KW)

            elif self.word_content in OP:
                self.token_type = 'OP'
                self.token_content = self._get_token_id(OP)
            
            else:
                self.token_type = 'IDN'
                self.token_content = self.word_content

        elif self.word_type == 'OP':
            self.token_type = 'OP'
            self.token_content = self._get_token_id(OP)
        
        elif self.word_type == 'KW':
            self.token_type = 'KW'
            self.token_content = self._get_token_id(KW)
        
        elif self.word_type == 'SE+1KW+3OP':
            if self.word_content in KW:
                self.token_type = 'KW'
                self.token_content = self._get_token_id(KW)

            elif self.word_content in OP:
                self.token_type = 'OP'
                self.token_content = self._get_token_id(OP)
            
            elif self.word_content in SE:
                self.token_type = 'SE'
                self.token_content = self._get_token_id(SE)

            else:
                print(self.word_content)
                print("ERROR in _process_raw_line(), SE+1KW+3OP NOT FOUND")
        
        elif self.word_type == 'STR':
            self.token_type = 'STR'
            self.token_content = self.word_content

        elif self.word_type == 'INT':
            self.token_type = 'INT'
            self.token_content = self.word_content
        
        elif self.word_type == 'FLOAT':
            self.token_type = 'FLOAT'
            self.token_content = self.word_content
        
        else:
            print(self.word_type)
            print("ERROR in _process_raw_line(), NOT TYPE MATCH")
    
    def _get_token_id(self, token_type):
        for i, op in enumerate(token_type):
            if op == self.word_content:
                return i + 1

class TokenTable():      
    def __init__(self):
        self.token_table = []
    
    def add_token_line(self, toke_line):
        self.token_table.append(toke_line)
    
    def print(self):
        for token_line in self.token_table:
            print(token_line)
    
    def save(self, test_name):
        file_name = 'token_table_' + test_name.replace("tests/", "").replace(".sql", ".txt")
        save_path = os.path.join(dir_names['output'], file_name)
        with open(save_path, 'w') as f:
            for token_line in self.token_table:
                f.write(token_line + '\n')
    
    def reset(self):
        self.token_table = []


class Node():
    def __init__(self, id):
        self.id = id

    def __str__(self):
        return str(self.id)


class Edge():
    def __init__(self, begin, end, weight=None):
        self.begin = begin
        self.end = end
        self.weight = weight

    def __str__(self):
        return f"weight:{weight}, begin:{begin}, end:{end}"


class Graph():
    def __init__(self, source, terminal, endNodes):
        self.source = source
        self.terminal = terminal
        self.endNodes = endNodes
        self.edges = []

    def __str__(self):
        if self.endNodes is None:
            return_str = "Start={} EndNode={} \n".format(self.beginNode, self.endNode)
        else:
            return_str = "Start={} EndNodes=[{}] \n".format(self.beginNode, ' '.join([str(node) for node in self.endNodes]))
        for edge in self.edges:
            return_str += str(edge) + '\n'
        return return_str