import sys
sys.path.append(".")
from utils.Configs import Configs

grammar_path = Configs.grammar_path

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
            if 'whereExpressio' in words:
                while 1:
                    pass
            self.productions.append(production(words[1], words[3:], index + 1)) # Add the production to the list
            self.non_terminals.append(words[1]) # Add the non-terminal to the list
            all_symbols.extend([words[1]]+ words[3:]) # Add the symbols to the list
            
        self.non_terminals = list(set(self.non_terminals)) # Remove duplicates
        all_symbols = list(set(all_symbols)) # Remove duplicates
        self.terminals = list((set(all_symbols) - set(self.non_terminals))) # Get the terminals
        if '$' in self.terminals:
            self.terminals.remove('$')
        self.start = self.productions[0].left # Set the start symbol
        
        self.terminals.sort()
        self.non_terminals.sort()
        
    def get_augumented_grammar(self):
        self.non_terminals.append('rootp')
        self.start = 'rootp'
        self.productions.insert(0, production('rootp', ['root'], 0))


if __name__ == '__main__':
    grammar_obj = grammar(grammar_path)
    grammar_obj.get_augumented_grammar()
    print(grammar_obj.non_terminals)
    print(len(grammar_obj.non_terminals))
    print(grammar_obj.terminals)
    print(len(grammar_obj.terminals))
    for production in grammar_obj.productions:
        print(production.left, production.right, production.index)
    print(grammar_obj.start)