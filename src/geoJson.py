# GeoJson.py 
# Kyle Fuller 
# 05/31/2018
# Desc: 
#    this file is to handle using our CC, SNA, and Police niehgborhoods. 
#    It provides fucntions and classes to deal with the loading and formatting of 
#    these files. The end product is to return a Map object for each geoJson used 
#    (cc, police, sna) that will provide easy access to the neighborhood name,
#    properties and geo. 

import json
from geomet import wkt
import re

#-----------------------------------------------------------------------------
#   Neighborhood Class
#-----------------------------------------------------------------------------

# Class------------------------------------------
class Neighborhood:
# each instance of the Record class is a JSON Dictionary containing both field name and field value
    # constructor----------------------------
    def __init__(self, name="", properties={}):     
        self.properties = properties
        self.name = name
    # methods--------------------------------
    # Getters and Setter------------------
    def getProperties(self):
        return str(self.properties)
    def getProperty(self, name):
        property = "no property with the name: " + name
        if hasNumbers(name):
            for title in self.properties.keys():
                if title.upper().startswith(name[:-2].upper()):
                    property = self.properties[title]
        else:
            for title in self.properties.keys():
                if title.upper() == name:
                    property = self.properties[title]
        return property
    def setProperties(self, properties):
        if type(properties) != dict:
            raise ValueError() 
        self.properties = properties
    def getNeighborhood(self):
        return self.name
    def setNeighborhood(self,neighborhood):
        self.name=neighborhood

        
#------------------------------------------------------------------------------
#   grabGeoData
#------------------------------------------------------------------------------

def grabGeoData(jsonF):
    try:
        map = {}
        print "Grabbing Geographic Data from " + jsonF + ".... \n     Please Wait"
        # opens json file and return the data
        with open(jsonF) as json_data:
            data = json.load(json_data)
        switcher = {
            "CINC_POLICE_NEIGHBORHOODSformattedFINAL.json" : "NHOOD",
            "CC_polygonsformattedFINAL.json" : "NEIGH",
            "SNA_polygonsformattedFINAL.json": "SNA_NAME"
        }
        fieldName = switcher[jsonF]
        count = 0
        for feature in data['features']:            
            name = feature['properties'][fieldName].upper()
            properties = feature['properties']
            properties.update({"GEOMETRY" : feature['geometry']})
            entry = Neighborhood(name, properties)
            #for key, value in properties.iteritems():
                #print str(key) + " " + str(value)
            count +=1
            map.update({name : entry})
            #print name
        print "Geographic Data has been successfully grabbed \nAll " +str(count)+ " records"
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

#------------------------------------------------------------------------------
#   hasNumbers
#------------------------------------------------------------------------------

def hasNumbers(inputString):
    return bool(re.search(r'\d', inputString))
#------------------------------------------------------------------------------
#   geoColumnNames
#------------------------------------------------------------------------------
# hopefully one day this'll grab the column names dynamically from a csv file to account for the differences across tableau workbooks 

def geoColumnNames():
    columnNames = {
        "CPD_NEIGHBORHOOD": [
            'NHOOD',
            'CRIME_NHOO',
            'GEOMETRY1'
        ],
        "SNA_NEIGHBORHOOD": [
            'SNA_NAME',
            'SHAPE_LENG1',
            'SHAPE_AREA1',
            'GEOMETRY2'
        ],
        "COMMUNITY_COUNCIL_NEIGHBORHOOD": [
            'NEIGH',
            'NEIGH_BOUN',
            'SHAPE_LENG',
            'SHAPE_AREA',
            'GEOMETRY'
        ]
    }
    return columnNames