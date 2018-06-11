# hyperAutomationTest

# Extract Automation
# Python v 2.7.10

# requires: 
# the tableau extract api 2.0 
# cx_oracle 5.3

#   v0.0: 05/25/2018 --- Start date
#   v0.1: 05/30/2018 first success with tabular data
#   v0.15: 05/31/2018 splitting hyperautmationtest.py into 4 separate py 
#   v0.20: 06/04/2018 updated populate data (easier). assumes geoData present -- TOP PRIPORITY setSpatial not working. cx_Oracle not imported
#   v0.25: 06/05/2018 substitute cx_Oracle for json files. runs the shootings hyper perfectly with fake geo data. -- TOP PRIORITY setSpatial not working. need to be able to delete files. 
#   By: Kyle Fuller

# ex: py -2.7 hyperautomationtest.py -b -j SHOOTINGS_TEST_FOR_KYLE.JSON -e SHOOTINGS_TEST_FOR_KYLE.hyper # will no longer work as the script requires fields based off of the input geo 
# v0.20 ex:  py -2.7 hyperautomationtest.py -b -j SHOOTINGS_TEST_FOR_KYLE.JSON -e Shootings_Test.hyper
# v0.25 ex:  py -2.7 hyperautomationtest.py -b -d OPEN_DATA_CPD_SHOOTINGS_X -e Shootings_Test.hyper
