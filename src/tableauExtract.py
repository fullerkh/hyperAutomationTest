from geoJson import *
from tableausdk import *
from tableausdk.HyperExtract import *
#------------------------------------------------------------------------------
#   Create Extract
#------------------------------------------------------------------------------
#   (NOTE: This function assumes that the Tableau SDK Extract API is initialized)
def openExtract(
    hyper
):
    try:
        # Create Extract Object
        # (NOTE: The Extract constructor opens an existing extract with the
        #  given hyper filename if one exists or creates a new extract with the given
        #  filename if one does not)
        extract = Extract( hyper )

        # Define Table Schema (If we are creating a new extract)
        # (NOTE: In Tableau Data Engine, all tables must be named 'Extract')
        if ( extract.hasTable( 'Extract' ) == None ):
            print 'A fatal error occurred has occured:\n there is no Hyper file by that name in this directory:\nExiting now\n.'
            exit( -1 )

    except TableauException, e:
        print 'A fatal error occurred while creating the new extract:\n', e, '\nExiting now.'
        exit( -1 )

    return extract

#------------------------------------------------------------------------------
#   Populate Extract
#------------------------------------------------------------------------------
#   (NOTE: This function assumes that the Tableau SDK Extract API is initialized)
def populateExtract(extract, oracleTable, allGeo, geoColumns):
    
    try:
        # Get Schema
        table = extract.openTable( 'Extract' )
        schema = table.getTableDefinition()
        getColumns = allColumns(schema)
        # Insert Data
        
        for record in oracleTable:
            row = Row(schema)
            for key,value in record.getData():
                setData(getColumns[key], value ,row, schema)
                if key in geoColumns: # if the column name is CPD_NEIGHBORHOOD, SNA_NEIGHBORHOD, or COMMUNITY_COUNCIL_NEIGHBORHOOD
                    for column in geoColumns[key]: # for the column names in geoColumns( whichever key it hit)
                        #print "allGeo[" + str(key) + "][" + str(value) + "].getProperty(" + str(column) + ")"
                        if value != None and value != 'N/A':
                            cellValue = allGeo[key][value].getProperty(column) 
                        else: 
                            #print "allGeo[" + str(key) + "][" + str(value) + "].getProperty(" + str(column) + ")"
                            cellValue = None
                            
                        setData(getColumns[column], cellValue ,row, schema) # find the column position in the hyper schema and set the the value. # have to find out how to get the proper value. 
        table.insert(row)
    except TableauException, e:
        print 'A fatal error occurred while populating the extract:\n', e, '\nExiting now.'
        exit( -1 )

#------------------------------------------------------------------------------
#   allColumns  
#------------------------------------------------------------------------------
#   (NOTE: This function assumes that the Tableau SDK Extract API is initialized)

def allColumns(schema):
    columnPositions = {}
    position = 0
    while position < schema.getColumnCount():
        columnName = schema.getColumnName(position).upper()
        print columnName
        columnPositions.update({columnName : position})
        position+=1
# Columns = allColumns(schema) # will use values to search for keys 
# print Columns.keys()[Columns.values().index(index)]    
    return columnPositions

#------------------------------------------------------------------------------
#   setData SUBTYPES 
#------------------------------------------------------------------------------
#   (NOTE: This function assumes that the Tableau SDK Extract API is initialized)

def setInt(row, index, value):
    row.setInteger(index, int(value))
    return row

def setDoub(row, index, value):
    row.setDouble(index, float(value))
    return row

def setBoo(row, index, value):
    row.setBoolean(index, value)
    return row

def setDat(row, index, value):
    year = value.year
    month = value.month
    day = value.day
    hour = value.hour
    minute = value.minute
    sec = value.second
    frac = 0
    row.setDateTime(index,year,month,day,hour,minute,sec,frac)	
    return row

def setCharStr(row, index, value):
    row.setCharString(index, value)
    return row

def setStr(row, index, value):
    row.setString(index, value)
    return row

def setSpace(row, index, value):
    # this is where things go wrong 
    coordinates = str(value[0]).upper() + '(' + str(value[1]) + ')'
    #print coordinates
    #row.setSpatial( 8, "POINT (30 10)" )
    row.setSpatial(index, "POINT (30 10)") # coordinates will be where the fake data is. 
    return row    

#------------------------------------------------------------------------------
#   setData
#------------------------------------------------------------------------------
#  
def setData(index, value, row, schema):
    ##-------------------------------------Switch Case
    switcher = {
        7: setInt,
        10: setDoub,
        "TAB_TYPE_Boolean": setBoo,
        ## "TAB_TYPE_Date": setDat
        13: setDat,
        #"TAB_TYPE_Duration":
        "TAB_TYPE_CharString": setCharStr,
        16: setStr,
        17: setSpace
    }
#    print str(schema.getColumnType(index)) + "\n"
#    print str(row) + "\n"
#    print str(index) + "\n"
#    print str(value) + "\n"
    if value == None:
        row.setNull(index)
    else: 
        switcher[schema.getColumnType(index)](row, index, value)  
    return row