## 源代码结构

```
.
├── lexer                    # 词法分析器
│   ├── ds                   # 词法分析器数据结构
│   │   ├── graph.py
│   │   └── token.py
│   ├── lexical_analyzer.py  # 词法分析器主程序
│   ├── rex2nfa.py           # 转NFA
│   ├── nfa2dfa.py           # NFA确定化
│   └── dfa2min.py           # DFA最小化
└── LR1_parser               # LR1语法分析器
    ├── ds                   # 语法分析器数据结构
    │   ├── analysisTable.py
    │   ├── FF.py
    │   ├── grammar.py
    │   ├── item.py
    │   └── stack.py
    └── LR1.py               # 词法分析器主程序
```



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

