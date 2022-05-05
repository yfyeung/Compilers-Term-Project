from .grammar import grammar
from .FF import FIRST, FOLLOW
from .item import itemSets
from utils.Configs import Configs

grammar_path = Configs.grammar_path
action_table_path = Configs.action_table_path
goto_table_path = Configs.goto_table_path

class actionTable():
    def __init__(self, grammar_obj, itemSets_obj):
        self.action_table = {}
        self.calculate_action_table(grammar_obj, itemSets_obj)
    def calculate_action_table(self, grammar_obj, itemSets_obj):
        state_num = len(itemSets_obj.item_sets)
        for terminal in grammar_obj.terminals + ['#']:
            for state in range(state_num):
                self.action_table[(state, terminal)] = None
        for I in itemSets_obj.item_sets:
            item_set = I.item_set
            index = I.index
            if index == 213:
                a = 1
            go_from_I = [(i, j) for i, j in itemSets_obj.go.items() if i[0] == index]
            for go in go_from_I:
                if go[0][1] in grammar_obj.terminals:
                    if not self.action_table.__contains__((index, go[0][1])):
                        print('Error: action table does\'t have the key: ', (index, go[0][1]))
                        exit(-1)  
                    elif self.action_table[(index, go[0][1])] is not None:
                        print('Error: action table confliction at: ', (index, go[0][1]))
                        exit(-1)  
                    self.action_table[(index, go[0][1])] = "s" + str(go[1])
            for item_ in item_set:
                
                if item_.dot_pos == len(item_.right):
                    for terminal in item_.terminals:
                        if not self.action_table.__contains__((index, terminal)):
                            print('Error: action table does\'t have the key: ', (index, terminal), "Abort!")
                            exit(-1)  
                        elif self.action_table[(index, terminal)] is not None:
                            if self.action_table[(index, terminal)][0] == 's':
                                continue
                            else:
                                print('Error: action table confliction at: ', (index, terminal), "Abort!")
                                exit(-1)
                        self.action_table[(index, terminal)] = "r" + str(item_.index)
                if item_.left == grammar_obj.start and item_.right == ['root'] and item_.dot_pos == len(item_.right) and '#' in item_.terminals:
                    self.action_table[(index, '#')] = "acc"
        
    def dump_table_into_file(self, file_path):
        output_file = open(file_path, 'w')
        output_file.write('action table:\n')
        
        output_list = list(self.action_table.items())
        output_list.sort()
        for action in output_list:
            output_file.write('  '+ str(action[0]) + '  ---->  ' + str(action[1]) + '\n')
        output_file.close()

class gotoTable():
    def __init__(self, grammar_obj, itemSets_obj):
        self.goto_table = {}
        self.calculate_goto_table(grammar_obj, itemSets_obj)
    def calculate_goto_table(self, grammar_obj, itemSets_obj):
        state_num = len(itemSets_obj.item_sets) # number of states
        for non_terminal in grammar_obj.non_terminals: 
            for state in range(state_num): 
                self.goto_table[(state, non_terminal)] = None
        for I in itemSets_obj.item_sets:
            index = I.index
            go_from_I = [(i, j) for i, j in itemSets_obj.go.items() if i[0] == index]
            for go in go_from_I:
                if go[0][1] in grammar_obj.non_terminals:
                    if not self.goto_table.__contains__((index, go[0][1])):
                        print('Error: goto table does\'t have the key: ', (index, go[0][1]), "Abort!")
                        exit(-1)  
                    elif self.goto_table[(index, go[0][1])] is not None:
                        print('Error: goto table confliction at: ', (index, go[0][1]), "Abort!")
                        exit(-1)  
                    self.goto_table[(index, go[0][1])] = "s" + str(go[1])
                    
    def dump_table_into_file(self, file_path):
        output_file = open(file_path, 'w')
        output_file.write('goto table:\n')
        
        output_list = list(self.goto_table.items())
        output_list.sort()
        for goto in output_list:
            output_file.write('  '+ str(goto[0]) + '  ---->  ' + str(goto[1]) + '\n')
        output_file.close()

        
class analysisTable():
    def __init__(self, grammar_obj, itemSets_obj):
        self.action_table = actionTable(grammar_obj, itemSets_obj)
        self.gotoTable = gotoTable(grammar_obj, itemSets_obj)
        
    def dump_table_into_file(self, action_table_path, goto_table_path): # dump action and goto table into files
        self.action_table.dump_table_into_file(action_table_path)
        self.gotoTable.dump_table_into_file(goto_table_path)


if __name__ == '__main__':
    grammar_obj = grammar(grammar_path)
    grammar_obj.get_augumented_grammar()
    FIRST_obj = FIRST(grammar_obj)
    FOLLOW_obj = FOLLOW(grammar_obj, FIRST_obj)
    itemSets_obj = itemSets()
    itemSets_obj.calculate_itemSets(grammar_obj, FIRST_obj)
    
    analysisTable_obj = analysisTable(grammar_obj, itemSets_obj)
    analysisTable_obj.dump_table_into_file(action_table_path=action_table_path, goto_table_path=goto_table_path)
