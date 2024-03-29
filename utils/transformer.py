from src.LR1_parser.ds.Stack import Stack

input_folder = "./tests/"
waiting_to_transform_file = "token_table_annotation.txt"
output_folder = "./output/input_stack/"
transformed_file = "token_table_annotation_trans.txt"

KW = {
    1: "SELECT",
    2: "FROM",
    3: "WHERE",
    4: "AS",
    5: "*",
    6: "INSERT",
    7: "INTO",
    8: "VALUES",
    9: "VALUE",
    10: "DEFAULT",
    11: "UPDATE",
    12: "SET",
    13: "DELETE",
    14: "JOIN",
    15: "LEFT",
    16: "RIGHT",
    17: "ON",
    18: "MIN",
    19: "MAX",
    20: "AVG",
    21: "SUM",
    22: "UNION",
    23: "ALL",
    24: "GROUP BY",
    25: "HAVING",
    26: "DISTINCT",
    27: "ORDER BY",
    28: "TRUE",
    29: "FALSE",
    30: "UNKNOWN",
    31: "IS",
    32: "NULL"
}

OP = {
    1: "=",
    2: ">",
    3: "<",
    4: ">=",
    5: "<=",
    6: "!=",
    7: "<=>",
    8: "AND",
    9: "&&",
    10: "OR",
    11: "||",
    12: "XOR",
    13: "NOT",
    14: "!",
    15: "-",
    16: "."
}

SE = {
    1: "(",
    2: ")",
    3: ","
}

def token2inputStack(input_file, output_file):
    input_stack_reversed = Stack()
    
    with open(input_file, "r") as f:
        input_lines = f.readlines()
    output_file_ = open(output_file, "w")
    for index, line in enumerate(input_lines):
        if index == len(input_lines) - 1:
            line = line + "\n"
        words = line.split("\t")
        items = words[1][1:-2].split(",")
        type = items[0]
        content = items[1]

        terminal = None
        if type == "KW":
            terminal = KW[int(content)]
        elif type == "OP":
            terminal = OP[int(content)]
        elif type == "SE":
            terminal = SE[int(content)]
        elif type == "IDN":
            terminal = "IDN"
        elif type == "INT":
            terminal = "INT"
        elif type == "FLOAT":
            terminal = "FLOAT"
        elif type == "STRING":
            terminal = "STRING"
        else:
            assert False, "Unknown type: " + type

        print(terminal, file=output_file_)
        input_stack_reversed.push(terminal)
    input_stack_reversed.push("#")
    input_stack = Stack()
    while not input_stack_reversed.isEmpty():
        input_stack.push(input_stack_reversed.pop())

    return input_stack
