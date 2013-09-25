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

out = []

for fld in plominoDocument.getForm().getFormFields(includesubforms=True):
    if fld.getFieldType() == 'ATTACHMENT':
        value = plominoDocument.getItem(fld.getId(), {}) or {}
        for filename,mimetype in value.items():
            AllegatoIn = dict(
                TipoFile = filename.split('.')[-1],
                ContentType = mimetype,
                Image = plominoDocument.get(filename)
            )
            out.append(AllegatoIn)

return out