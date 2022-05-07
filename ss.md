from .grammar import grammar
from .FF import FIRST, FOLLOW
from .item import itemSets
from utils.configs import Configs

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

## 词法分析器





## LR1语法分析器

### LR1.py

该文件定义了**LR1语法分析器**

+ 成员变量
  + `grammar_obj`: 文法对象
  + `FIRST_obj`: FIRST集
  + `FOLLOW_obj`: FOLLOW集
  + `itemSets_obj`: 项目集规范族
  + `analysisTable_obj`: 动作表
  + `Configs`: 语法分析器的基本设置
+ 成员函数
  + `LR1_init`: 初始化LR1语法分析器，即根据语法计算出所有需要的对象，并且以pkl的形式保存，方便下一次直接调用。
  + `parse`: 进行语法分析，输出归约序列到stdout或者文本文件中。



### analysisTable.py

+ **actionTable** 动作表
  + 成员变量 
    + `action_table`: 动作表
  + 成员函数 
    + `calculate_actionTable`: 根据项目及规范族和go关系计算动作表。
    + `dump_actionTable_into_file`: 将动作表写入文本文件。

+ **gotoTable** goto函数表
  + 成员变量
    + `goto_table`: goto函数表
  + 成员函数
    + `calculate_gotoTable`: 根据项目及规范族和go关系计算goto函数表。
    + `dump_gotoTable_into_file`: 将goto函数表写入文本文件。

+ **analysisTable** 分析表
  + 成员变量
    + `actionTable`: 动作表
    + `gotoTable`: goto函数表
  + 成员函数
    + `dump_analysisTable_into_file`: 将分析表写入文本文件。



### FF.py

该文件中定义了**FIRST和FOLLOW**两个数据结构。

+ **FIRST** FIRST集合
  + 成员变量 
    + `first_sets`: first集合的集合
    + `grammar_obj`：待计算first的文法
  + 成员函数 
    + `calculate_first`: 计算grammar_obj的first集合
    + `calculate_first_set`: 计算确切的某一个符号串的first集合
    + `dump_first_sets_into_file`：将first写入文本文件



+ **FOLLOW** FOLLOW集合
  + 成员变量 
    + `follow_sets`: follow集合的集合
  + 成员函数 
    + `calculate_follow`: 计算grammar_obj的follow集合
    + `dump_follow_sets_into_file`: 将follow写入文本文件



### grammar.py

该文件中定义了**production(产生式)，grammar(文法)**两个数据结构。

+ **production** 产生式
  + 成员变量
    +  `left`: 产生式左端
    + `right`: 产生式右端(list)
    + `index`: 产生式序号

+ **grammar** 文法
  + 成员变量 
    + `non_terminals`: 文法的非终结符列表
    + `terminals`: 文法的终结符列表
    + `productions`: 文法的产生式列表
    + `start`: 文法的开始符号
    + `grammar_content`: 文法的文本
  + 成员函数 
    + `load_grammar`: 从文件中加载语法文本，并将其转换为四元组存储在成员变量中。
    + `get_augumented_grammar`：生成增广文法。



### item.py

该文件中定义了**item（项目），itemSet（项目集），itemSets（项目集规范族）**三个数据结构。

+ **item** 项目
  + 成员变量 
    + `left`: 产生式左端
    + `right`: 产生式右端(list)
    + `dot_pos`: dot的位置
    + `terminals`: 项目对应的终结符列表，即项目的第二个分量
    + `index`: 项目的序号
  + 成员函数 
    + `go`：计算`move(item, terminal)`，即根据输入的终结符得到下一个项目。
    + `__eq__`: 定义“项目相等”的比较方法。（主要使得“in”的查询可行）
    + `__lt__`: 定义项目排序方法。（没有用到）



+ **itemSet** 项目集
  + 成员变量 
    + `item_set`: 经过有限状态机转换后的同一个状态对应的项目集。
    + `index`：项目集在项目集规范族中的序号（go的依据）。
  + 成员函数
    + `calculate_closure`: 计算项目集闭包。
    + `__lt__`: 定义项目集排序方法。（应该是没有用到）




+ **itemSets** 项目集规范族

  + ​	成员变量 
    + `item_sets`: 项目集的集合，即项目集规范族。
    + `go`：项目集规范族中的go关系，即有限状态机里的转移关系。

  + 成员函数
    + `calculate_itemSets`: 由文法计算该文法的项目集规范族以及go关系。
    + `calculate_go`: 计算某个项目集所有可以go到的项目集。
    + `convert_go`: 对self.go进行格式转换，转换后的格式为字典，其中：key为 (from_index, terminal), value为go_index，即go的转换结果。方便查询。



### stack.py

