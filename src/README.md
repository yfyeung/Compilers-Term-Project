### 数据结构
`data_structure.py`文件中定义LR(1)分析过程中所用到的几个重要数据结构。

+ **production** 产生式
  + 成员变量
    +  `left`: 产生式左端
    + `right`: 产生式右端(list)
    + `index`: 产生式序号
+ **grammar** 文法
  + 成员变量 
    + `non_terminals`: 非终结符列表
    + `terminals`: 终结符列表
    + `productions`: 产生式列表
    + `start`: 开始符号
    + `grammar_content`: 文法文本
  + 成员函数 
    + `map`: 产生式推导函数
+ **item** 项目
  + 成员变量 
    + `left`: 产生式左端
    + `right`: 产生式右端(list)
    + `dot_pos`: dot位置
    + `terminals`: 终结符列表，项目的第二个分量
  + 成员函数 
    + 
+ **itemSet** 项目集
  + 成员变量 
    + `items`: 项目列表
  + 成员函数

+ **FIRST** FIRST集合
  + 成员变量 
    + `first_dict`: first字典
  + 成员函数 
    + `get_first`: 计算first集合

+ **FOLLOW** FOLLOW集合
  + 成员变量 
    + `follow_dict`: follow字典
  + 成员函数 
    + `get_follow`: 计算first集合
+ **actionTable** 分析表
  + 成员变量 
    + 
  + 成员函数 
    + 
+ **gotoTable** goto函数表
  + 成员变量
    + 
  + 成员函数
    + 
+ **analysisTable** 分析表
  + 成员变量
    + `actionTable`: 动作表
    + `gotoTable`: goto函数表
  + 成员函数
    + 



### LR1语法分析器
`LR1_parser.py`中编写LR1语法分析器.