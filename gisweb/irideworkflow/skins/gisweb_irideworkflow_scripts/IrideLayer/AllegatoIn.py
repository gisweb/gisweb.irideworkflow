## Script (Python) "AllegatoIn"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Build a AllegatoIn-like object
##
# Example code:

"""
Ricava dal PlominoDocument le informazioni utili per costruire un oggetto
AllegatoIn-like.
"""

plominoDocument = context.getParentDocument()

fieldmap = dict(
    TipoFile = lambda doc: 'pdf',
    ContentType = lambda doc: doc.checkItem('documenti_pdf', dict()).get('domanda_inviata.pdf'),
    Image = lambda doc: doc.get('domanda_inviata.pdf')
)

out = dict()
for k,fun in fieldmap.items():
    res = fun(plominoDocument)
    if res != None:
        out[k] = res
return out
    