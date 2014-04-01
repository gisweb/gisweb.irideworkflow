## Script (Python) "Iride_loadPortalSettings"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Load settings from portal_properties tool
##
# Example code:

from Products.CMFCore.utils import getToolByName

# così posso prendere alcuni attributi di default dalle
# portal_properties del portale
# (es. HOST è una impostazione propria del portale)
pp = getToolByName(context,'portal_properties')

if 'Iride' in pp.keys():
    out = dict([(k,v) for k,v in pp['Iride'].propertyItems() if k!='title'])
else:
    out = dict()

updatenfo = dict([(k,v) for k,v in context.getParentDatabase().propertyItems()
    if k.startswith('Iride_')])

if len(updatenfo)>0:
    out.update(updatenfo)

return out