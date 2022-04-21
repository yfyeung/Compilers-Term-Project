**Note that**：
语法分析器LR1定义在`./src/LR1.py`中。
语法分析器LR1所用到的所有数据结构定义在`./src/dataStructure`中。



## QuickStart
1. 将待语法分析的token流放在tests文件夹内；
2. 修改utils.Configs文件中的input_file_name为刚待分析的文件名；
3. 根据需要修改utils.Configs中的redirect stdout属性，若将此设为True，则会将归约序列重定向至output/parse.result文件夹中。
4. 输出文件全部位于output文件夹中。
