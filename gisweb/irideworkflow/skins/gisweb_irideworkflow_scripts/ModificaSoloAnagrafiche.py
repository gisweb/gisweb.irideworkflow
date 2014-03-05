## Script (Python) "ModificaSoloAnagrafiche"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=testinfo=False, json=False
##title=
##
# Example code:

docid = context.getItem('irideIdDocumento')
assert docid, 'Nessun ID trovato NON posso procedere'
#assert not test, ''

from gisweb.irideworkflow import ModificaSoloAnagrafiche
from gisweb.utils import json_dumps

MittentiDestinatariIn = context.IrideLayer.MittentiDestinatariIn()
res = ModificaSoloAnagrafiche(docid, MittentiDestinatariIn, testinfo=True, **context.Iride_loadPortalSettings())

if json:
    context.REQUEST.RESPONSE.setHeader("Content-type", "application/json")
    print json_dumps(res, prettyxml=True)
    return printed
else:
    return res