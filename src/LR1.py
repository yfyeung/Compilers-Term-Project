grammar_path = './docs/grammar.txt'
from dataStructure.FF import FIRST, FOLLOW
from dataStructure.item import item, itemSet, itemSets
from dataStructure.grammar import grammar

if __name__ == '__main__':
    grammar_obj = grammar(grammar_path)
    grammar_obj.get_augumented_grammar()
    # print(G.non_terminals)
    # print(len(G.non_terminals))
    # print(G.terminals)
    # print(len(G.terminals))
    # for production in G.productions:
    #     print(production.left, production.right, production.index)
    # print(G.start)
    FIRST_obj = FIRST(grammar_obj)
    # FIRST_obj.calculate_first(G.non_terminals, G.terminals, G.productions)
    # for firstset in FIRST_obj.first_sets.items():
    #     print(firstset)
    # print(len(FIRST_obj.first_sets))
    FOLLOW_obj = FOLLOW(grammar_obj, FIRST_obj)
    # FOLLOW_obj.calculate_follow(G.non_terminals, G.terminals, G.productions, G.start, FIRST_obj.first_sets)
    # for followset in FOLLOW_obj.follow_sets.items():
    #     print(followset)
    # print(len(FOLLOW_obj.follow_sets))
    itemSets_obj = itemSets()
    itemSets_obj.calculate_itemSets(grammar_obj, FIRST_obj)
    # for item_set_obj in itemSets_obj.item_sets:
    #     for item in item_set_obj.item_set:
    #         print(item.left, item.right, item.dot_pos, item.terminals)
    #     print(item_set_obj.index)
    