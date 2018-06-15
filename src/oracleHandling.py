

import cx_Oracle
import datetime

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
    def allRecords(self):
        return self.records
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
#   fourYearsAgo()
#------------------------------------------------------------------------------

def fourYearsAgo():
    filter = (datetime.datetime.today()-datetime.timedelta(days=4*365)).strftime('%Y-%m-%d')
    return filter    
#------------------------------------------------------------------------------
#   grabData
#------------------------------------------------------------------------------

def grabData(oracleTable, con):
    try:
        print con.version
        print con.dsn

        table = Table()
        #------------------------------------------------------------------------------ SELECT STATEMENT AND CURSOR EXECUTION
        filterDate = fourYearsAgo()
        print "dates past " + filterDate + " will be filtered out of the selection" 
        
        cursor = con.cursor()
        selection = cursor.execute("select COLUMN_NAME from ALL_TAB_COLUMNS where TABLE_NAME= '"+ oracleTable + "'")
        possibleGeoColumns = {
                                "SNA_NEIGHBORHOOD":                   " LEFT JOIN KYLE_SNA_NEIGHBORHOOD s ON s.SNA_NAME = t.SNA_NEIGHBORHOOD",
                                "COMMUNITY_COUNCIL_NEIGHBORHOOD":     " LEFT JOIN KYLE_COMMUNITY_COUNCIL c ON c.NEIGH = t.COMMUNITY_COUNCIL_NEIGHBORHOOD",
                                "CPD_NEIGHBORHOOD":                   " LEFT JOIN KYLE_CPD_NEIGHBORHOOD p ON p.NHOOD = t.CPD_NEIGHBORHOOD"
                            }
        selectStatment = "SELECT * FROM "+ oracleTable
        for title in selection:
            if title[0] in possibleGeoColumns:
                selectStatment += possibleGeoColumns[title[0]]
        # get the table data - filter by the pst 4 years        
        where = " where to_char(DATEOCCURRED, 'yyyy-mon-dd') >= '" + str(filterDate)+ "'"
        selectStatment += where # selection complete and ready
        print selectStatment
        selection = cursor.execute(selectStatment) 
        #------------------------------------------------------------------------------ SCHEMA
        # set the table schema
        counter = 0
        for field in selection.description:
            table.setField(counter, field[0])
            counter += 1
        #------------------------------------------------------------------------------ TABLE POPULATE
        # take table selection and add each record to the table as a list
        counter = 0 
        for row in selection:
            table.setRecord(row)
            
        return table
    except Exception, e:
        print "A fatal error occurred while grabbing the Tabular data:\n", e, "\nExiting now."
        exit(-1)