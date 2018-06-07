# Extract Automation
# Python v 2.7.10
#   v0.0: 05/25/2018 --- Start date
#   v0.1: 05/30/2018 first success with tabular data
#   v0.15: 05/31/2018 splitting hyperautmationtest.py into 4 separate py 
#   v0.20: 06/04/2018 updated populate data (easier). assumes geoData present -- TOP PRIPORITY setSpatial not working. cx_Oracle not imported
#   v0.25: 06/05/2018 substitute cx_Oracle for json files. runs the shootings hyper perfectly with fake geo data. -- TOP PRIORITY setSpatial not working. need to be able to delete files. 
#   By: Kyle Fuller

# ex: py -2.7 hyperautomationtest.py -b -j SHOOTINGS_TEST_FOR_KYLE.JSON -e SHOOTINGS_TEST_FOR_KYLE.hyper # will no longer work as the script requires fields based off of the input geo 
# v0.20 ex:  py -2.7 hyperautomationtest.py -b -j SHOOTINGS_TEST_FOR_KYLE.JSON -e Shootings_Test.hyper # now uses oracle db
# v0.25 ex:  py -2.7 hyperautomationtest.py -b -d OPEN_DATA_CPD_SHOOTINGS_X -e Shootings_Test.hyper 

# import statments 
import argparse
import textwrap

# import of other python files. contain most of the methods and classes. 
# these files also contain the other relevant import statements like 
    # import json 
    # from tableausdk import *
    # from tableausdk.HyperExtract import *
from geoJson import *
from oracleHandling import *
from tableauExtract import * 


# import oracle credentials 
import sys
sys.path.insert(0, 'C:/Users/kyle.fuller/Documents/NetBeansProjects')
from oracleCred import oracleLogin 


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
    parser.add_argument( '-d', '--Database', action='store', metavar='json', default='order-py.json',
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
#   Main
#------------------------------------------------------------------------------
def main():
    
    # Parse Arguments
    options = parseArguments()
    
    print "you have chosen to use a json file named " + str(options[ 'Database' ]) + " to extended the hyper named "+ str(options[ 'EndHyper' ]) +"\nhave you chosen to build it?: " + str(options[ 'build' ])

    # Extract API Demo
    if ( options[ 'build' ] ):
        # Initialize the Tableau Extract API
        ExtractAPI.initialize()
        
        # variables for GeoJson
        police_polygons = grabGeoData("Police_polygonsformattedFINAL.json")
        cc_polygons = grabGeoData("CC_polygonsformattedFINAL.json")
        sna_polygons = grabGeoData("SNA_polygonsformattedFINAL.json")
        allGeo = {"CPD_NEIGHBORHOOD": police_polygons,"COMMUNITY_COUNCIL_NEIGHBORHOOD": cc_polygons,"SNA_NEIGHBORHOOD": sna_polygons}
        
        # grab the shp file columns 
        geoColumns = geoColumnNames()
        
        #variables for Oracle # will be used to make the connection. DOES NOT CHANGE// imported from another file. 
        # function shown below
#        def oracleLogin():
#            #variables for Oracle # will be used to make the connection. DOES NOT CHANGE 
#            login = {"username" : 'name', "password" : 'pass', "server" : 'server.com', "service" : 'serviceName', "port" : int}
#            return login
        credentials = oracleLogin()
        
        # connect and grab oracle table
        connection = conData(credentials["username"], credentials["password"], credentials["server"], credentials["service"], credentials["port"])
        table = grabData(options[ 'Database' ], connection) ## raw json data turned to a list of record objects (a list within a list) ## need to add filter year 
            
        # Create or Expand the Extract
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