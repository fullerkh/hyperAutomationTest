# Extract Automation
# Python v 2.7.10
#   v0.0: 05/25/2018 --- Start date
#   v0.1: 05/30/2018 first success with tabular data
#   v0.15: 05/31/2018 splitting hyperautmationtest.py into 4 separate py 
#   By: Kyle Fuller

# ex: py -2.7 hyperautomationtest.py -b -j SHOOTINGS_TEST_FOR_KYLE.JSON -e SHOOTINGS_TEST_FOR_KYLE.hyper # will no longer work as the script requires fields based off of the input geo 
# ex  py -2.7 hyperautomationtest.py -b -j SHOOTINGS_TEST_FOR_KYLE.JSON -e Shootings_Test.hyper

# import statments 
import argparse
import textwrap

# import of other python files. contain most of the methods and classes. 
# these files also contain the other relevant import statements like 
    # import json 
    # from tableausdk import *
    # from tableausdk.HyperExtract import *
from geoJson import *
from jsonHandling import *
from tableauExtract import * 

#------------------------------------------------------------------------------
#   Parse Arguments
#------------------------------------------------------------------------------
def parseArguments():
    parser = argparse.ArgumentParser( description='A simple demonstration of the Tableau SDK.', formatter_class=argparse.RawTextHelpFormatter )
    # (NOTE: '-h' and '--help' are defined by default in ArgumentParser
    parser.add_argument( '-b', '--build', action='store_true', # default=False,
                         help=textwrap.dedent('''\
                            If an extract named FILENAME exists in the current directory,
                            extend it with sample data.
                            If no Tableau extract named FILENAME exists in the current directory,
                            create one and populate it with sample data.
                            (default=%(default)s)
                            ''' ) )
    parser.add_argument( '-j', '--jsonFile', action='store', metavar='json', default='order-py.json',
                         help=textwrap.dedent('''\
                            JSON file of the data to be added
                            (default='%(default)s')
                            ''' ) )
    parser.add_argument( '-e', '--EndHyper', action='store', metavar='hyper', default='order-py.hyper',
                         help=textwrap.dedent('''\
                            The Hyper file to be extended 
                            (default=%(default)s)
                            ''' ) )
    return vars( parser.parse_args() )
	
#------------------------------------------------------------------------------
#   Database connection
#------------------------------------------------------------------------------

#def conData(username, password, db):
#    try:
#        print "Connecting to database.... \n     Please Wait"
#        #return cx_Oracle.connect(username, password, db)
#    except Exception, e:
#        print "A fatal error occurred while connecting to the oracle database:\n", e, "\nExiting now."
#        exit(-1)

#------------------------------------------------------------------------------
#   Main
#------------------------------------------------------------------------------
def main():
    
    # variables for Oracle 
#    user = 'opdapub' 
#    password = 'opdapub123'
#    db = 'opdadw1.rcc.org'
    # variables for GeoJson 
    
    # Parse Arguments
    options = parseArguments()
    
    print "you have chosen to use a json file named " + str(options[ 'jsonFile' ]) + " to extended the hyper named "+ str(options[ 'EndHyper' ]) +"\nhave you chosen to build it?: " + str(options[ 'build' ])

    # Extract API Demo
    if ( options[ 'build' ] ):
        # Initialize the Tableau Extract API
        ExtractAPI.initialize()
        
        # variables for GeoJson
        police_polygons = grabGeoData("Police_polygonsformatted.json")
        cc_polygons = grabGeoData("CC_polygonsformatted.json")
        sna_polygons = grabGeoData("SNA_polygonsformatted.json")
        allGeo = {"CPD_NEIGHBORHOOD": police_polygons,"COMMUNITY_COUNCIL_NEIGHBORHOOD": cc_polygons,"SNA_NEIGHBORHOD": sna_polygons}
        
        
        # grab the shp file columns 
        geoColumns = geoColumnNames()
        
        
        
        # filter year - 4 years
        ##------------------------TO DO------------------------------------------

        # Create or Expand the Extract
        table = grabData( str(options[ 'jsonFile' ])) ## raw json data turned to a list of record objects (a list within a list) ## need to add filter year 
            # grab the 3 GeoJson files with out Geo data and make them tables as well.
        extract = openExtract( options[ 'EndHyper' ]) ## the extract to be updated
        populateExtract( extract, table, allGeo, geoColumns ) 

        # Flush the Extract to Disk
        extract.close()

        # Close the Tableau Extract API
        ExtractAPI.cleanup()

    return 0

if __name__ == "__main__":
    print"Welcome to hyperAutomation.py v0.1 \n We hope you enjoy your stay"
    retval = main()
    print"the real work begins here"
    sys.exit( retval )																					
    #NOTHING APPEARS AFTER THIS