该文件中定义了一个**简易栈**


    
    
    
    
    
    
    


\begin{center}
\textbf{ADT1:} production 抽象数据类型
\end{center}
\begin{verbatim}
    ADT production {
        数据对象：D = {
            左部符号 left,   
            右部符号 right,
            产生式编号 index
        }
        数据关系：R = {}
        基本操作：
            init(left, right, index)
                初始条件：left存在
                操作结果：初始化production
    } ADT production
\end{verbatim}
\label{ADT TokenLine}


\begin{center}
\textbf{ADT1:} grammar 抽象数据类型
\end{center}
\begin{verbatim}
    ADT grammar {
        数据对象：D = {
            非终结符集 non_terminal,
            终结符集 terminal,
            产生式集 productions,
            初始符号 start
            grammar文本内容 grammar_context
        }
        数据关系：R = {}
        基本操作：
            init(grammar_file_path)
                初始条件：路径存在
                操作结果：初始化grammar各变量
            load_grammar(grammar_file_path)
                初始条件：路径存在
                操作结果：根据grammar文本文件，计算得到non_terminal, terminal, productions, start等成员对象
            get_augumented_grammar()
                初始条件：grammar加载完成
                操作结果：将grammar转换为其对应的增广文法
    } ADT grammar
\end{verbatim}
\label{ADT TokenLine}


\begin{center}
\textbf{ADT1:} FIRST 抽象数据类型
\end{center}
\begin{verbatim}
    ADT FIRST {
        数据对象：D = {
            FIRST集合 first_sets,
            文法对象 grammar_obj
        }
        数据关系：R = {}
        基本操作：
            init(grammar_obj)
                初始条件：grammar_obj存在
                操作结果：初始化FIRST
            calculate_first_sets()
                初始条件：FIRST已初始化
                操作结果：根据文法计算该文法中各个符号的FIRST集合，并存入first_sets中
            calculate_follow_set(symbols)
                初始条件：FIRST已初始化、first_sets已计算完成、symbols合法
                操作结果：返回符号串symbols的FIRST集合 
            dump_first_sets_into_file(file_path)
                初始条件：FIRST已初始化、first_sets已计算完成、file_path合法
                操作结果：将FIRST按照规定格式写入文件file_path中
    } ADT FIRST
\end{verbatim}
\label{ADT TokenLine}


\begin{center}
\textbf{ADT1:} FOLLOW 抽象数据类型
\end{center}
\begin{verbatim}
    ADT FOLLOW {
        数据对象：D = {
            FOLLOW集合 follow_sets
        }
        数据关系：R = {}
        基本操作：
            init(grammar_obj, FIRST_obj)
                初始条件：grammar_obj存在，FIRST_obj存在，并且FIRST_obj与grammar_obj相对应
                操作结果：初始化FOLLOW
            calculate_follow()
                初始条件：FOLLOW已初始化
                操作结果：根据文法grammar_obj与其对应的FIRST_obj计算该文法中各个符号（终结符）的FOLLOW集合，并存入follow_sets中
            dump_follow_sets_into_file(file_path)
                初始条件：FOLLOW已初始化、follow_sets已计算完成、file_path合法
                操作结果：将FOLLOW按照规定格式写入文件file_path中
    } ADT FOLLOW
\end{verbatim}
\label{ADT TokenLine}


\begin{center}
\textbf{ADT1:} item 抽象数据类型
\end{center}
\begin{verbatim}
    ADT item {
        数据对象：D = {
            项目产生式左端符号 left,
            项目产生式右端符号 right,
            项目dot位置 dot_pos,
            项目对应的终结符号集合 terminals,
            项目对应的产生式的编号 index
        }
        数据关系：R = {}
        基本操作：
            init(left, right, dot_pos, terminals, index)
                初始条件：left, right, dot_pos, terminals, index合法
                操作结果：初始化item
            go(symbol)
                初始条件：item已初始化、symbol合法
                操作结果：计算move(item, symbol)，即根据输入的终结符得到下一个项目。

    } ADT item
\end{verbatim}
\label{ADT TokenLine}


\begin{center}
\textbf{ADT1:} itemSet 抽象数据类型
\end{center}
\begin{verbatim}
    ADT itemSet {
        数据对象：D = {
            项目集合 item_set,
            项目集合的编号 index
        }
        数据关系：R = {}
        基本操作：
            init(item_set, index)
                初始条件：item_set合法、index合法
                操作结果：初始化itemSet
            calculate_closure(grammar_obj, FIRST_obj)
                初始条件：itemSet已初始化、grammar_obj存在、FIRST_obj存在，并且FIRST_obj与grammar_obj相对应
                操作结果：计算项目集合的闭包，项目增加入item_set中


    } ADT itemSet
