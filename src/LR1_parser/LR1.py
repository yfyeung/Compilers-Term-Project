import sys
import copy
import os
import pickle

from .ds.FF import FIRST, FOLLOW
from .ds.analysisTable import analysisTable
from .ds.item import itemSets
from .ds.grammar import grammar
from .ds.Stack import Stack

class LR1_parser:
    '''语法分析器'''
    def __init__(self, Configs):
        self.grammar_obj = None
        self.FIRST_obj = None
        self.FOLLOW_obj = None
        self.itemSets_obj = None
        self.analysisTable_obj = None
        self.Configs = Configs
        self.LR1_init(self.Configs.grammar_path)
        
    def LR1_init(self, grammar_path):
        # 读入语法并生成语法四元组
        if not os.path.exists(self.Configs.grammar_path_e):
            grammar_obj = grammar(grammar_path)
            grammar_obj.get_augumented_grammar()
            self.grammar_obj = grammar_obj
            pickle.dump(self.grammar_obj, open(self.Configs.grammar_path_e, 'wb'))
        else:
            self.grammar_obj = pickle.load(open(self.Configs.grammar_path_e, 'rb'))
            
        # 生成FIRST集
        if not os.path.exists(self.Configs.first_sets_output_path_e):
            FIRST_obj = FIRST(self.grammar_obj)
            self.FIRST_obj = FIRST_obj
            pickle.dump(self.FIRST_obj, open(self.Configs.first_sets_output_path_e, 'wb'))
        else:
            self.FIRST_obj = pickle.load(open(self.Configs.first_sets_output_path_e, 'rb'))
        
        # 生成FOLLOW集
        if not os.path.exists(self.Configs.follow_sets_output_path_e):
            FOLLOW_obj = FOLLOW(self.grammar_obj, self.FIRST_obj)
            self.FOLLOW_obj = FOLLOW_obj
            pickle.dump(self.FOLLOW_obj, open(self.Configs.follow_sets_output_path_e, 'wb'))
        else:
            self.FOLLOW_obj = pickle.load(open(self.Configs.follow_sets_output_path_e, 'rb'))
        
        # 生成项目集规范族
        if not os.path.exists(self.Configs.item_sets_path_e):
            itemSets_obj = itemSets()
            itemSets_obj.calculate_itemSets(self.grammar_obj, self.FIRST_obj)
            self.itemSets_obj = itemSets_obj
            pickle.dump(self.itemSets_obj, open(self.Configs.item_sets_path_e, 'wb'))
        else:
            self.itemSets_obj = pickle.load(open(self.Configs.item_sets_path_e, 'rb'))

        # 生成分析表
        if not os.path.exists(self.Configs.analysis_table_path_e):
            analysisTable_obj = analysisTable(self.grammar_obj, self.itemSets_obj)
            self.analysisTable_obj = analysisTable_obj
        else:
            self.analysisTable_obj = pickle.load(open(self.Configs.analysis_table_path_e, 'rb'))
            
        # 将各集合与表格输出为文件
        if self.Configs.DUMP_DS_TO_FILE:
            self.FIRST_obj.dump_first_sets_into_file(self.Configs.first_sets_output_path)
            self.FOLLOW_obj.dump_follow_sets_into_file(self.Configs.follow_sets_output_path)
            self.analysisTable_obj.dump_table_into_file(action_table_path=self.Configs.action_table_path, goto_table_path=self.Configs.goto_table_path)
            self.itemSets_obj.dump_into_file()
            
    def parse(self, input_stack, REDIRECT_STDOUT_TO_FILE, save_path):
        
        if REDIRECT_STDOUT_TO_FILE:
            old_std_out = sys.stdout
            sys.stdout = open(save_path, 'w')
        
        state_stack = Stack()
        symbol_stack = Stack()

        state_stack.push(0)
        symbol_stack.push('#')

        step = 1
        
        while(len(input_stack.items) > 0):
            input_front = input_stack.peek()
            state_front = state_stack.peek()

            
            if input_front in self.grammar_obj.terminals or input_front == "#":
                action = self.analysisTable_obj.action_table.action_table[(state_front, input_front)]
                if action == 'acc':
                    print('{}\t{}\t{}#{}\t{}'.format(step,'/',symbol_stack.peek(),input_stack.peek(),'accept'), end='')
                    break
                elif action is None:
                    print('{}\t{}\t{}#{}\t{}'.format(step,'/',symbol_stack.peek(),input_stack.peek(),'error'))
                    break
                else:
                    if action[0] == 's':
                        print('{}\t{}\t{}#{}\t{}'.format(step,'/',symbol_stack.peek(),input_stack.peek(),'move'))
                        step += 1
                        state_stack.push(int(action[1:]))
                        symbol_stack.push(input_stack.pop())
                        # print('{}\t{}\t{}#{}\t{}'.format(step,'/',symbol_stack.peek(),input_stack.peek(),'move'))
                        # step += 1
                    elif action[0] == 'r':
                        print('{}\t{}\t{}#{}\t{}'.format(step,action[1:],symbol_stack.peek(),input_stack.peek(),'reduction'))
                        step += 1
                        production = self.grammar_obj.productions[int(action[1:])]
                        if production.index != int(action[1:]):
                            assert False, "Error: production index not match. Abort!"
                        if production.right == ['$']:
                            right_symbol_num = 0
                        else:
                            right_symbol_num = len(production.right)
                        right_symbols = copy.deepcopy(production.right)
                        right_symbols.reverse()
                        for i in range(right_symbol_num):
                            if (right_symbols[i] != symbol_stack.peek()):
                                assert False, "Error: symbol not match. Abort!"
                            state_stack.pop()
                            symbol_stack.pop()
                        symbol_stack.push(production.left)
                        state_front = state_stack.peek()
                        symbol_front = symbol_stack.peek()
                        state_stack.push(int(self.analysisTable_obj.gotoTable.goto_table[(state_front, symbol_front)][1:]))
                        
                        
                    else:
                        assert False, "Error: action is neither acc nor None or 's' or 'r'. Abort!"
            elif input_front in self.grammar_obj.non_terminals:
                goto = self.analysisTable_obj.gotoTable.goto_table[(state_front, input_front)]
                if goto == None:
                    print('{}\t{}\t{}#{}\t{}'.format(step,'/',symbol_stack.peek(),input_stack.peek(),'error'))
                    break
                elif goto[0] == 's':
                    state_stack.push(goto[1])
                    symbol_stack.push(input_stack.pop())
                    print('{}\t{}\t{}#{}\t{}'.format(step,'/',symbol_stack.peek(),input_stack.peek(),'move'))
                    step += 1
                else:
                    assert False, "Error: goto is neither None or 's'. Abort!"
            else:
                assert False, "Error: input is neither terminal nor non-terminal in grammar. Abort!"
        if REDIRECT_STDOUT_TO_FILE:
            sys.stdout = old_std_out
        if action == 'acc':
            return True
        elif action is None:
            return False
        else:
            assert False, "At the end of parsing, action is neither acc nor None. Abort!"
