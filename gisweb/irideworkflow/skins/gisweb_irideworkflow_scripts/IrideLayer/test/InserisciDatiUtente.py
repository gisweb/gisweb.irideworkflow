## Script (Python) "InserisciDatiUtente"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##
# Example code:

from gisweb.irideworkflow import InserisciDatiUtente

UtenteIn = context.IrideLayer.DatiUtenteIn()
docid = context.getItem('irideIdDocumento')
res = InserisciDatiUtente(docid, UtenteIn, testinfo=True, **context.Iride_loadPortalSettings())



print res
return printed