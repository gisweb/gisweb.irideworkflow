## Script (Python) "DatiUtenteIn"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Build a DatiUtenteIn-like object
##
# Example code:

"""
Ricava dal PlominoDocument le informazioni utili per costruire un oggetto
DatiUtenteIn-like.
"""

plominoDocument = context.getParentDocument()

tablenames = dict(
    frm_gara_base = 'POR_COMPSTRA',
    frm_occupazione_a = 'POR_CONCSTRA_VOL',
    frm_occupazione_c = 'POR_CONCSTRA_CPUB'
)

fieldmaps = dict(
    frm_gara_base = dict(
        COMP_DENGARA =      lambda doc: doc.checkItem('gara_denominazione'),
        COMP_DATACOMP =     lambda doc: doc.checkItem('gara_data_gara'),
        COMP_LOCALITA =     lambda doc: doc.checkItem('gara_comune_gara'),
        COMP_ORE_RITROVO =  lambda doc: doc.checkItem('gara_ora_ritrovo'),
        COMP_LUO_RITROVO =  lambda doc: doc.checkItem('gara_luogo_ritrovo'),
        COMP_LUO_PARTENZA = lambda doc: doc.checkItem('gara_luogo_partenza'),
        COMP_ORE_PARTENZA = lambda doc: doc.checkItem('gara_ora_partenza'),
        COMP_ORE_ARRIVO =   lambda doc: doc.checkItem('gara_ora_arrivo'),
        COMP_LUO_ARRIVO =   lambda doc: doc.checkItem('gara_luogo_arrivo'),
        COMP_ITINERARIO =   lambda doc: doc.checkItem('gara_itinerario'),
        COMP_DATA_SOPLUO =  lambda doc: doc.checkItem('gara_data_sopraluogo'),
        COMP_NUM_POLIZZA =  lambda doc: doc.checkItem('gara_polizza_num'),
        COMP_DATA_POLIZZA = lambda doc: doc.checkItem('gara_polizza_data'),
        COMP_SOC_ASSICURA = lambda doc: doc.checkItem('gara_polizza_societa'),
        COMP_CATEG =        lambda doc: doc.checkItem('gara_tipo')
    ),
    # whatever...
)
        
key = plominoDocument.getForm().getFormName()
assert (key in fieldmaps) and (key in tablenames), 'Layer per la pratica "%s" NON ancora implementato!' % doc.Title().decode('ascii', errors='replace').encode('ascii', errors='replace')

fieldmap = fieldmaps.get(key) or dict()
out = dict()
for k,fun in fieldmap.items():
    res = fun(plominoDocument)
    if res != None:
        out[k] = res

return {tablenames[key]: (out, )}
    