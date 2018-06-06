# Extract Automation
# Python v 2.7.10
#   v0.0 05252018 --- Start date
#   v0.1 05302018 first success
#   By Kyle Fuller

# import statments 
import argparse
import json 
import textwrap
from tableausdk import 
from tableausdk.HyperExtract import 

#------------------------------------------------------------------------------
#   Parse Arguments
#------------------------------------------------------------------------------
def parseArguments()
    parser = argparse.ArgumentParser( description='A simple demonstration of the Tableau SDK.', formatter_class=argparse.RawTextHelpFormatter )
    # (NOTE '-h' and '--help' are defined by default in ArgumentParser
    parser.add_argument( '-b', '--build', action='store_true', # default=False,
                         help=textwrap.dedent('''
                            If an extract named FILENAME exists in the current directory,
                            extend it with sample data.
                            If no Tableau extract named FILENAME exists in the current directory,
                            create one and populate it with sample data.
                            (default=%(default)s)
                            ''' ) )
    parser.add_argument( '-s', '--spatial', action='store_true', # default=False,
                         help=textwrap.dedent('''
                            Include spatial data when creating a new extract.
                            If an extract is being extended, this argument is ignored.
                            (default=%(default)s)
                            ''' ) )
    parser.add_argument( '-j', '--jsonFile', action='store', metavar='json', default='order-py.json',
                         help=textwrap.dedent('''
                            JSON file of the data to be added
                            (default='%(default)s')
                            ''' ) )
    parser.add_argument( '-e', '--EndHyper', action='store', metavar='hyper', default='order-py.hyper',
                         help=textwrap.dedent('''
                            The Hyper file to be extended 
                            (default=%(default)s)
                            ''' ) )
    return vars( parser.parse_args() )
	
#------------------------------------------------------------------------------
#   Table Class
#------------------------------------------------------------------------------

# Class------------------------------------------
class Record
# each instance of the Record class is a JSON Dictionary containing both field name and field value
	# constructor----------------------------
    def __init__(self,data = {})
		self.data = data
	# methods--------------------------------
	# Getters and Setter------------------
    def getData(self)
        return self.data.iteritems()
    def setData(self,data)
        self.data=data


#------------------------------------------------------------------------------
#   Database connection
#------------------------------------------------------------------------------

#def conData(username, password, db)
#    try
#        print Connecting to database.... n     Please Wait
#        #return cx_Oracle.connect(username, password, db)
#    except Exception, e
#        print A fatal error occurred while connecting to the oracle databasen, e, nExiting now.
#        exit(-1)

#------------------------------------------------------------------------------
#   Database GrabData
#------------------------------------------------------------------------------

def grabData(jsonF)
    try
        table = []
        print Grabbing Data from  + jsonF +.... n     Please Wait
        # opens json file and return the data
        with open(jsonF) as json_data
            data = json.load(json_data)
            #print json.dumps(data, separators  = (, ,  ), indent = 4)
        for record in data
            entry = Record(record)
            table.append(entry)
        print Data has been successfully grabbed
        return table
    except Exception, e
        print A fatal error occurred while grabbing oracle datan, e, nExiting now.
        exit(-1)


#------------------------------------------------------------------------------
#   Database field
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
#   Create Extract
#------------------------------------------------------------------------------
#   (NOTE This function assumes that the Tableau SDK Extract API is initialized)
def openExtract(
    hyper
)
    try
        # Create Extract Object
        # (NOTE The Extract constructor opens an existing extract with the
        #  given hyper filename if one exists or creates a new extract with the given
        #  filename if one does not)
        extract = Extract( hyper )

        # Define Table Schema (If we are creating a new extract)
        # (NOTE In Tableau Data Engine, all tables must be named 'Extract')
        if ( extract.hasTable( 'Extract' ) == None )
            print 'A fatal error occurred has occuredn there is no Hyper file by that name in this directorynExiting nown.'
            exit( -1 )

    except TableauException, e
        print 'A fatal error occurred while creating the new extractn', e, 'nExiting now.'
        exit( -1 )

    return extract

