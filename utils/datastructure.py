from fileinput import filename
import sys
import os

sys.path.append(".")
from utils.Configs import Configs


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
            if self.word_content in Configs.KW:
                self.token_type = 'KW'
                self.token_content = self._get_token_id(Configs.KW)

            elif self.word_content in Configs.OP:
                self.token_type = 'OP'
                self.token_content = self._get_token_id(Configs.OP)
            
            else:
                self.token_type = 'IDN'
                self.token_content = self.word_content

        elif self.word_type == 'OP':
            self.token_type = 'OP'
            self.token_content = self._get_token_id(Configs.OP)
        
        elif self.word_type == 'KW':
            self.token_type = 'KW'
            self.token_content = self._get_token_id(Configs.KW)
        
        elif self.word_type == 'SE+1KW+3OP':
            if self.word_content in Configs.KW:
                self.token_type = 'KW'
                self.token_content = self._get_token_id(Configs.KW)

            elif self.word_content in Configs.OP:
                self.token_type = 'OP'
                self.token_content = self._get_token_id(Configs.OP)
            
            elif self.word_content in Configs.SE:
                self.token_type = 'SE'
                self.token_content = self._get_token_id(Configs.SE)

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
        save_path = os.path.join(Configs.dir_names['output'], "token_table", file_name)
        with open(save_path, 'w') as f:
            for token_line in self.token_table:
                f.write(token_line + '\n')
    
    def reset(self):
        self.token_table = []



class Node():
    num = 0
    def __init__(self, id=None):
        if id is not None:
            self.id = id
        else:
            self.id = Node.num
            Node.num += 1

    def __str__(self):
        return str(self.id)


class Edge():
    def __init__(self, beginNode=None, endNode=None, label=None):
        self.beginNode = beginNode
        self.endNode = endNode
        self.label = label

    def __str__(self):
        return "Edge [begin={} end={} label={}]".format(str(self.beginNode), str(self.endNode), str(self.label))


