import json

with open('shootingstestA.json') as json_data:
    data = json.load(json_data)
    print json.dumps(data, separators  = (", ", ": "), indent = 4)
    


file = open("shootingstest - Copy.json","w")

file.write(json.dumps(data, separators  = (", ", ": "), indent = 4))




##   py -2.7 hyperAutomationtest.py -b -j shootingstestComplete.json -e shootingsWorkbook.hyper