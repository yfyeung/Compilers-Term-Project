class Configs:
    # input grammar
    grammar_path = "./src/grammar.txt"
    
    # output dataStructures
    DUMP_DS_TO_FILE = True
    action_table_path = './output/action_table.txt'
    goto_table_path = './output/goto_table.txt'
    first_sets_output_path = './output/first_sets.txt'
    follow_sets_output_path = './output/follow_sets.txt'
    
    # redirect stdout
    REDIRECT_STDOUT_TO_FILE = False
    parse_result_path = './output/parse_result.txt'