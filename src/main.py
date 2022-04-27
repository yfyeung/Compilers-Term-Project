import sys
sys.path.append(".")


from src.LR1_parser.LR1 import LR1_parser
from utils.Configs import Configs
from utils.transformer import token2inputStack
from src.lexer.lexical_analyzer import LexicalAnalyzer

if __name__ == '__main__':
    lexer = LexicalAnalyzer(Configs) # 实例化词法分析器
    parser = LR1_parser(Configs) # 实例化LR1语法分析器
    
    '''词法分析器根据预设配置，读取待解析文件，进行解析并输出中间结果'''
    lexer.lexical_analyze()
    # lexer.print_token_table()
    lexer.save_token_table()
    
    
    '''语法分析器根据预设配置，读取中间结果，进行解析并输出'''
    input_stack = token2inputStack(Configs.input_file, Configs.input_stack_output_file)
    parser.parse(input_stack)