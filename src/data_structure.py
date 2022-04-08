grammar_path = './docs/grammar.txt'
import copy as cp

from more_itertools import first


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
        indexMax = len(self.productions)
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
    def calculate_first_set(self, symbols):
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
    def __init__(self, grammar, first_sets):
        self.follow_dict = {}
        self.calculate_follow(grammar.non_terminals, grammar.terminals, grammar.productions, first_sets)
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
    def __init__(self, left, right, dot_pos, terminals):
        self.left = left
        self.right = right
        self.dot_pos = dot_pos
        self.terminals = terminals
    
    
class itemSets():
    def __init__(self):
        self.item_sets = []
    def calculate_itemSets(self, productions, non_terminals, FIRST, FOLLOW):
        pass
        
    def calculate_closure(self, item_set, productions, non_terminals, FIRST):
        while True:
            before_len = len(item_set)
            for item in item_set:
                if item.dot_pos == len(item.right):
                    continue
                else:
                    dot_right_symbol = item.right[item.dot_pos]
                    if dot_right_symbol in non_terminals:
                        for production in productions:
                            if production.left == dot_right_symbol:
                                symbols = []
                                if not item.dot_pos == len(item.right) - 1:
                                    symbols.append(item.right[item.dot_pos + 1:])
                                symbols.append(item.terminals)
                                first_set = FIRST.calculate_first_set(symbols)
                                tmp_item = item(production.left, production.right, 0, first_set)
                                if tmp_item not in item_set:
                                    item_set.append(tmp_item)
            item_set = list(set(item_set))
            after_len = len(item_set)
            if after_len == before_len:
                break        
        return item_set
        
        
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
    G.get_augumented_grammar()
    print(G.non_terminals)
    print(len(G.non_terminals))
    print(G.terminals)
    print(len(G.terminals))
    for production in G.productions:
        print(production.left, production.right, production.index)
    print(G.start)
    # FIRST_obj = FIRST()
    # FIRST_obj.calculate_first(G.non_terminals, G.terminals, G.productions)
    # for firstset in FIRST_obj.first_dict.items():
    #     print(firstset)
    # print(len(FIRST_obj.first_dict))
    # FOLLOW_obj = FOLLOW()
    # FOLLOW_obj.calculate_follow(G.non_terminals, G.terminals, G.productions, G.start, FIRST_obj.first_dict)
    # for followset in FOLLOW_obj.follow_dict.items():
    #     print(followset)
    # print(len(FOLLOW_obj.follow_dict))