

import cx_Oracle
import datetime

#------------------------------------------------------------------------------
#   conData
#------------------------------------------------------------------------------

def conData(username, password, server, service, port):
   try:
	print "Connecting to database.... \n     Please Wait"
	dsn = cx_Oracle.makedsn(server, port, service_name=service)
        connection = cx_Oracle.connect(username, password, dsn)
	print "Database connection made to " + server
	return connection
   except Exception, e:
       print "A fatal error occurred while connecting to the oracle database:\n", e, "\nExiting now."
       exit(-1)

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

        table = []
        filterDate = fourYearsAgo()

        print "dates past " + filterDate + " will be filtered out of the selection" 

        # get the table schema
            # save as list to be used later 
        cursor = con.cursor()
        selection = cursor.execute("select COLUMN_NAME from ALL_TAB_COLUMNS where TABLE_NAME= '"+ oracleTable + "'")
        schema  = []
        for title in selection:
            schema.append(title[0])
        
        # get the table data - filter by the pst 4 years 
        selection = cursor.execute("select * from "+ oracleTable + " where to_char(DATEOCCURRED, 'yyyy-mon-dd') >= '" + str(filterDate)+ "'") # I hope date occurred is a standard field otherwise we will need more processing
        
        # take table selection and add each record to the table as a dictionary with the key being the field name and the value being the reciprocal value. 
        for row in selection:
            data = {}
            position = 0
            for item in row:
                value = item
                ## these two if statements suck and shouldn't be here. it is a lack of data standardization. 
                if schema[position]== "CPD_NEIGHBORHOOD" and value == "MT. AIRY":
                    value = "MOUNT AIRY"
                if schema[position]== "CPD_NEIGHBORHOOD" and value == "SPRING GROVE VILLAGE":
                    value = "WINTON HILLS"
                data.update({schema[position] : value})
                position +=1 
            entry = Record(data)
            table.append(entry)	
        cursor.close()
        return table
    except Exception, e:
        print "A fatal error occurred while grabbing the Tabular data:\n", e, "\nExiting now."
        exit(-1)