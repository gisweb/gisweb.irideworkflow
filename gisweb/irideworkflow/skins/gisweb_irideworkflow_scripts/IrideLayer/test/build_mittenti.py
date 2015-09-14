## Script (Python) "build_mittenti"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##
# Example code:

PlominoDocument = context.getParentDocument()
from gisweb.utils import json_dumps
from gisweb.irideworkflow import test_build_mittente

#print  json_dumps(PlominoDocument.IrideLayer.MittentiDestinatariIn())
context.REQUEST.RESPONSE.setHeader("Content-type", "text/xml")
for mitt in PlominoDocument.IrideLayer.MittentiDestinatariIn():
    print test_build_mittente(mitt, **context.Iride_loadPortalSettings())

return printed