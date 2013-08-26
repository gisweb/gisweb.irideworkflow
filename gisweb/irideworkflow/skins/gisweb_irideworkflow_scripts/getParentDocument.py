## Script (Python) "getParentDocument"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Get the nearest PlominoDocument in the acquisition chain.
##
# Example code: context.getParentDocument()

"""
As the PlominoDatabase method getParentDocument it is normally used via
acquisition by scripts.
"""

obj = context
while getattr(obj, 'meta_type', '') != 'PlominoDocument':
    obj = obj.aq_parent
return obj