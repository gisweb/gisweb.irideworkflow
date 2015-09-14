## Script (Python) "Iride_testConnection"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Tool for testing conection to Iride workflow service
##
# Example code:

from gisweb.irideworkflow import test_di_connessione

return test_di_connessione(**context.Iride_loadPortalSettings())