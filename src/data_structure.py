grammar_path = './docs/grammar.txt'
import copy as cp
from enum import Flag
from cv2 import FlannBasedMatcher

from more_itertools import first
from pandas import value_counts


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
            self.productions.append(production(words[1], words[3:], index + 1)) # Add the production to the list
            self.non_terminals.append(words[1]) # Add the non-terminal to the list
            all_symbols.extend([words[1]]+ words[3:]) # Add the symbols to the list
            
        self.non_terminals = list(set(self.non_terminals)) # Remove duplicates
        all_symbols = list(set(all_symbols)) # Remove duplicates
        self.terminals = list((set(all_symbols) - set(self.non_terminals))) # Get the terminals
        self.start = self.productions[0].left # Set the start symbol
    
    def get_augumented_grammar(self):
        self.non_terminals.append('rootP')
        self.start = 'rootP'
        self.productions.insert(0, production('rootP', ['root'], 0))

class FIRST():
    def __init__(self, grammar):
        self.first_dict = {}
        self.grammar = grammar
        self.calculate_first(grammar.non_terminals, grammar.terminals, grammar.productions)
        
    def calculate_first(self, non_terminals, terminals, productions):
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
                        break # If the production is a terminal, then break
                    # If the production is a non-terminal, then add the first set of the right side[0] (except epsilon) to the first set of left side
                    if tmp_symbol in non_terminals:
                        if '$' in self.first_dict[tmp_symbol]:
                            self.first_dict[left_symbol].extend(list(set(self.first_dict[tmp_symbol]) - set(['$'])))
                            right_symbols.remove(tmp_symbol)
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
    def calculate_first_set(self, symbols):
        if symbols == ['#']:
            return ['#']
        if len(symbols) > 1 and '#' in symbols:
            symbols.remove('#')
        first_set = []
        if len(symbols) == 0:
            return first_set
        symbol = symbols[0]
        while True:
            if symbol in self.grammar.terminals:
                first_set.append(symbol)
                break
            else:
                if '$' in self.first_dict[symbol]:
                    first_set.extend(list(set(self.first_dict[symbol]) - set(['$'])))
                    symbols.remove(symbol)
                    if len(symbols) == 0:
                        first_set.append('$')
                        break
                    else:
                        symbol = symbols[0]
                else:
                    first_set.extend(self.first_dict[symbol])
                    break
        first_set = list(set(first_set))
        return first_set
    def dump_first_sets_into_file(self, file_path):
        pass

class FOLLOW():
    def __init__(self, grammar, FIRST):
        self.follow_dict = {}
        self.calculate_follow(grammar.non_terminals, grammar.terminals, grammar.productions, grammar.start, FIRST.first_dict)
    def calculate_follow(self, non_terminals, terminals, productions, start, firstSets):
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
                    if(idx != -1):
                        # If symbol is the last symbol in the right side, then add the follow set of the left side to the follow set of the symbol
                        flag = True
                        suffix_num = len(right_symbols) - idx - 1
                        cnt = 1
                        while cnt <= suffix_num:
                            if '$' not in firstSets[right_symbols[idx + cnt]]:
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
                            idx_right_symbol = right_symbols[idx + 1]
                            while True:
                                if idx_right_symbol in non_terminals and '$' in firstSets[idx_right_symbol]:
                                    self.follow_dict[symbol].extend(list(set(firstSets[idx_right_symbol]) - set(['$'])))
                                    right_symbols.remove(idx_right_symbol)
                                    if idx == len(right_symbols) - 1:
                                        break
                                    else:
                                        idx_right_symbol = right_symbols[idx + 1]
                                elif idx_right_symbol in non_terminals and '$' not in firstSets[idx_right_symbol]:
                                    self.follow_dict[symbol].extend(firstSets[idx_right_symbol])
                                    break
                                elif idx_right_symbol in terminals:
                                    self.follow_dict[symbol].append(idx_right_symbol)
                                    break
                                


                        
                            
                self.follow_dict[symbol] = list(set(self.follow_dict[symbol])) # Remove duplicates
                
                after_len = len(self.follow_dict[symbol])
                if after_len > before_len:  
                    changed = True # If the follow set of the symbol is changed, then changed is True
            
            if not changed: # Loop until all the follow sets don't change
                break
    def dump_follow_sets_into_file(self, file_path):
        pass

class item():
    def __init__(self, left, right, dot_pos, terminals):
        self.left = left
        self.right = right
        self.dot_pos = dot_pos
        self.terminals = terminals
        
    def go(self, terminal_symbol):
        if self.dot_pos > len(self.right) - 1:
            return None
        elif self.right[self.dot_pos] == terminal_symbol:
            return item(self.left, self.right, self.dot_pos + 1, self.terminals)
        else:
            return None
        
    def __eq__(self, __o: object) -> bool:
        return self.__dict__ == __o.__dict__
    
