import sys
sys.path.append(".")
import copy as cp

from src.LR1_parser.ds.grammar import grammar
from utils.configs import Configs

grammar_path = Configs.grammar_path
first_sets_output_path = Configs.first_sets_output_path
follow_sets_output_path =  Configs.follow_sets_output_path

class FIRST():
    def __init__(self, grammar_obj):
        self.first_sets = {}
        self.grammar_obj = grammar_obj
        self.calculate_first_sets(grammar_obj.non_terminals, grammar_obj.terminals, grammar_obj.productions)
        
    def calculate_first_sets(self, non_terminals, terminals, productions):
        # Initialize the first set
        for symbol in non_terminals:
            self.first_sets[symbol] = [] 
        for symbol in terminals:
            self.first_sets[symbol] = [symbol]
        self.first_sets['#'] = ['#']
        while True:
            changed = False # Flag to check if the FIRST sets has changed

            for production in productions:
                left_symbol = production.left
                right_symbols = cp.deepcopy(production.right)
                
                before_len = len(self.first_sets[production.left])
                while True:
                    
                    if len(right_symbols) == 0:
                        self.first_sets[left_symbol].append('$')
                        break
                    tmp_symbol = right_symbols[0]
                    # If the production is a terminal, then add it to the first set of the left side
                    if tmp_symbol in terminals:
                        self.first_sets[left_symbol].append(tmp_symbol)
                        break # If the production is a terminal, then break
                    # If the production is a non-terminal, then add the first set of the right side[0] (except varepsilon) to the first set of left side
                    if tmp_symbol in non_terminals:
                        if '$' in self.first_sets[tmp_symbol]:
                            self.first_sets[left_symbol].extend(list(set(self.first_sets[tmp_symbol]) - set(['$'])))
                            right_symbols.remove(tmp_symbol)
                            continue # If the first dict of the right side[0] include varepsilon, then continue
                        else:
                            self.first_sets[left_symbol].extend(self.first_sets[tmp_symbol])
                            break # If the first dict of the right side[0] doesn't include varepsilon, then break
                    if tmp_symbol == '$':
                        self.first_sets[left_symbol].append('$')
                        break
                self.first_sets[left_symbol] = list(set(self.first_sets[left_symbol]))
                
                after_len = len(self.first_sets[left_symbol])
                
                if after_len > before_len: # If the first set of the left side is changed, then changed is True
                    changed = True
                    
            if not changed: # Loop until all the first sets don't changed
                break
            
    def calculate_first_set(self, symbols):
        first_set = []
        terminals = self.grammar_obj.terminals + ['$']
        if len(symbols) == 0:
            return first_set
        symbol = symbols[0]
        while True:
            if symbol == '$':
                first_set.append('$')
                break
            elif symbol in terminals:
                first_set.append(symbol)
                break
            else:
                if '$' in self.first_sets[symbol]:
                    first_set.extend(list(set(self.first_sets[symbol]) - set(['$'])))
                    symbols.remove(symbol)
                    if len(symbols) == 0:
                        first_set.append('$')
                        break
                    else:
                        symbol = symbols[0]
                else:
                    first_set.extend(self.first_sets[symbol])
                    break
        first_set = list(set(first_set))
        return first_set
    
    def dump_first_sets_into_file(self, file_path):
        output_file = open(file_path, 'w')
        output_file.write('FIRST:\n')
        
        output_list = list(self.first_sets.items())
        output_list.sort()
        for first_set in output_list:
            output_file.write('  '+ first_set[0] + '=' + str(first_set[1]) + '\n')
        output_file.close()

class FOLLOW():
    def __init__(self, grammar_obj, FIRST_obj):
        self.follow_sets = {}
        self.calculate_follow(grammar_obj.non_terminals, grammar_obj.terminals, grammar_obj.productions, grammar_obj.start, FIRST_obj.first_sets)
    def calculate_follow(self, non_terminals, terminals, productions, start, first_sets):
        # Initialize the follow set
        for symbol in non_terminals:
            self.follow_sets[symbol] = []
        self.follow_sets[start].append('#') # Add # to the follow set of the start symbol
        
        while True:
            changed = False # Flag to check if the FOLLOW sets has changed
            for symbol in non_terminals:
                before_len = len(self.follow_sets[symbol])
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
                            if '$' not in first_sets[right_symbols[idx + cnt]]:
                                flag = False
                                break
                            cnt += 1
                        if flag:
                            self.follow_sets[symbol].extend(self.follow_sets[left_symbol])
                        # If the next symbol is a terminal, then add it to the follow set of the symbol
                        elif idx < len(right_symbols) - 1 and right_symbols[idx + 1] in terminals:
                            self.follow_sets[symbol].append(right_symbols[idx + 1])
                        # If the next symbol is a non-terminal, then add the first set of the next symbol except $ to the follow set of the symbol
                        if idx < len(right_symbols) - 1 and right_symbols[idx + 1] in non_terminals:
                            idx_right_symbol = right_symbols[idx + 1]
                            while True:
                                if idx_right_symbol in non_terminals and '$' in first_sets[idx_right_symbol]:
                                    self.follow_sets[symbol].extend(list(set(first_sets[idx_right_symbol]) - set(['$'])))
                                    right_symbols.remove(idx_right_symbol)
                                    if idx == len(right_symbols) - 1:
                                        break
                                    else:
                                        idx_right_symbol = right_symbols[idx + 1]
                                elif idx_right_symbol in non_terminals and '$' not in first_sets[idx_right_symbol]:
                                    self.follow_sets[symbol].extend(first_sets[idx_right_symbol])
                                    break
                                elif idx_right_symbol in terminals:
                                    self.follow_sets[symbol].append(idx_right_symbol)
                                    break
                                
                            
                self.follow_sets[symbol] = list(set(self.follow_sets[symbol])) # Remove duplicates
                
                after_len = len(self.follow_sets[symbol])
                if after_len > before_len:  
                    changed = True # If the follow set of the symbol is changed, then changed is True
            
            if not changed: # Loop until all the follow sets don't change
                break

    def dump_follow_sets_into_file(self, file_path):
        output_file = open(file_path, 'w')
        output_file.write('FOLLOW:\n')
        
        output_list = list(self.follow_sets.items())
        output_list.sort()
        for follow_set in output_list:
            output_file.write('  '+ follow_set[0] + '=' + str(follow_set[1]) + '\n')
        output_file.close()
        pass


if __name__ == '__main__':
    grammar_obj = grammar(grammar_path)
    grammar_obj.get_augumented_grammar()
    FIRST_obj = FIRST(grammar_obj)
    # for firstset in FIRST_obj.first_sets.items():
    #     print(firstset)
    # print(len(FIRST_obj.first_sets))
    FOLLOW_obj = FOLLOW(grammar_obj, FIRST_obj)
    # for followset in FOLLOW_obj.follow_sets.items():
    #     print(followset)
    # print(len(FOLLOW_obj.follow_sets))
    FIRST_obj.dump_first_sets_into_file(first_sets_output_path)
    FOLLOW_obj.dump_follow_sets_into_file(follow_sets_output_path)
