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

#------------------------------------------------------------------------------
#   Neighborhood Class
#------------------------------------------------------------------------------

# Class------------------------------------------
class Neighborhood:
# each instance of the Record class is a JSON Dictionary containing both field name and field value
    # constructor----------------------------
    def __init__(self, name="", properties={}):     
#        self.geometry = geometry
        self.properties = properties
        self.name = name
    # methods--------------------------------
    # Getters and Setter------------------
#    def getGeo(self):
#        return str(self.geometry)
#    def setGeo(self, geometry):
#        if type(geometry) != dict:
#            raise ValueError() 
#        self.geometry = geometry
    def getProperties(self):
        return str(self.properties)
    def getProperty(self, name):
        #print name[:-2].upper()
        for title in self.properties.keys():
            if title.upper().startswith(name[:-2].upper()):
                #print "name accepted"
                return self.properties[title]
        return "no property with that name"
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
            "Police_polygonsformatted.json" : "NHOOD",
            "CC_polygonsformatted.json" : "NEIGH",
            "SNA_polygonsformatted.json": "SNA_NAME"
        }
        fieldName = switcher[jsonF]
        count = 0
        for feature in data['features']:            
            name = feature['properties'][fieldName].upper()
            properties = feature['properties']
            properties.update({"GEOMETRY" : [feature['geometry']['type'], feature['geometry']['coordinates']]})
            entry = Neighborhood(name, properties)
            count +=1
            map.update({name : entry})
        
        print "Geographic Data has been successfully grabbed \nAll " +str(count)+ " records"
        return map
    except Exception, e:
        print "A fatal error occurred while grabbing the Geographic data in " + jsonF + ":\n", e, "\nExiting now."
        exit(-1)
    
#------------------------------------------------------------------------------
#   geoColumnNames
#------------------------------------------------------------------------------
# hopefully one day this'll grab the column names dynamically from a csv file to account for the differences across tableau workbooks 

def geoColumnNames():
    columnNames = {
        "CPD_NEIGHBORHOOD": [
            'NHOOD',
            'CRIME_NHOO',
            'Geometry1'
        ],
        "SNA_NEIGHBORHOD": [
            'SNA_NAME',
            'Shape_Leng1',
            'Shape_Area1',
            'Geometry2'
        ],
        "COMMUNITY_COUNCIL_NEIGHBORHOOD": [
            'NEIGH',
            'NEIGH_BOUN',
            'Shape_Leng',
            'Shape_Area',
            'Geometry'
        ]
    }
    return columnNames