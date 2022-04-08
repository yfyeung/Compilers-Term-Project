KW = [
    "SELECT", "FROM", "WHERE", "AS",
    "INSERT", "INTO", "VALUES",
    "UPDATE",
    "DELETE",
    "JOIN", "LEFT", "RIGHT",
    "MIN", "MAX", "AVG", "SUM",
    "UNION", "ALL",
    "GROUP BY", "HAVING", "DISTINCT", "ORDER BY"
    "TRUE", "FALSE", "IS", "NOT", "NULL"
]

OP = [
    "=", ">", ">=", "<=", "!=", "<=>",
    "AND", "&&", "||", "OR", "XOR",
    "."
]

SE = [
    "(", ")", ","
]

VOCABULARY = [item for item in '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ !"#$%&\'()*+,-./:;<=>?@[]^_`{|}~'] + ["\\"]