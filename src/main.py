import sys
import os
sys.path.append(".")


from src.LR1_parser.LR1 import LR1_parser
from utils.Configs import Configs
from utils.transformer import token2inputStack
from src.lexer.lexical_analyzer import LexicalAnalyzer

if __name__ == '__main__':
    lexer = LexicalAnalyzer(Configs) # 实例化词法分析器
    parser = LR1_parser(Configs) # 实例化LR1语法分析器
    
    test_names = []
    for i in range(2,3):
        test_names.append("testcase-{}.sql".format(i))
    
    
    
    for test_name in test_names:
        print("testing {}.....".format(test_name))
        '''词法分析器根据预设配置，读取待解析文件，进行解析并输出中间结果'''
        lexer.lexical_analyze(test_name, False, True)

        '''语法分析器根据预设配置，读取中间结果，进行解析并输出'''
        token_table_path = os.path.join(Configs.dir_names["output"], "token_table", "token_table_" + test_name.replace(".sql", ".txt"))
        input_stack_path = os.path.join(Configs.dir_names["output"], "input_stack", "input_stack_" + test_name.replace(".sql", ".txt"))
        input_stack = token2inputStack(token_table_path, input_stack_path)
        
        save_path = os.path.join(Configs.dir_names["output"], "parse_result", "parse_result_" + test_name.replace(".sql", ".txt"))
        parse_success_flag = parser.parse(input_stack, True, save_path)
        if parse_success_flag:
            print("test {} parsed successfully\n".format(test_name))
        else:
            print("test {} failed in parsing\n".format(test_name))
            
        lexer.reset()