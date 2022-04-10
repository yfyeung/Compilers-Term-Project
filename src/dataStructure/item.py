from math import prod
from matplotlib import collections
from grammar import grammar
from FF import FIRST, FOLLOW
import collections
import copy as cp
grammar_path = './docs/grammar.txt'


class item():
    def __init__(self, left, right, dot_pos, terminals, index):
        self.left = left
        self.right = right
        self.dot_pos = dot_pos
        terminals.sort()
        self.terminals = terminals
        self.index = index
        
    def go(self, symbol):
        
        if self.dot_pos > len(self.right) - 1:
            return None
        elif self.right[self.dot_pos] == symbol:
            return item(self.left, self.right, self.dot_pos + 1, self.terminals, self.index)
        else:
            return None
        
    def __eq__(self, __o: object) -> bool:
        return self.__dict__ == __o.__dict__
    
    def __lt__(self, __o: object):
        if not self.left == __o.left:
            return self.left < __o.left
        elif not self.dot_pos < __o.dot_pos:
            return self.dot_pos < __o.dot_pos
        elif not self.right == __o.right:
            return self.right < __o.right
        else:
            return self.terminals < __o.terminals
        
    
class itemSet():
    def __init__(self, item_set_origin, grammar_obj, FIRST_obj, index):
        self.item_set = self.calculate_closure(item_set_origin, grammar_obj.productions, grammar_obj.non_terminals, FIRST_obj)
        self.index = index
        
    def __eq__(self, __o: object) -> bool:
        return self.item_set == __o.item_set
    
    def calculate_closure(self, item_set_origin, productions, non_terminals, FIRST_obj):
        while True:
            before_len = len(item_set_origin)
            for item_obj in item_set_origin:
                if item_obj.dot_pos == len(item_obj.right):
                    continue
                else:
                    dot_right_symbol = item_obj.right[item_obj.dot_pos]
                    if dot_right_symbol in non_terminals:
                        for production in productions:
                            if production.left == dot_right_symbol:
                                symbol = []
                                first_set = []
                                if not item_obj.dot_pos == len(item_obj.right) - 1:
                                    symbol.extend(item_obj.right[item_obj.dot_pos + 1:])
                                for terminal in item_obj.terminals:
                                    symbols = []
                                    symbols.extend(symbol)
                                    symbols.extend([terminal])
                                    first_set.extend(FIRST_obj.calculate_first_set(symbols))
                                first_set = list(set(first_set))
                                if production.right == ['$']:
                                    tmp_item = item(production.left, [], 0, first_set, production.index)
                                else:
                                    tmp_item = item(production.left, production.right, 0, first_set, production.index)
                                if tmp_item not in item_set_origin:
                                    item_set_origin.append(tmp_item)
            after_len = len(item_set_origin)
            if after_len == before_len:
                break        
        # item_set_origin.sort()
        return item_set_origin
    def __lt__(self, __o):
        if not self.item_set[0] == __o.item_set[0]:
            return self.item_set[0] < __o.item_set[0]
        else:
            return len(self.item_set) < len(__o.item_set)
        
class itemSets():
    def __init__(self):
        self.item_sets = []
        self.go = {}
    def calculate_itemSets(self, grammar_obj, FIRST_obj):
        max_index = 0
        productions = grammar_obj.productions
        non_terminals = grammar_obj.non_terminals
        start_item = item(productions[0].left, productions[0].right, 0, ['#'], productions[0].index)
        start_item_set = itemSet([start_item], grammar_obj, FIRST_obj, max_index)
        max_index += 1
        self.item_sets.append(start_item_set)
        
        while True:
            before_len = len(self.go)
            for add_item_set in self.item_sets:
                add_go = self.calculate_go(add_item_set, grammar_obj)
                for key, value in add_go.items():
                    value_closure = itemSet(value, grammar_obj, FIRST_obj, -1)
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
            after_len = len(self.go)
            if after_len == before_len:
                break
        self.convert_go()
        self.merge_item_sets()
    def calculate_go(self, itemSet_obj, grammar_obj):
        terminals = grammar_obj.terminals
        non_terminals = grammar_obj.non_terminals
        symbols = terminals + non_terminals
        add_go = collections.OrderedDict()
        for symbol in symbols:
            for item_ in itemSet_obj.item_set:
                if item_.go(symbol) is not None:
                    if not add_go.__contains__((itemSet_obj.index, symbol)):
                        add_go[(itemSet_obj.index, symbol)] = [item_.go(symbol)]
                    else:
                        add_go[(itemSet_obj.index, symbol)].append(item_.go(symbol))
        return add_go
        
    def convert_go(self):
        new_go = {}
        for key, value in self.go.items():
            new_go[key] = value.index
        self.go = new_go

    def merge_item_sets(self):
        for index, item_set in enumerate(self.item_sets):
            new_item_set = []
            store_dict = {}
            query_dict = {}
            for item_ in item_set.item_set:
                tmp_tri = [item_.left, item_.right, item_.dot_pos, item_.index]
                query_dict[str(tmp_tri)] = tmp_tri
                store_dict[str(tmp_tri)] = []
            for item_ in item_set.item_set:
                tmp_tri = [item_.left, item_.right, item_.dot_pos, item_.index]
                store_dict[str(tmp_tri)].extend(item_.terminals)
            for key, value in store_dict.items(): 
                value = list(set(value))
                value.sort()
                tri = query_dict[key]
                tmp_item = item(tri[0], tri[1], tri[2], value, tri[3])
                new_item_set.append(tmp_item)
            
            self.item_sets[index].item_set = new_item_set
        
        pass
            

if __name__ == '__main__':
    grammar_obj = grammar(grammar_path)
    grammar_obj.get_augumented_grammar()
    # print(grammar_obj.non_terminals)
    # print(len(grammar_obj.non_terminals))
    # print(grammar_obj.terminals)
    # print(len(grammar_obj.terminals))
    # for production in grammar_obj.productions:
    #     print(production.left, production.right, production.index)
    # print(grammar_obj.start)
    FIRST_obj = FIRST(grammar_obj)
    # FIRST_obj.calculate_first(grammar_obj.non_terminals, grammar_obj.terminals, grammar_obj.productions)
    # for firstset in FIRST_obj.first_sets.items():
    #     print(firstset)
    # print(len(FIRST_obj.first_sets))
    FOLLOW_obj = FOLLOW(grammar_obj, FIRST_obj)
    # FOLLOW_obj.calculate_follow(grammar_obj.non_terminals, grammar_obj.terminals, grammar_obj.productions, grammar_obj.start, FIRST_obj.first_sets)
    # for followset in FOLLOW_obj.follow_sets.items():
    #     print(followset)
    # print(len(FOLLOW_obj.follow_sets))
    itemSets_obj = itemSets()
    itemSets_obj.calculate_itemSets(grammar_obj, FIRST_obj)
    for item_set_obj in itemSets_obj.item_sets:
        if item_set_obj.index in [11,12,13]:
            for item in item_set_obj.item_set:
                print(item.left, item.right, item.dot_pos, item.terminals, item.index)
            print(item_set_obj.index)
    # for go in itemSets_obj.go.items():
    #     print(go)