class Graph():
    def __init__(self, beginNode=None, endNode=None, endNodes=None):
        self.beginNode = beginNode
        self.endNode = endNode
        self.endNodes = endNodes
        self.edges = []

    def add_star(self, obj=None):
        if isinstance(obj, str):
            centerNode = Node()
            beginNode = Node()
            endNode = Node()

            edgeLink = Edge(beginNode=centerNode, endNode=centerNode, label=str(obj))
            beginEdgeEpsilon = Edge(beginNode=beginNode, endNode=centerNode, label="epsilon")
            endEdgeEpsilon = Edge(beginNode=centerNode, endNode=endNode, label="epsilon")

            self.edges.append(edgeLink)
            self.edges.append(beginEdgeEpsilon)
            self.edges.append(endEdgeEpsilon)

            self.beginNode = beginNode
            self.endNode = endNode

        elif isinstance(obj, Graph):
            beginNode = Node()
            endNode = Node()
            edgeone = Edge(beginNode=beginNode, endNode=endNode, label="epsilon")
            edgetwo = Edge(beginNode=beginNode, endNode=obj.beginNode, label="epsilon")
            edgethree = Edge(beginNode=obj.endNode, endNode=endNode, label="epsilon")
            edgefour = Edge(beginNode=obj.endNode, endNode=obj.beginNode, label="epsilon")

            for edge in obj.edges:
                self.edges.append(edge)

            self.edges.append(edgeone)
            self.edges.append(edgetwo)
            self.edges.append(edgethree)
            self.edges.append(edgefour)

            self.beginNode = beginNode
            self.endNode = endNode

        else:
            print("Unknown type {}".format(type(obj)))
            exit(-1)

    def add_union(self, obj1=None, obj2=None):
        if isinstance(obj1, Graph) and isinstance(obj2, str):
            beginNode = Node()
            endNode = Node()
            edgeone = Edge(beginNode=beginNode, endNode=obj1.beginNode, label="epsilon")
            edgetwo = Edge(beginNode=obj1.endNode, endNode=endNode, label="epsilon")
            edgethree = Edge(beginNode=beginNode, endNode=endNode, label=str(obj2))

            for edge in obj1.edges:
                self.edges.append(edge)

            self.edges.append(edgeone)
            self.edges.append(edgetwo)
            self.edges.append(edgethree)

            self.beginNode = beginNode
            self.endNode = endNode

        elif isinstance(obj1, str) and isinstance(obj2, Graph):
            beginNode = Node()
            endNode = Node()
            edgeone = Edge(beginNode=beginNode, endNode=obj2.beginNode, label="epsilon")
            edgetwo = Edge(beginNode=obj2.endNode, endNode=endNode, label="epsilon")
            edgethree = Edge(beginNode=beginNode, endNode=endNode, label=str(obj1))

            for edge in obj2.edges:
                self.edges.append(edge)

            self.edges.append(edgeone)
            self.edges.append(edgetwo)
            self.edges.append(edgethree)

            self.beginNode = beginNode
            self.endNode = endNode

        elif isinstance(obj1, Graph) and isinstance(obj2, Graph):
            beginNode = Node()
            endNode = Node()
            edgeone = Edge(beginNode=beginNode, endNode=obj1.beginNode, label="epsilon")
            edgetwo = Edge(beginNode=beginNode, endNode=obj2.beginNode, label="epsilon")
            edgethree = Edge(beginNode=obj1.endNode, endNode=endNode, label="epsilon")
            edgefour = Edge(beginNode=obj2.endNode, endNode=endNode, label="epsilon")


            self.beginNode = beginNode
            self.endNode = endNode

            for edge in obj1.edges:
                self.edges.append(edge)

            for edge in obj2.edges:
                self.edges.append(edge)

            self.edges.append(edgeone)
            self.edges.append(edgetwo)
            self.edges.append(edgethree)
            self.edges.append(edgefour)


        elif isinstance(obj1, str) and isinstance(obj2, str):
            beginNode = Node()
            endNode = Node()

            edgeone = Edge(beginNode=beginNode, endNode=endNode, label=str(obj1))
            edgetwo = Edge(beginNode=beginNode, endNode=endNode, label=str(obj2))

            self.edges.append(edgeone)
            self.edges.append(edgetwo)

            self.beginNode = beginNode
            self.endNode = endNode


    def add_concat(self, obj1=None, obj2=None):
        if isinstance(obj1, Graph) and isinstance(obj2, str):
            endNode = Node()
            edgeone = Edge(beginNode=obj1.endNode, endNode=endNode, label=str(obj2))
            for edge in obj1.edges:
                self.edges.append(edge)

            self.edges.append(edgeone)
            self.beginNode = obj1.beginNode
            self.endNode = endNode

        elif isinstance(obj1, str) and isinstance(obj2, Graph):
            beginNode = Node()
            edgeone = Edge(beginNode=beginNode, endNode=obj2.beginNode, label=str(obj1))

            for edge in obj2.edges:
                self.edges.append(edge)

            self.edges.append(edgeone)
            self.beginNode = beginNode
            self.endNode = obj2.endNode

        elif isinstance(obj1, Graph) and isinstance(obj2, Graph):
            edgeone = Edge(beginNode=obj1.endNode, endNode=obj2.beginNode, label="epsilon")
            self.beginNode = obj1.beginNode
            self.endNode = obj2.endNode

            for edge in obj1.edges:
                self.edges.append(edge)

            for edge in obj2.edges:
                self.edges.append(edge)

            self.edges.append(edgeone)

        elif isinstance(obj1, str) and isinstance(obj2, str):
            beginNode = Node()
            centerNode = Node()
            endNode = Node()

            edge1 = Edge(beginNode=beginNode, endNode=centerNode, label=str(obj1))
            edge2 = Edge(beginNode=centerNode, endNode=endNode, label=str(obj2))

            self.beginNode = beginNode
            self.endNode = endNode

            self.edges.append(edge1)
            self.edges.append(edge2)


    def __str__(self):
        if self.endNodes is None:
            return_str = "Start={} EndNode={} \n".format(self.beginNode, self.endNode)
        else:
            return_str = "Start={} EndNodes=[{}] \n".format(self.beginNode, ' '.join([str(node) for node in self.endNodes]))
        for edge in self.edges:
            return_str += str(edge) + '\n'
        return return_str


class StateNode():
    id = 0
    def __init__(self, node_set=None):
        self.node_set = node_set
        self.id = StateNode.id
        self.is_begin = False
        self.is_end = False
        StateNode.id += 1

    def __str__(self):
        return 'StateNode' + str(self.id) +' ' + ''.join([str(x) for x in self.node_set])

