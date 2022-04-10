grammar_path = './docs/grammar.txt'
from dataStructure.FF import FIRST, FOLLOW
from dataStructure.analysisTable import actionTable, analysisTable
from dataStructure.item import item, itemSet, itemSets
from dataStructure.grammar import grammar

if __name__ == '__main__':
    # 读入语法并生成语法四元组
    grammar_obj = grammar(grammar_path)
    grammar_obj.get_augumented_grammar()

    # 生成FIRST集
    FIRST_obj = FIRST(grammar_obj)
    # 生成FOLLOW集
    FOLLOW_obj = FOLLOW(grammar_obj, FIRST_obj)

    # 生成项目集规范族
    itemSets_obj = itemSets()
    itemSets_obj.calculate_itemSets(grammar_obj, FIRST_obj)

    # 生成分析表
    analysisTable_obj = analysisTable(grammar_obj, itemSets_obj)