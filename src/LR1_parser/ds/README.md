`data_structure`中定义LR(1)分析过程中所用到的几个重要数据结构，依据类别归类为以下几个文件:

### grammar.py

该文件中定义了**production(产生式)，grammar(文法)**两个数据结构。

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
    + `load_grammar`: 从文件中加载语法文本，并将其转换为四元组存储在成员变量中。
    + `get_augumented_grammar`：生成增广文法。

### item.py

该文件中定义了**item（项目），itemSet（项目集），itemSets（项目集规范族）**三个数据结构。

+ **item** 项目
  + 成员变量 
    + `left`: 产生式左端
    + `right`: 产生式右端(list)
    + `dot_pos`: dot位置
    + `terminals`: 终结符列表，项目的第二个分量
  + 成员函数 
    + `go`：计算`move(item, terminal)`。
  + 重载eq：当item各成员变量相等时，item相等。



+ **itemSet** 项目集
  + 成员变量 
    + `item_set`: 项目的集合
    + `index`：项目集在项目集规范族中的序号
  + 成员函数
    + `calculate_closure`: 计算项目集闭包
  + 重载eq：当项目集合中各个项目相等时，项目集相等（忽略index）。



+ **itemSet** 项目集规范族

  + ​	成员变量 
    + `item_sets`: 项目集的集合
    + `go`：项目集规范族的go关系

  + 成员函数
    + `calculate_itemSets`: 由文法计算该文法的项目集规范族以及go关系
    + `calculate_go`: 计算某个项目集可以go到的项目集
    + `convert_go`: 对self.go进行格式转换，转换后的格式为：key: (from_index, terminal), value: go_index



### FF.py

该文件中定义了**FIRST和FOLLOW**两个数据结构。

+ **FIRST** FIRST集合
  + 成员变量 
    + `first_sets`: first集合集
    + `grammar_obj`：待计算first的文法
  + 成员函数 
    + `calculate_first`: 计算first集合集
    + `calculate_first_set`: 由符号串计算其对应的first集
    + `dump_first_sets_into_file`：存储



+ **FOLLOW** FOLLOW集合
  + 成员变量 
    + `follow_sets`: follow集合集
  + 成员函数 
    + `**calculate_follow**`: 计算follow集合集
    + `dump_follow_sets_into_file`:存储

### analysisTable.py

该文件存储以下几个数据结构：

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