\end{verbatim}
\label{ADT TokenLine}


\begin{center}
\textbf{ADT1:} itemSets 抽象数据类型
\end{center}
\begin{verbatim}
    ADT itemSets {
        数据对象：D = {
            项目集规范族 item_sets
            go关系 go
        }
        数据关系：R = {}
        基本操作：
            init()
                初始条件：无
                操作结果：初始化itemSets
            calculate_itemSets(grammar_obj, FIRST_obj)
                初始条件：itemSets已初始化、grammar_obj存在、FIRST_obj存在，并且FIRST_obj与grammar_obj相对应
                操作结果：根据语法计算其对应的项目集规范族，并存入item_sets中
            calculate_go(itemSet_obj, grammar_obj)
                初始条件：itemSet_obj合法、grammar_obj存在
                操作结果：计算itemSet_obj在grammar_obj的文法下可以跳转到的项目集，并将相应的关系存入go中
            convert_go()
                初始条件：itemSets已初始化
                操作结果：将成员变量go从原来的列表类型转换为字典类型
            merge_item_sets()
                初始条件：itemSets各成员变量已经计算完成
                操作结果：将成员变量item_sets中各个项目集进行merge操作，将项目集内具有相同产生式和dot位置的项目对应的终结符号集合合并起来，作为一个项目
            dump_into_file():
                初始条件：itemSets已计算完毕
                操作结果：将itemSets中的数据按照规定格式写入文件
    } ADT itemSets
\end{verbatim}
\label{ADT TokenLine}


\begin{center}
\textbf{ADT1:} actionTable 抽象数据类型
\end{center}
\begin{verbatim}
    ADT actionTable {
        数据对象：D = {
            动作表 action_table
        }
        数据关系：R = {}
        基本操作：
            init()
                初始条件：无
                操作结果：初始化actionTable
            calculate_action_Table(grammar_obj, itemSets_obj)
                初始条件：actionTable已初始化、grammar_obj存在、itemSets_obj存在，并且itemSets_obj与grammar_obj相对应
                操作结果：根据语法规则和项目集规范族计算其对应的动作表，并存入action_table中
            dump_table_into_file(file_path)
                初始条件：action_table已计算完毕、file_path合法
                操作结果：将action_table中的数据按照规定格式写入文件
    } ADT actionTable
\end{verbatim}
\label{ADT TokenLine}

\begin{center}
\textbf{ADT1:} gotoTable 抽象数据类型
\end{center}
\begin{verbatim}
    ADT gotoTable {
        数据对象：D = {
            跳转表 goto_table
        }
        数据关系：R = {}
        基本操作：
            init()
                初始条件：无
                操作结果：初始化gotoTable
            calculate_goto_Table(grammar_obj, itemSets_obj)
                初始条件：gotoTable已初始化、grammar_obj存在、itemSets_obj存在，并且itemSets_obj与grammar_obj相对应
                操作结果：根据语法规则和项目集规范族计算其对应的跳转表，并存入goto_table中
            dump_table_into_file(file_path)
                初始条件：goto_table已计算完毕、file_path合法
    } ADT gotoTable
\end{verbatim}
\label{ADT TokenLine}

\begin{center}
\textbf{ADT1:} LR1_parser 抽象数据类型
\end{center}
\begin{verbatim}
    ADT LR1_parser {
        数据对象：D = {
            语法分析器对应文法 grammar_obj,
            语法分析器对应FIRST集 FIRST_obj,    
            语法分析器对应FOLLOW集 FOLLOW_obj,
            语法分析器对应项目集规范族 itemSets_obj,
            语法分析器对应分析表 analysisTable_obj,
            语法分析器基本配置项 Configs
        }
        数据关系：R = {}
        基本操作：
            init(Configs)
                初始条件：Configs合法
                操作结果：根据Configs初始化LR1_parser   
            LR1_init(grammar_path)
                初始条件：grammar_path合法
                操作结果：根据grammar_path计算LR1_parser所有成员变量
            parse(input_stack, REDIRECT_STDOUT_TO_FILE, save_path)
                初始条件：input_stack合法、REDIRECT_STDOUT_TO_FILE合法、save_path合法
                操作结果：对input_stack进行语法分析。若REDIRECT_STDOUT_TO_FILE为真，则将语法分析过程输出到文件save_path中；若为假，则将语法分析过程输出到标准输出中。
    } ADT LR1_parser
\end{verbatim}
\label{ADT TokenLine}

语法分析前需要首先对文法进行预处理，将以文本文件形式存储的语法转换为${\rm [V_N, V_T, P, S]}$的形式，其中$V_N$为非终结符集，$V_T$为终结符集，$P$为产生式集，$S$为开始符号。