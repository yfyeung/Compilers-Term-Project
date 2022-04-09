from grammar import grammar
from FF import FIRST, FOLLOW
from item import itemSets
grammar_path = './docs/grammar.txt'

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
            go_from_I = [(i, j) for i, j in itemSets_obj.go.items() if i[0] == index]
            for go in go_from_I:
                if go[0][1] in grammar_obj.terminals:
                    if not self.action_table.__contains__((index, go[0][1])):
                        print('Error: action table does\'t have the key: ', (index, go[0][1]))  
                    elif self.action_table[(index, go[0][1])] is not None:
                        print('Error: action table confliction at: ', (index, go[0][1]))
                    self.action_table[(index, go[0][1])] = "s" + str(go[1])
            for item_ in item_set:
                if item_.dot_pos == len(item_.right):
                    for terminal in item_.terminals:
                        if not self.action_table.__contains__((index, terminal)):
                            print('Error: action table does\'t have the key: ', (index, terminal))
                        elif self.action_table[(index, terminal)] is not None:
                            print('Error: action table confliction at: ', (index, terminal))
                        self.action_table[(index, terminal)] = "r" + str(item_.index)
        

class gotoTable():
    def __init__(self, grammar_obj, itemSets_obj):
        self.goto_table = {}
        self.calculate_goto_table(grammar_obj, itemSets_obj)
    def calculate_goto_table(self, grammar_obj, itemSets_obj):
        state_num = len(itemSets_obj.item_sets)
        for non_terminal in grammar_obj.non_terminals:
            for state in range(state_num):
                self.goto_table[(state, non_terminal)] = None
        for I in itemSets_obj.item_sets:
            index = I.index
            go_from_I = [(i, j) for i, j in itemSets_obj.go.items() if i[0] == index]
            for go in go_from_I:
                if go[0][1] in grammar_obj.non_terminals:
                    if not self.goto_table.__contains__((index, go[0][1])):
                        print('Error: goto table does\'t have the key: ', (index, go[0][1]))
                    elif self.goto_table[(index, go[0][1])] is not None:
                        print('Error: goto table confliction at: ', (index, go[0][1]))
                    self.goto_table[(index, go[0][1])] = "s" + str(go[1])
            
class analysisTable():
    def __init__(self, grammar_obj, itemSets_obj):
        self.action_table = actionTable(grammar_obj, itemSets_obj)
        self.gotoTable = gotoTable(grammar_obj, itemSets_obj)

if __name__ == '__main__':
    grammar_obj = grammar(grammar_path)
    grammar_obj.get_augumented_grammar()
    FIRST_obj = FIRST(grammar_obj)
    FOLLOW_obj = FOLLOW(grammar_obj, FIRST_obj)
    itemSets_obj = itemSets()
    itemSets_obj.calculate_itemSets(grammar_obj, FIRST_obj)
    
    analysisTable(grammar_obj, itemSets_obj)
    a = 1