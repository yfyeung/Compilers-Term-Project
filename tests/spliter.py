splited_file = "./tests/testcase-all.sql"

f = open(splited_file, 'r')
cnt = 0

content = f.read().split("\n\n")

for c in content:
    with open("./tests/testcase-{}.sql".format(cnt), 'w') as f:
        f.write(c)
    cnt += 1
    