import json


jsonsGeo = ["Police_polygonsformatted", "CC_polygonsformatted", "SNA_polygonsformatted"]
jsonsProperties = ["Police_polygonsformattedOriginal", "CC_polygonsformattedOriginal", "SNA_polygonsformattedOriginal"]


def grabGeoData(jsonF):
    try:
        mapProperties = []
        print "Grabbing properties data from " + jsonF + ".... \n     Please Wait"
        # opens json file and return the data
        with open(jsonF) as json_data:
            data = json.load(json_data)
			
        for feature in data['features']:
			mapProperties.append(feature['properties'])
            #print name
        print "Geographic Data has been successfully grabbed "
        return mapProperties
    except Exception, e:
        print "A fatal error occurred while grabbing the Geographic data in " + jsonF + ":\n", e, "\nExiting now."
        exit(-1)

		
jsonsPropertyValues= {}
for items in jsonsProperties:
	properties = grabGeoData(items +'.json')
	jsonsPropertyValues.update({items : properties})
	
count = 0
while count < len(jsonsGeo):
	with open(jsonsGeo[count] +'.json') as json_data:
		data = json.load(json_data)
		neighborhood = 0
		for feature in data['features']:
			feature['properties'] = jsonsPropertyValues[jsonsProperties[count]][neighborhood]
			neighborhood +=1
		file = open(jsonsGeo[count] + "FINAL.json","w")
		file.write(json.dumps(data, separators  = (", ", ": "), indent = 4))
		file.close()
	count += 1 
	





##   py -2.7 hyperAutomationtest.py -b -j shootingstestComplete.json -e shootingsWorkbook.hyper