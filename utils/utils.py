KW = [
    "SELECT", "FROM", "WHERE", "AS", "*"
    "INSERT", "INTO", "VALUES", "VALUE", "DEFAULT"
    "UPDATE", "SET"
    "DELETE",
    "JOIN", "LEFT", "RIGHT", "ON"
    "MIN", "MAX", "AVG", "SUM",
    "UNION", "ALL",
    "GROUP BY", "HAVING", "DISTINCT", "ORDER BY"
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

VOCABULARY = [_ for _ in '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ !"#$%&\'()*+,-./:;<=>?@[]^_`{|}~'] + ["\\"]

dir_names = {
    'bin': 'bin',
    'docs': 'docs',
    'log': 'log',
    'output': 'output',
    'src': 'src',
    'tests': 'tests',
    'utils': 'utils'
}