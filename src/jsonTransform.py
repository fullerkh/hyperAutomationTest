import json

jsons = ["SNA_polygons", "Police_polygons", "CC_polygons"]

for doc in jsons:
	with open(doc +'.json') as json_data:
		data = json.load(json_data)
		print json.dumps(data, separators  = (", ", ": "), indent = 4)
		


	file = open(doc + "formatted.json","w")

	file.write(json.dumps(data, separators  = (", ", ": "), indent = 4))




##   py -2.7 hyperAutomationtest.py -b -j shootingstestComplete.json -e shootingsWorkbook.hyper