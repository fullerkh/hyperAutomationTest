

import json

#------------------------------------------------------------------------------
#   Table Class
#------------------------------------------------------------------------------

# Class------------------------------------------
class Record:
# each instance of the Record class is a JSON Dictionary containing both field name and field value
	# constructor----------------------------
    def __init__(self,data = {}):
		self.data = data
	# methods--------------------------------
	# Getters and Setter------------------
    def getData(self):
        return self.data.iteritems()
    def setData(self,data):
        self.data=data
        
#------------------------------------------------------------------------------
#   grabData
#------------------------------------------------------------------------------

def grabData(jsonF):
    try:
        table = []
        print "Grabbing Tabular Data from " + jsonF +".... \n     Please Wait"
        # opens json file and return the data
        with open(jsonF) as json_data:
            data = json.load(json_data)
            #print json.dumps(data, separators  = (", ", ": "), indent = 4)
        for record in data:
            entry = Record(record)
            table.append(entry)
        print "Tabular Data has been successfully grabbed"
        return table
    except Exception, e:
        print "A fatal error occurred while grabbing the Tabular data:\n", e, "\nExiting now."
        exit(-1)
        