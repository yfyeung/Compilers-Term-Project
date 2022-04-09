class item():
    def __init__(self, left, right, dot_pos, terminals):
        self.left = left
        self.right = right
        self.dot_pos = dot_pos
        self.terminals = terminals
        
    def go(self, terminal):
        if self.dot_pos > len(self.right) - 1:
            return None
        elif self.right[self.dot_pos] == terminal:
            return item(self.left, self.right, self.dot_pos + 1, self.terminals)
        else:
            return None
        
    def __eq__(self, __o: object) -> bool:
        return self.__dict__ == __o.__dict__
    
class itemSet():
    def __init__(self, item_set_origin, grammar_obj, FIRST_obj, index):
        self.item_set = self.calculate_closure(item_set_origin, grammar_obj.productions, grammar_obj.non_terminals, FIRST_obj)
        self.index = index
        
    def __eq__(self, __o: object) -> bool:
        return self.item_set == __o.item_set
    
    def calculate_closure(self, item_set_origin, productions, non_terminals, FIRST_obj):
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
                                first_set = FIRST_obj.calculate_first_set(symbols)
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
    def calculate_itemSets(self, grammar_obj, FIRST_obj):
        max_index = 0
        productions = grammar_obj.productions
        non_terminals = grammar_obj.non_terminals
        start_item = item(productions[0].left, productions[0].right, 0, ['#'])
        start_item_set = itemSet([start_item], grammar_obj, FIRST_obj, max_index)
        max_index += 1
        self.item_sets.append(start_item_set)
        
        while True:
            before_len = len(self.item_sets)
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
            after_len = len(self.item_sets)
            if after_len == before_len:
                break
        self.convert_go()

    def calculate_go(self, itemSet_obj, grammar_obj):
        terminals = grammar_obj.terminals
        non_terminals = grammar_obj.non_terminals
        symbols = terminals + non_terminals
        add_go = {}
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