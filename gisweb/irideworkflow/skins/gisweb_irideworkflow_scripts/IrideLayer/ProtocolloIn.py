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

# Example code:

"""
Ricava dal PlominoDocument le informazioni utili per costruire un oggetto
ProtocolloIn-like.
"""

from gisweb.irideworkflow import conf2dict

plominoDocument = context.getParentDocument()
conf_name = '%s.txt' % plominoDocument.getForm().getFormName()
resources = plominoDocument.getParentDatabase().resources

msg = 'Layer per la pratica "%s" NON ancora implementato!' % plominoDocument.Title().decode(
    'ascii', errors='replace').encode('ascii', errors='replace')

if 'IrideLayer' in resources.keys() and conf_name in resources.IrideLayer.keys():
    conf = conf2dict(str(getattr(resources.IrideLayer, conf_name)))
elif conf_name in script.config.keys():
    conf = conf2dict(str(getattr(script.config, conf_name)))
else:
    assert False, msg

defaults = conf2dict(str(getattr(script.config, 'defaults.txt')))['CONFIG']

return dict(
    defaults, # valori le cui chiavi sono presenti anche in conf saranno sovrascritti
    Oggetto = plominoDocument.Title(),
    **dict([(k,v) for k,v in conf['CONFIG'].items() if k not in conf])
)
