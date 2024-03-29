import os

class Configs:
    # dir_names
    dir_names = {
        'docs': 'docs',
        'output': 'output',
        'src': 'src',
        'tests': 'tests',
        'utils': 'utils'
    }

    # input grammar
    grammar_name = "grammar_sql--_enhanced.txt"

    
    test_names = []
    for file in os.listdir(dir_names["tests"]):
        if file.startswith("testcase-") and file.endswith(".sql"):
            test_names.append(file) 


    # token info
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

    # output dataStructures
    DUMP_DS_TO_FILE = True

    grammar_path = os.path.join(dir_names['utils'], grammar_name)
    action_table_path = os.path.join(dir_names['output'], 'ds_details', grammar_name.replace(".txt", "_") + 'action_table.txt')
    goto_table_path = os.path.join(dir_names['output'], 'ds_details', grammar_name.replace(".txt", "_") + 'goto_table.txt')
    first_sets_output_path = os.path.join(dir_names['output'], 'ds_details', grammar_name.replace(".txt", "_") + 'first_sets.txt')
    follow_sets_output_path = os.path.join(dir_names['output'], 'ds_details', grammar_name.replace(".txt", "_") + 'follow_sets.txt')
    item_sets_path = os.path.join(dir_names['output'], 'ds_details', grammar_name.replace(".txt", "_") + 'item_sets.txt')
    go_path = os.path.join(dir_names['output'], 'ds_details', grammar_name.replace(".txt", "_") + 'go.txt')
    
    grammar_path_e = os.path.join(dir_names['output'], 'ds_entity', grammar_name.replace(".txt", "_") + 'grammar.pkl')
    analysis_table_path_e = os.path.join(dir_names['output'], 'ds_entity', grammar_name.replace(".txt", "_") + 'analysis_table.pkl')
    first_sets_output_path_e = os.path.join(dir_names['output'], 'ds_entity', grammar_name.replace(".txt", "_") + 'first_sets.pkl')
    follow_sets_output_path_e = os.path.join(dir_names['output'], 'ds_entity', grammar_name.replace(".txt", "_") + 'follow_sets.pkl')
    item_sets_path_e = os.path.join(dir_names['output'], 'ds_entity', grammar_name.replace(".txt", "_") + 'item_sets.pkl')
    go_path_e = os.path.join(dir_names['output'], 'ds_entity', grammar_name.replace(".txt", "_") + 'go.pkl')


    # 创建output的子文件夹
    if not os.path.exists(os.path.join(dir_names["output"], "ds_details")):
        os.mkdir(os.path.join(dir_names["output"], "ds_details"))
    if not os.path.exists(os.path.join(dir_names["output"], "ds_entity")):
        os.mkdir(os.path.join(dir_names["output"], "ds_entity"))
    if not os.path.exists(os.path.join(dir_names["output"], "input_stack")):
        os.mkdir(os.path.join(dir_names["output"], "input_stack"))
    if not os.path.exists(os.path.join(dir_names["output"], "parse_result")):
        os.mkdir(os.path.join(dir_names["output"], "parse_result"))
    if not os.path.exists(os.path.join(dir_names["output"], "token_table")):
        os.mkdir(os.path.join(dir_names["output"], "token_table"))
        
    