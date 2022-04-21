class Configs:
    # input grammar
    grammar_path = "./docs/grammar_enhanced.txt"
    
    # output dataStructures
    DUMP_DS_TO_FILE = True
    action_table_path = './output/action_table.txt'
    goto_table_path = './output/goto_table.txt'
    first_sets_output_path = './output/first_sets.txt'
    follow_sets_output_path = './output/follow_sets.txt'
    item_sets_path = './output/item_sets.txt'
    go_path = './output/go.txt'
    
    # redirect stdout
    REDIRECT_STDOUT_TO_FILE = False
    parse_result_path = './output/parse_result.txt'
    
    
    input_file_name = 'token_table_simple.txt'
    input_file = './tests/' + input_file_name
    input_stack_output_file =  './output/input_stack/' + input_file_name