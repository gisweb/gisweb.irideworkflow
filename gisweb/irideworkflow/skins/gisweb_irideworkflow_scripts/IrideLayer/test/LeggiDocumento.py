## Script (Python) "build_mittente"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=json=True
##title=
##
# Example code:

assert context.isAuthor(), "You need edit permission on this document!"

from gisweb.irideworkflow import leggi_documento
from Products.CMFPlomino.PlominoUtils import json_dumps

docid = context.getItem('irideIdDocumento')

if docid:
    res = leggi_documento(docid)
else:
    res = None

if json:
    print json_dumps(res)
    return printed
else:
    return res