import json


jsonsGeo = ["CINC_POLICE_NEIGHBORHOODSformatted", "CC_polygonsformatted", "SNA_polygonsformatted"]
jsonsProperties = ["CINC_POLICE_NEIGHBORHOODSformattedOriginal", "CC_polygonsformattedOriginal", "SNA_polygonsformattedOriginal"]

jsonsGeoFINAL = ["CINC_POLICE_NEIGHBORHOODSformattedFINAL", "CC_polygonsformattedFINAL", "SNA_polygonsformattedFINAL"] 


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

def changeGeoJsonProperties(jsonsProperties,jsonsGeo):	
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
	
	
# NEVER WORKED 
# def deleteZaxis(jsonsGeoFINAL):
	# for entry in jsonsGeoFINAL:
		# with open(entry +'.json') as json_data:
			# data = json.load(json_data)
			# for feature in data['features']:
				# for key in feature['geometry']:
					# if key == 'coordinates':
						# for polygon in feature['geometry'][key]:
							# newPolygon = polygonPoints(polygon)
							# polygon = newPolygon
			# file = open(entry + "FINAL.json","w")
			# file.write(json.dumps(data, separators  = (", ", ": "), indent = 4))
			# file.close()

# def polygonPoints(polygon):
	# newPolygon = []
	# for point in polygon:
		# x= point[0]
		# y= point[1]
		# print str(x) + "   " + str(y)
		# point = [x,y]
		# newPolygon.append(point)
	# return newPolygon
		

changeGeoJsonProperties(jsonsProperties,jsonsGeo)



##   py -2.7 hyperAutomationtest.py -b -j shootingstestComplete.json -e shootingsWorkbook.hyper