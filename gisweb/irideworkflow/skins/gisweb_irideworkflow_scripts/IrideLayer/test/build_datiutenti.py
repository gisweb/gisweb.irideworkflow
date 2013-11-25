## Script (Python) "build_datiutenti"
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
from gisweb.irideworkflow import test_build_mittente, test_prepare_string

datiUtente = context.IrideLayer.DatiUtenteIn()

context.REQUEST.RESPONSE.setHeader("Content-type", "text/xml")
print test_prepare_string(datiUtente, PlominoDocument.getId())
return printed