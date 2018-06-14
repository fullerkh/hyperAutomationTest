

import cx_Oracle
import datetime

#------------------------------------------------------------------------------
#   conData
#------------------------------------------------------------------------------

def conData(username, password, server, service, port):
   try:
	print "Connecting to database.... \n     Please Wait"
	dsn = cx_Oracle.makedsn(server, port, service_name=service)
	print "Database connection made to " + server
	return cx_Oracle.connect(username, password, dsn)
   except Exception, e:
       print "A fatal error occurred while connecting to the oracle database:\n", e, "\nExiting now."
       exit(-1)

#------------------------------------------------------------------------------
#   Table Class
#------------------------------------------------------------------------------

# Class------------------------------------------
class Table:
# each instance of the Record class is a JSON Dictionary containing both field name and field value
	# constructor----------------------------
    def __init__(self,records = [], schema = []):
		self.records = records
                self.schema = schema
	# methods--------------------------------
	# Getters and Setter------------------
    def getRecord(self, index):
        return self.records[index]
    def setRecord(self,record):
        self.records.append(record)
    def getSchema(self):
        return self.schema
    def setSchema(self,schema):
        self.schema=schema
    def getField(self,index):
        return self.schema[index]
    def setField(self,index, field):
        self.schema.insert(index, field)
        
#------------------------------------------------------------------------------
#   Table Class
#------------------------------------------------------------------------------

# Class------------------------------------------
class Record:
# each instance of the Record class is a JSON Dictionary containing both field name and field value
	# constructor----------------------------
    def __init__(self,data = []):
		self.data = data
	# methods--------------------------------
	# Getters and Setter------------------
    def getData(self):
        return self.data.iteritems()
    def setData(self,data):
        self.data=data
        
#------------------------------------------------------------------------------
#   fourYearsAgo()
#------------------------------------------------------------------------------

def fourYearsAgo():
    filter = (datetime.datetime.today()-datetime.timedelta(days=4*365)).strftime('%Y-%m-%d')
    return filter    
#------------------------------------------------------------------------------
#   grabData
#------------------------------------------------------------------------------

def grabData(oracleTable, geolist, hyperSchema, con):
    try:
        print con.version
        print con.dsn

        table = []
        filterDate = fourYearsAgo()

        print "dates past " + filterDate + " will be filtered out of the selection" 

        # get the table schema
            # save as list to be used later 
            
#        for column in hyperSchema: 
#            field += column +", "
#        selectStatment = "SELECT " + field + "FROM "+ oracleTable

        selectStatment = "SELECT * FROM "+ oracleTable
        possibleGeoColumns = {
                                "SNA_NEIGHBORHOOD":                   " LEFT JOIN KYLE_SNA_NEIGHBORHOOD s ON s.SNA_NAME = t.SNA_NEIGHBORHOOD",
                                "COMMUNITY_COUNCIL_NEIGHBORHOOD":     " LEFT JOIN KYLE_COMMUNITY_COUNCIL c ON c.NEIGH = t.COMMUNITY_COUNCIL_NEIGHBORHOOD",
                                "CPD_NEIGHBORHOOD":                   " LEFT JOIN KYLE_CPD_NEIGHBORHOOD p ON p.NHOOD = t.CPD_NEIGHBORHOOD"
                            }
        where = " where to_char(DATEOCCURRED, 'yyyy-mon-dd') >= '" + str(filterDate)+ "'"
                            
        cursor = con.cursor()
        selection = cursor.execute("select COLUMN_NAME from ALL_TAB_COLUMNS where TABLE_NAME= '"+ oracleTable + "'")
        schema  = []
        for title in selection:
            if title in possibleGeoColumns:
                selectStatment += possibleGeoColumns[title]
            schema.append(title[0])
        
        selectStatment += where # selection complete and ready
        
        
        # get the table data - filter by the pst 4 years 
        selection = cursor.execute(selectStatment) # I hope date occurred is a standard field otherwise we will need more processing
        
        for field in slection.description:
            
        # take table selection and add each record to the table as a dictionary with the key being the field name and the value being the reciprocal value. 
        count = 0 
        for row in selection:
            data = {}
            position = 0
            for item in row:
                value = item
                data.update({schema[position] : value})
                position +=1 
            entry = Record(data)
            table.append(entry)	
            count +=1 
        print count 
        cursor.close()
        return table
    except Exception, e:
        print "A fatal error occurred while grabbing the Tabular data:\n", e, "\nExiting now."
        exit(-1)