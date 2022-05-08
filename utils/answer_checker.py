import sys
import os


sys.path.append("..")

dir_name = {
    "ans": "./ans/parse_result",
    "result": "./output/parse_result"
}


result_all_names = os.listdir(dir_name["result"])
result_names = [os.path.split(i)[-1] for i in result_all_names]

for result_name in result_names:
    print("checking {}.....".format(result_name))
    ans_name = result_name
    try:
        result = open(os.path.join(dir_name["result"], result_name), "r").readlines()
    except:
        print("RESULT_FILE: {} not found\n".format(result_name))
        continue
    try:
        ans = open(os.path.join(dir_name["ans"], ans_name), "r").readlines()
    except:
        print("ANSWER_FILE: {} not found\n".format(ans_name))
        continue
    flag = True
    for index, result_line in enumerate(result):
        ans_line = ans[index]
        if result_line != ans_line:
            print("DIFFER: ")
            print("      result: {} line {}: {}".format(result_name, index, result_line))
            print("      answer: {} line {}: {}".format(ans_name, index, ans_line))
            flag = False
            
    if flag:
        print("Result {} passed successfully\n".format(result_name))
        
    