## Script (Python) "ProtocolloIn"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Build a ProtocolloIn-like object
##
# Example code:

"""
Ricava dal PlominoDocument le informazioni utili per costruire un oggetto
ProtocolloIn-like.
"""

plominoDocument = context.getParentDocument()
conf_name = '%s.txt' % plominoDocument.getForm().getFormName()

msg = 'Layer per la pratica "%s" NON ancora implementato!' % plominoDocument.Title().decode(
    'ascii', errors='replace').encode('ascii', errors='replace')
assert (conf_name in context.config.keys()), msg

from gisweb.irideworkflow import conf2dict

conf = conf2dict(str(getattr(script.config, conf_name)))
defaults = conf2dict(str(getattr(script.config, 'defaults.txt')))['CONFIG']

return dict(
    defaults,
    Oggetto = plominoDocument.Title(),
    **dict([(k,v) for k,v in conf['CONFIG'].items() if k not in conf])
)