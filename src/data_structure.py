grammar_path = './docs/grammar.txt'
import copy as cp
from turtle import left, right

from aem import con


class production():
    def __init__(self, left, right, index):
        self.left = left
        self.right = right
        self.index = index

class grammar():
    def __init__(self, grammar_file_path):
        # grammar quadruple
        self.non_terminals = []
        self.terminals = []
        self.productions = []
        self.start = None
        
        self.grammar_content = None
        self.load_grammar(grammar_file_path)
    
    # Load the grammar from the file
    def load_grammar(self, grammar_file_path):
        
        with open(grammar_file_path, 'r') as f:
            self.grammar_content = f.readlines()
            
        all_symbols = [] # All symbols in the grammar
        
        for index, line in enumerate(self.grammar_content): # Loop through the lines
            line = line[:-1] # remove \n
            words = line.split(' ')  # split the line by space
            self.productions.append(production(words[1], words[3:], index)) # Add the production to the list
                                                                            # index starts from 0
            self.non_terminals.append(words[1]) # Add the non-terminal to the list
            all_symbols.extend(list(words[1]) + words[3:]) # Add the symbols to the list
            
        self.non_terminals = list(set(self.non_terminals)) # Remove duplicates
        all_symbols = list(set(all_symbols)) # Remove duplicates
        self.terminals = list((set(all_symbols) - set(self.non_terminals))) # Get the terminals
        self.start = self.productions[0].left # Set the start symbol

class FIRST():
    def __init__(self):
        self.first_dict = {}
        
    def get_first(self, non_terminals, terminals, productions):
        # Initialize the first set
        for symbol in non_terminals:
            self.first_dict[symbol] = [] 
        for symbol in terminals:
            self.first_dict[symbol] = [symbol]
            
        while True:
            changed = False # Flag to check if the FIRST sets has changed

            for production in productions:
                left_symbol = production.left
                right_symbols = cp.deepcopy(production.right)
                
                before_len = len(self.first_dict[production.left])
                while True:
                    
                    if len(right_symbols) == 0:
                        self.first_dict[left_symbol].append('$')
                        break
                    tmp_symbol = right_symbols[0]
                    # If the production is a terminal, then add it to the first set of the left side
                    if tmp_symbol in terminals:
                        self.first_dict[left_symbol].append(tmp_symbol)
                        right_symbols.remove(tmp_symbol)
                        break # If the production is a terminal, then break
                    # If the production is a non-terminal, then add the first set of the right side[0] (except epsilon) to the first set of left side
                    if tmp_symbol in non_terminals:
                        if '$' in right_symbols:
                            self.first_dict[left_symbol].extend(list(set(self.first_dict[tmp_symbol]) - set(['$'])))
                            continue # If the first dict of the right side[0] include epsilon, then continue
                        else:
                            self.first_dict[left_symbol].extend(self.first_dict[tmp_symbol])
                            break # If the first dict of the right side[0] doesn't include epsilon, then break
                
                self.first_dict[left_symbol] = list(set(self.first_dict[left_symbol]))
                
                after_len = len(self.first_dict[left_symbol])
                
                if after_len > before_len: # If the first set of the left side is changed, then changed is True
                    changed = True
                    
            if not changed: # Loop until all the first sets don't changed
                break
            
    def dump_first_sets_into_file(self, file_path):
        pass

class FOLLOW():
    def __init__(self, grammar):
        self.follow_dict = {}
    def get_follow(self, non_terminals, terminals, productions, start, firstSets):
        # Initialize the follow set
        for symbol in non_terminals:
            self.follow_dict[symbol] = []
        self.follow_dict[start].append('#') # Add # to the follow set of the start symbol
        
        while True:
            changed = False # Flag to check if the FOLLOW sets has changed
            for symbol in non_terminals:
                before_len = len(self.follow_dict[symbol])
                for production in productions:
                    left_symbol = production.left
                    right_symbols = cp.deepcopy(production.right)
                    
                    try:
                        idx = right_symbols.index(symbol)
                    except:
                        idx = -1
                    while(idx != -1):
                        # If symbol is the last symbol in the right side, then add the follow set of the left side to the follow set of the symbol
                        flag = True
                        suffix_num = len(right_symbols) - idx - 1
                        cnt = 1
                        while cnt <= suffix_num:
                            if '$' not in right_symbols[idx + cnt]:
                                flag = False
                                break
                            cnt += 1
                        if flag:
                            self.follow_dict[symbol].extend(self.follow_dict[left_symbol])
                        # If the next symbol is a terminal, then add it to the follow set of the symbol
                        elif idx < len(right_symbols) - 1 and right_symbols[idx + 1] in terminals:
                            self.follow_dict[symbol].append(right_symbols[idx + 1])
                            
                        # If the next symbol is a non-terminal, then add the first set of the next symbol except $ to the follow set of the symbol
                        if idx < len(right_symbols) - 1 and right_symbols[idx + 1] in non_terminals:
                            if '$' in firstSets[right_symbols[idx + 1]]:
                                self.follow_dict[symbol].extend(list(set(firstSets[right_symbols[idx + 1]]) - set(['$'])))
                            else:
                                self.follow_dict[symbol].extend(firstSets[right_symbols[idx + 1]])
                        
                        right_symbols.remove(symbol)
                        
                        try:
                            idx = right_symbols.index(symbol)
                        except:
                            idx = -1
                            
                self.follow_dict[symbol] = list(set(self.follow_dict[symbol])) # Remove duplicates
                
                after_len = len(self.follow_dict[symbol])
                if after_len > before_len:  
                    changed = True # If the follow set of the symbol is changed, then changed is True
            
            if not changed: # Loop until all the follow sets don't change
                break
    def dump_follow_sets_into_file(self, file_path):
        pass

class item():
    def __init__(self):
        self.left = None
        self.right = None
        self.dot_pos = None
        self.terminals = []
        pass
    
    
class itemSet():
    def __init__(self):
        self.items = []
        
class actionTable():
    pass

class gotoTable():
    pass

class analysisTable():
    def __init__(self) -> None:
        self.action_table = None
        self.gotoTable = None
        
        
if __name__ == '__main__':
    G = grammar(grammar_path)
    # print(G.non_terminals)
    # print(G.terminals)
    # for production in G.productions:
    #     print(production.left, production.right, production.index)
    # print(G.start)
    FIRST_obj = FIRST()
    FIRST_obj.get_first(G.non_terminals, G.terminals, G.productions)
    # for firstset in FIRST_obj.first_dict.items():
    #     print(firstset)
    FOLLOW_obj = FOLLOW()
    FOLLOW_obj.get_follow(G.non_terminals, G.terminals, G.productions, G.start, FIRST_obj.first_dict)
    for followset in FOLLOW_obj.follow_dict.items():
        print(followset)