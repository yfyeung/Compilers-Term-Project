import sys
sys.path.append(".")


from src.LR1 import LR1_parser
from utils.Configs import Configs
from utils.transformer import token2inputStack

if __name__ == '__main__':
    
    LR1_parser_obj = LR1_parser(Configs) # 实例化LR1语法分析器
    
    '''
        此处应当将input_stack替换为待分析的输入,
        类型应为dataStructures.Stack.Stack或以其为基类的子类。
        
        Configs类中定义了语法分析器所必须的一些参数值,
        其静态属性可以在utils/Configs.py中修改与查看。
    '''
    
    input_stack = token2inputStack(Configs.input_file, Configs.input_stack_output_file)
    LR1_parser_obj.parse(input_stack)