#------------------------------------------------------------------------------
#   Populate Extract
#------------------------------------------------------------------------------
#   (NOTE This function assumes that the Tableau SDK Extract API is initialized)
def populateExtract(
    extract,
    useSpatial,
    jsonTable
)
    try
        # Get Schema
        table = extract.openTable( 'Extract' )
        schema = table.getTableDefinition()
        numOfColumns = schema.getColumnCount()
        # Insert Data
        
        for record in jsonTable
            row = Row(schema)
            for key,value in record.getData()
                i = 0
                while i  numOfColumns
                    if key == schema.getColumnName(i)
                        setData(i, value ,row, schema) ## row += setData(field,row) 
                    i += 1
            table.insert(row)
    except TableauException, e
        print 'A fatal error occurred while populating the extractn', e, 'nExiting now.'
        exit( -1 )

#------------------------------------------------------------------------------
#   setData
#------------------------------------------------------------------------------
#   (NOTE This function assumes that the Tableau SDK Extract API is initialized)

def setData(index, value, row, schema)
    
    def setInt(row, key, value)
        row.setInteger(key, int(value))
        return row
        
    def setDoub(row, key, value)
        row.setDouble(key, float(value))
        return row
    
    def setBoo(row, key, value)
        row.setBoolean(key, value)
        return row
        
    def setDat(row, key, value) ## If I could get give it the whole int i Wouldn't need this processing method. 
        year = int(value[04])
        month = int(value[46])
        day = int(value[68])
        hour = int(value[810])
        minute = int(value[1012])
        sec = int(value[12])
        frac = 0
        row.setDateTime	(key,year,month,day,hour,minute,sec,frac)	
        return row
        
    def setCharStr(row, key, value)
        row.setCharString(key, value)
        return row
        
    def setStr(row, key, value)
        row.setString(key, value)
        return row
        
    def setSpace(row, key, value)
        row.setInteger(key, value)
        return row    
    ##-------------------------------------Switch Case
    switcher = {
        7 setInt,
        10 setDoub,
        TAB_TYPE_Boolean setBoo,
        ## TAB_TYPE_Date setDat
        13 setDat,
        #TAB_TYPE_Duration
        TAB_TYPE_CharString setCharStr,
        16 setStr,
        TAB_TYPE_Spatial setSpace
    }
#    print str(schema.getColumnType(index)) + n
#    print str(row) + n
#    print str(index) + n
#    print str(value) + n
    if value == None
        row.setNull(index)
    else 
        switcher[schema.getColumnType(index)](row, index, value)    
    return row

#------------------------------------------------------------------------------
#   Main
#------------------------------------------------------------------------------
def main()
    
    # variables for Oracle 
#    user = 'opdapub' 
#    password = 'opdapub123'
#    db = 'opdadw1.rcc.org'
    
    # Parse Arguments
    options = parseArguments()
    
    print you have chosen to use a json file named  + str(options[ 'jsonFile' ]) +  to extended the hyper named + str(options[ 'EndHyper' ]) +nhave you chosen to build it  + str(options[ 'build' ]) + ndo you have spaitial data  + str(options[ 'spatial' ])

    # Extract API Demo
    if ( options[ 'build' ] )
        # Initialize the Tableau Extract API
        ExtractAPI.initialize()
        
        # filter year - 4 years
        ##------------------------TO DO------------------------------------------

        # Create or Expand the Extract
        table = grabData( str(options[ 'jsonFile' ])) ## raw json data turned to a list of record objects (a list within a list) ## need to add filter year 
        extract = openExtract( options[ 'EndHyper' ]) ## the extract to be updated
        populateExtract( extract, options[ 'spatial' ], table ) 

        # Flush the Extract to Disk
        extract.close()

        # Close the Tableau Extract API
        ExtractAPI.cleanup()

    return 0

if __name__ == __main__
    printWelcome to hyperAutomation.py v0.1 n We hope you enjoy your stay
    retval = main()
    printthe real work begins here
    sys.exit( retval )																					
    #NOTHING APPEARS AFTER THIS