class itemSet():
    def __init__(self, item_set_origin, grammar, FIRST, index):
        self.item_set = self.calculate_closure(item_set_origin, grammar.productions, grammar.non_terminals, FIRST)
        self.index = index
        
    def __eq__(self, __o: object) -> bool:
        return self.item_set == __o.item_set
    
    def calculate_closure(self, item_set_origin, productions, non_terminals, FIRST):
        while True:
            before_len = len(item_set_origin)
            for item_ in item_set_origin:
                if item_.dot_pos == len(item_.right):
                    continue
                else:
                    dot_right_symbol = item_.right[item_.dot_pos]
                    if dot_right_symbol in non_terminals:
                        for production in productions:
                            if production.left == dot_right_symbol:
                                symbols = []
                                if not item_.dot_pos == len(item_.right) - 1:
                                    symbols.extend(item_.right[item_.dot_pos + 1:])
                                symbols.extend(item_.terminals)
                                first_set = FIRST.calculate_first_set(symbols)
                                tmp_item = item(production.left, production.right, 0, first_set)
                                if tmp_item not in item_set_origin:
                                    item_set_origin.append(tmp_item)
            after_len = len(item_set_origin)
            if after_len == before_len:
                break        
        return item_set_origin

class itemSets():
    def __init__(self):
        self.item_sets = []
        self.go = {}
    def calculate_itemSets(self, grammar, FIRST, FOLLOW):
        max_index = 0
        productions = grammar.productions
        non_terminals = grammar.non_terminals
        start_item = item(productions[0].left, productions[0].right, 0, ['#'])
        start_item_set = itemSet([start_item], grammar, FIRST, max_index)
        max_index += 1
        self.item_sets.append(start_item_set)
        
        while True:
            before_len = len(self.item_sets)
            for add_item_set in self.item_sets:
                add_go = self.calculate_go(add_item_set, grammar)
                for key, value in add_go.items():
                    value_closure = itemSet(value, grammar, FIRST, -1)
                    flag = False
                    for ground_key, ground_value in self.go.items():
                        if value_closure == ground_value:
                            self.go[key] = ground_value
                            flag = True
                            break
                    if not flag:
                        value_closure.index = max_index
                        max_index += 1
                        self.go[key] = value_closure
                        self.item_sets.append(value_closure)
            after_len = len(self.item_sets)
            if after_len == before_len:
                break
        self.go_convert()

    def calculate_go(self, itemSet, grammar):
        terminals = grammar.terminals
        non_terminals = grammar.non_terminals
        symbols = terminals + non_terminals
        add_go = {}
        for symbol in symbols:
            for item_ in itemSet.item_set:
                if item_.go(symbol) is not None:
                    if not add_go.__contains__((itemSet.index, symbol)):
                        add_go[(itemSet.index, symbol)] = [item_.go(symbol)]
                    else:
                        add_go[(itemSet.index, symbol)].append(item_.go(symbol))
        return add_go
        
    def go_convert(self):
        new_go = {}
        for key, value in self.go.items():
            new_go[key] = value.index
        self.go = new_go
        
class actionTable():
    pass

class gotoTable():
    pass

class analysisTable():
    def __init__(self) -> None:
        self.action_table = None
        self.gotoTable = None
        
        
if __name__ == '__main__':
    grammar_obj = grammar(grammar_path)
    grammar_obj.get_augumented_grammar()
    # print(G.non_terminals)
    # print(len(G.non_terminals))
    # print(G.terminals)
    # print(len(G.terminals))
    # for production in G.productions:
    #     print(production.left, production.right, production.index)
    # print(G.start)
    FIRST_obj = FIRST(grammar_obj)
    # FIRST_obj.calculate_first(G.non_terminals, G.terminals, G.productions)
    # for firstset in FIRST_obj.first_dict.items():
    #     print(firstset)
    # print(len(FIRST_obj.first_dict))
    FOLLOW_obj = FOLLOW(grammar_obj, FIRST_obj)
    # FOLLOW_obj.calculate_follow(G.non_terminals, G.terminals, G.productions, G.start, FIRST_obj.first_dict)
    # for followset in FOLLOW_obj.follow_dict.items():
    #     print(followset)
    # print(len(FOLLOW_obj.follow_dict))
    itemSets_obj = itemSets()
    itemSets_obj.calculate_itemSets(grammar_obj, FIRST_obj, FOLLOW_obj)
    for item_set_obj in itemSets_obj.item_sets:
        for item in item_set_obj.item_set:
            print(item.left, item.right, item.dot_pos, item.terminals)
        print(item_set_obj.index)
    