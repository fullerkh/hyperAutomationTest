from geoJson import *
from tableausdk import *
from tableausdk.HyperExtract import *
import os
#------------------------------------------------------------------------------
#   Create Extract
#------------------------------------------------------------------------------
#   (NOTE: This function assumes that the Tableau SDK Extract API is initialized)
def openExtract(hyper):
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
#   GrabSchema 
#------------------------------------------------------------------------------
#   (NOTE: This function assumes that the Tableau SDK Extract API is initialized)

def grabSchema(hyper):
    toCreate = {}
    extract = Extract( hyper )
    hyper = extract.openTable( 'Extract' )
    schema = hyper.getTableDefinition()
    position = 0
    while position < schema.getColumnCount():
        columnName = schema.getColumnName(position)
        columnType = schema.getColumnType(position)
        #print columnName
        toCreate.update({columnName : columnType})
        print columnName + " " + str(columnType)
        position+=1
    return toCreate

#------------------------------------------------------------------------------
#   delete hyper  
#------------------------------------------------------------------------------
#   (NOTE: This function assumes that the Tableau SDK Extract API is initialized)

def deleteHyper(name):
    extract = Extract( name )
    extract.close()
    os.remove(name)
    print "the old hyper named " + name + " has been deleted"

#------------------------------------------------------------------------------
#   create hyper  
#------------------------------------------------------------------------------
#   (NOTE: This function assumes that the Tableau SDK Extract API is initialized)

def createHyper(name, oldSchema):
    extract = Extract(name)
    newSchema = TableDefinition()
    newSchema.setDefaultCollation( Collation.EN_GB )
    for fieldkey, fieldvalue in oldSchema.iteritems():
        newSchema.addColumn(fieldkey, fieldvalue)
    table = extract.addTable( 'Extract', newSchema )
    print "A new hyper named " + name + " has been created"
    return table

#------------------------------------------------------------------------------
#   Populate Extract
#------------------------------------------------------------------------------
#   (NOTE: This function assumes that the Tableau SDK Extract API is initialized)
def populateExtract(extract, oracleTable):
    
    try:
        errorColumn = ""
        count = 0
        
        # Get Schema
        table = extract.openTable( 'Extract' )
        schema = table.getTableDefinition()
        getColumns = allColumns(schema)
        
        records = oracleTable.allRecords
        oracleSchema = oracleTable.getSchema
        
        # Insert Data
        for record in records:
            row = Row(schema)
            index = 0
            for value in record:
                errorColumn = " at " + getColumns[oracleSchema[index]] + " in the oracle table"
                # might be able to get away with doing a simple setData if fields are matching and unique --- setData(getColumns[oracleSchema[index]], value ,row, schema)
                if value != None and value != 'N/A':
                    cellValue = value 
                else: 
                    cellValue = None
                setData(getColumns[oracleSchema[index]], cellValue ,row, schema)
                index += 1
            table.insert(row)
        print "all " + str(count) + " records added"
    except TableauException, e:
        print 'A fatal error occurred while populating the extract'+ errorColumn +' the record count was = '+ count +':\n', e, '\nExiting now.'
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
        #print columnName
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
    row.setString(index, value + " test5") # add + "  TEST" to ensure that new rows are ebeing added. 
    return row

def setSpace(row, index, value):
    #print value 
    #take geojson coordinates and turn them ino wkt --- the way that's compatible with the extract api 
    row.setSpatial(index, value)
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