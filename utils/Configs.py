class Configs:
    # input grammar
    grammar_path = "./docs/grammar_enhanced.txt"
    
    # output dataStructures
    DUMP_DS_TO_FILE = True
    action_table_path = './output/ds_details/action_table.txt'
    goto_table_path = './output/ds_details/goto_table.txt'
    first_sets_output_path = './output/ds_details/first_sets.txt'
    follow_sets_output_path = './output/ds_details/follow_sets.txt'
    item_sets_path = './output/ds_details/item_sets.txt'
    go_path = './output/ds_details/go.txt'
    
    
    # input file
    input_file_name = 'token_table_simple.txt'
    input_file = './tests/' + input_file_name
    input_stack_output_file =  './output/input_stack/' + input_file_name
    
    # redirect stdout
    REDIRECT_STDOUT_TO_FILE = True
    parse_result_path = "./output/parse_result/parse_result_" + input_file_name

    
    KW = [
        "SELECT", "FROM", "WHERE", "AS", "*",
        "INSERT", "INTO", "VALUES", "VALUE", "DEFAULT",
        "UPDATE", "SET",
        "DELETE",
        "JOIN", "LEFT", "RIGHT", "ON",
        "MIN", "MAX", "AVG", "SUM",
        "UNION", "ALL",
        "GROUP BY", "HAVING", "DISTINCT", "ORDER BY",
        "TRUE", "FALSE", "UNKNOWN", "IS", "NULL"
    ]

    OP = [
        "=", ">", "<", ">=", "<=", "!=", "<=>",
        "AND", "&&", "OR", "||", "XOR", "NOT", "!",
        "-",
        "."
    ]

    SE = [
        "(", ")", ","
    ]

    digit = "0123456789"
    letter = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

    dir_names = {
        'bin': 'bin',
        'docs': 'docs',
        'log': 'log',
        'output': 'output',
        'src': 'src',
        'tests': 'tests',
        'utils': 'utils'
    }