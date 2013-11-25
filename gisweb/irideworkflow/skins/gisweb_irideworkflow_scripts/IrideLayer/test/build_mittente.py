## Script (Python) "build_mittente"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##
# Example code:

from gisweb.irideworkflow import test_build_mittente

mitt = context.MittentiDestinatariIn(index=1)

context.REQUEST.RESPONSE.setHeader("Content-type", "text/xml")
print test_build_mittente(mitt, **context.Iride_loadPortalSettings())
return printed