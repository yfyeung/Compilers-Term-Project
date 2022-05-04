## Introduction

- 这是天津大学《编译原理与技术》课程的大作业，内容为实现一个简易的SQL编译器，包括词法分析器和LR1语法分析器
- 支持的语言为SQL--，具体词法和语法详见 [实验文档(https://docs.qq.com/doc/DQ3ZsZ0lQTWpMbUNU)](./doc)
- 源代码的介绍详见 [这里](./src/README.md)



## Environment

Python 3

matplotlib==3.4.3



## Quick Start

1. 将测试用例命令为 `testcase-{X}.sql` ，如 `testcase-3.sql` ，并放在 `tests` 里
2. 在项目根目录执行 `python main.py`
3. 编译结果位于 `output` 



## Code Structure

```
.
├── docs                          # 文档
├── main.py                       # 主程序
├── output                        # 输出文件夹
│   ├── ds_details                # 
│   ├── ds_entity                 # 
│   ├── input_stack               # 
│   ├── parse_result              # 
│   └── token_table               # 
├── src                           # 源代码
│   ├── lexer                     # 词法分析器
│   │   ├── ds                    # 词法分析器数据结构
│   │   │   ├── graph.py
│   │   │   └── token.py
│   │   ├── lexical_analyzer.py   # 词法分析器主程序
│   │   ├── rex2nfa.py            # 转NFA
│   │   ├── nfa2dfa.py            # NFA确定化
│   │   └── dfa2min.py            # DFA最小化
│   └── LR1_parser                # LR1语法分析器
│       ├── ds                    # 语法分析器数据结构
│       │   ├── analysisTable.py
│       │   ├── FF.py
│       │   ├── grammar.py
│       │   ├── item.py
│       │   └── stack.py
│       └── LR1.py                # 词法分析器主程序
├── tests                         # 测试用例 
└── utils                         # 工具包
    ├── configs.py                # 配置
    ├── regex.json                # 词法
    ├── grammar.txt               # 语法
    └── transformer.py            # 转换器
```



## Sponsor

如果本项目对您有帮助的话，请给我们star一下哒~

