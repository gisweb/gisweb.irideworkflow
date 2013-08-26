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

fixed = dict(
    frm_gara_base = dict(
        TipoDocumento='COMP',
        InCaricoA='COMPSTRANEW',
        #Classifica='002.000.000'
    ),
    frm_concessione_1 = dict(
        TipoDocumento='CONAS',
        InCaricoA='CONCESNEW',
        Classifica='XVIII.02.03.'
    ),
    frm_occupazione_a = dict(
        TipoDocumento = 'CONSC',
        InCaricoA = 'CONCESNEW'
    ),
    # whatever...
)

formname = plominoDocument.getForm().getFormName()
return dict(
    fixed[formname],
    Oggetto = plominoDocument.Title(),
)

#fieldmap = dict(
    #Oggetto =       lambda doc: doc.Title(), #(doc.Title()).decode('ascii', 'replace').encode('ascii', 'replace'),
    #TipoDocumento = lambda doc: fixed[doc.getForm().getFormName()]['TipoDocumento'],
    #InCaricoA =     lambda doc: fixed[doc.getForm().getFormName()]['InCaricoA'],
    ##Classifica =    lambda doc: fixed[doc.getForm().getFormName()]['Classifica'],
#)

#out = dict()
#for k,fun in fieldmap.items():
    #res = fun(plominoDocument)
    #if res != None:
        #out[k] = res
#return out     