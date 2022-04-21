from imp import init_frozen
import sys
import copy

from src.dataStructure.FF import FIRST, FOLLOW
from src.dataStructure.analysisTable import analysisTable
from src.dataStructure.item import itemSets
from src.dataStructure.grammar import grammar
from src.dataStructure.Stack import Stack

class LR1_parser:
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
        grammar_obj = grammar(grammar_path)
        grammar_obj.get_augumented_grammar()
        self.grammar_obj = grammar_obj

        # 生成FIRST集
        FIRST_obj = FIRST(grammar_obj)
        self.FIRST_obj = FIRST_obj
        
        # 生成FOLLOW集
        FOLLOW_obj = FOLLOW(grammar_obj, FIRST_obj)
        self.FOLLOW_obj = FOLLOW_obj

        # 生成项目集规范族
        itemSets_obj = itemSets()
        itemSets_obj.calculate_itemSets(grammar_obj, FIRST_obj)
        self.itemSets_obj = itemSets_obj
        
        # 生成分析表
        analysisTable_obj = analysisTable(grammar_obj, itemSets_obj)
        self.analysisTable_obj = analysisTable_obj
        
        # 将各集合与表格输出为文件
        if self.Configs.DUMP_DS_TO_FILE:
            FIRST_obj.dump_first_sets_into_file(self.Configs.first_sets_output_path)
            FOLLOW_obj.dump_follow_sets_into_file(self.Configs.follow_sets_output_path)
            analysisTable_obj.dump_table_into_file(action_table_path=self.Configs.action_table_path, goto_table_path=self.Configs.goto_table_path)
    
    def parse(self, input_stack):
        
        if self.Configs.REDIRECT_STDOUT_TO_FILE:
            old_std_out = sys.stdout
            sys.stdout = open(self.Configs.parse_result_path, 'w')
        
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
                    print('{}\t{}\t{}#{}\t{}'.format(step,'/',symbol_stack.peek(),input_stack.peek(),'accept'))
                    break
                elif action is None:
                    print('{}\t{}\t{}#{}\t{}'.format(step,'/',symbol_stack.peek(),input_stack.peek(),'error'))
                    exit(-1)
                else:
                    if action[0] == 's':
                        state_stack.push(int(action[1:]))
                        symbol_stack.push(input_stack.pop())
                        print('{}\t{}\t{}#{}\t{}'.format(step,'/',symbol_stack.peek(),input_stack.peek(),'move'))
                        step += 1
                    elif action[0] == 'r':
                        production = self.grammar_obj.productions[int(action[1:])]
                        if production.index != int(action[1:]):
                            print("Error: production index not match. Abort!")
                            exit(-1)
                        if production.right == ['$']:
                            right_symbol_num = 0
                        else:
                            right_symbol_num = len(production.right)
                        right_symbols = copy.deepcopy(production.right)
                        right_symbols.reverse()
                        for i in range(right_symbol_num):
                            if (right_symbols[i] != symbol_stack.peek()):
                                print("Error: symbol not match. Abort!")
                                exit(-1)
                            state_stack.pop()
                            symbol_stack.pop()
                        symbol_stack.push(production.left)
                        state_front = state_stack.peek()
                        symbol_front = symbol_stack.peek()
                        state_stack.push(int(self.analysisTable_obj.gotoTable.goto_table[(state_front, symbol_front)][1:]))
                        
                        print('{}\t{}\t{}#{}\t{}'.format(step,action[1],symbol_stack.peek(),input_stack.peek(),'reduction'))
                        step += 1
                    else:
                        print("Error: action is neither acc nor None or 's' or 'r'. Abort!")
                        exit(-1)
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
                    print("Error: goto is neither None or 's'. Abort!")
                    exit(-1)
            else:
                print("Error: input is neither terminal nor non-terminal in grammar. Abort!")
                exit(-1)
                
