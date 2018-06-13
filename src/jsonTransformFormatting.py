import json
import re
from geomet import wkt


jsonsGeo = ["CINC_POLICE_NEIGHBORHOODSformatted", "CC_polygonsformatted", "SNA_polygonsformatted"]
jsonsProperties = ["CINC_POLICE_NEIGHBORHOODSformattedOriginal", "CC_polygonsformattedOriginal", "SNA_polygonsformattedOriginal"]

jsonsGeoFINAL = ["CINC_POLICE_NEIGHBORHOODSformattedFINAL", "CC_polygonsformattedFINAL", "SNA_polygonsformattedFINAL"] 
#jsonsGeoFINAL = ["convertformatted"]

def grabData(jsonF):
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
                
def longestStr(jsonF):
    jsonF = jsonF + ".json"
    try:
        counter = 0
        with open(jsonF) as json_data:
            data = json.load(json_data)
            print "data opened"
            for feature in data['features']:
                #print feature
                if 'geometry' in feature: 
                    print str(feature['geometry']['coordinates'])
                    length = len(str(feature['geometry']['coordinates']))
                    if length > counter:
                        print "no"
                        counter = length
        return counter
    except Exception, e:
        print "A fatal error occurred while grabbing the Geographic data in " + jsonF + ":\n", e, "\nExiting now."
        exit(-1)
	
	
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
		

#changeGeoJsonProperties(jsonsProperties,jsonsGeo)

def grabGeoData(jsonF):
    try:
        counter = 0
        neighborhoods =[]
        print "Grabbing Geographic Data from " + jsonF + ".... \n     Please Wait"
        # opens json file and return the data
        with open(jsonF) as json_data:
            data = json.load(json_data)
        count = 0
        for feature in data['features']:
            entry = {}
            for propertyK, propertyV in feature.iteritems():
                if propertyK == "geometry": 
                    propertyV= geojson2wkt(propertyV)
                    if len(propertyV) > counter:
                        count = len(propertyV)
                    entry.update({propertyK:propertyV})
                    print "geo"
                if propertyK == "properties": 
                    for key, value in propertyV.iteritems():
                        print key + "     " + str(value) 
                        entry.update({key:value})
                neighborhoods.append(entry)
        map = {"neighborhoods" : neighborhoods}
        print "Geographic Data has been successfully grabbed \nThe longest string was :  " +str(count)+ " chars long for this file"
        return map
    except Exception, e:
        print "A fatal error occurred while grabbing the Geographic data in " + jsonF + ":\n", e, "\nExiting now."
        exit(-1)
      
#------------------------------------------------------------------------------
#   geojson2wkt
#------------------------------------------------------------------------------

def geojson2wkt(geojson):
    #print geojson
    coordinates = wkt.dumps(geojson, 6)
    # print what kind of geometry we are dealing with
    #print coordinates[0:coordinates.find(" ")]
    return coordinates

def writeJson(name, data):
        final = json.dumps(data, separators  = (", ", ": "), indent = 4)
	file = open(name + "-brandon1.json","w")
	file.write(final)

for map in jsonsGeoFINAL:
    map = map + ".json"
    data = grabGeoData(map)
    writeJson(map, data)
    


##   py -2.7 hyperAutomationtest.py -b -j shootingstestComplete.json -e shootingsWorkbook.hyper