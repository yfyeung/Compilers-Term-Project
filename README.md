## Code Structure

```
.
├── README.md // help
├── bin				// 启动入口：.sh脚本
├── docs			// 文档
├── log				// 日志
├── output		// 输出：符号表、常量表、词素序列、token序列等
├── src				// 主程序
├── tests			// 测试用例
└── utils			// 全局变量、全局方法
```

**Note that**：
语法分析器LR1定义在`./src/LR1.py`中。
语法分析器LR1所用到的所有数据结构定义在`./src/dataStructure`中。



## QuickStart

直接运行`./src/main.py`即可。

> 运行前请根据需要修改`utils.Configs.py`中的一些设置，并且设置好main.py中的input_stack。

