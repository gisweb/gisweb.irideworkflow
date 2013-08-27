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
    frm_concessione_1 = 'POR_CONCSTRA_ATTR',
    frm_concessione_2 = 'POR_CONCSTRA_PACCE',
    frm_concessione_3 = 'POR_CONCSTRA_TACCE',
    frm_concessione_4 = 'POR_CONCSTRA_PROVV',
    #frm_occupazione_a = 'POR_CONCSTRA_VOL',
    #frm_occupazione_c = 'POR_CONCSTRA_CPUB'
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
    frm_concessione_1 = dict(
        ATTR_TIPOPERE =   lambda doc: doc.checkItem('concessione_opere') or doc.checkItem('concessione_opere_altro'),
        ATTR_LOCSTRADA =  lambda doc: doc.checkItem('ubicazione_strada_elenco'),
        ATTR_COMUNE =     lambda doc: doc.checkItem('ubicazione_comune'),
        ATTR_LATO =       lambda doc: doc.checkItem('ubicazione_lato'),
        ATTR_PROGRE =     lambda doc: doc.checkItem('ubicazione_prog'),
        ATTR_INIPROGRE =  lambda doc: doc.checkItem('ubicazione_daprog'),
        ATTR_FINEPROGRE = lambda doc: doc.checkItem('ubicazione_aprog'),
        ATTR_FOGLIO =     lambda doc: doc.checkItem('ubicazione_foglio'),
        ATTR_MAPPALE =    lambda doc: doc.checkItem('ubicazione_mappale'),
        ATTR_NOTE =       lambda doc: doc.checkItem('concessione_annotazioni'),
        APROG_WKTGEOM =   lambda doc: doc.checkItem('ubicazione_prog_geometry'),
        DAPROG_WKTGEOM =  lambda doc: doc.checkItem('ubicazione_daprog_geometry'),
        PROG_WKTGEOM =    lambda doc: doc.checkItem('ubicazione_aprog_geometry'),
    ),
    frm_concessione_2 = dict(
        PACCE_TIPO_ABP =   lambda doc: str('ABP' in doc.checkItem('ubicazione_strada_elenco'))[1],
        PACCE_TIPO_RUR =   lambda doc: str('RUR' in doc.checkItem('ubicazione_strada_elenco'))[1],
        PACCE_TIPO_CIA =   lambda doc: str('CIA' in doc.checkItem('ubicazione_strada_elenco'))[1],
        PACCE_TIPO_MURI =  lambda doc: str('MURI' in doc.checkItem('ubicazione_strada_elenco'))[1],
        PACCE_TIPO_REC =   lambda doc: str('REC' in doc.checkItem('ubicazione_strada_elenco'))[1],
        PACCE_TIPO_ALTRO = lambda doc: str('ALTRO' in doc.checkItem('ubicazione_strada_elenco'))[1],
        PACCE_TIPO_NOTE =  lambda doc: doc.checkItem('concessione_opere_altro'),
        PACCE_LOCSTRADA =  lambda doc: doc.checkItem('ubicazione_strada_elenco'),
        PACCE_COMUNE    =  lambda doc: doc.checkItem('ubicazione_comune'),
        PACCE_LATO =       lambda doc: doc.checkItem('ubicazione_lato'),
        PACCE_PROGRE =     lambda doc: doc.checkItem('ubicazione_prog'),
        PACCE_INIPROGRE =  lambda doc: doc.checkItem('ubicazione_daprog'),
        PACCE_FINEPROGRE = lambda doc: doc.checkItem('ubicazione_aprog'),
        PACCE_FOGLIO =     lambda doc: doc.checkItem('ubicazione_foglio'),
        PACCE_MAPPALE =    lambda doc: doc.checkItem('ubicazione_mappale'),
        PACCE_NOTE =       lambda doc: doc.checkItem('concessione_annotazioni'),
        APROG_WKTGEOM =    lambda doc: doc.checkItem('ubicazione_prog_geometry'),
        DAPROG_WKTGEOM =   lambda doc: doc.checkItem('ubicazione_daprog_geometry'),
        PROG_WKTGEOM =     lambda doc: doc.checkItem('ubicazione_aprog_geometry'),

    ),
    frm_concessione_3 = dict(
        TACCE_TIPOPERE =   lambda doc: doc.checkItem('concessione_opere') or doc.checkItem('concessione_opere_altro'),
        TACCE_LOCSTRADA =  lambda doc: doc.checkItem('ubicazione_strada_elenco'),
        TACCE_COMUNE    =  lambda doc: doc.checkItem('ubicazione_comune'),
        TACCE_LATO =       lambda doc: doc.checkItem('ubicazione_lato'),
        TACCE_PROGRE =     lambda doc: doc.checkItem('ubicazione_prog'),
        TACCE_INIPROGRE =  lambda doc: doc.checkItem('ubicazione_daprog'),
        TACCE_FINEPROGRE = lambda doc: doc.checkItem('ubicazione_aprog'),
        TACCE_FOGLIO =     lambda doc: doc.checkItem('ubicazione_foglio'),
        TACCE_MAPPALE =    lambda doc: doc.checkItem('ubicazione_mappale'),
        TACCE_DATAINI =    lambda doc: doc.checkItem('concessione_data_da'),
        TACCE_DATAFINE =   lambda doc: doc.checkItem('concessione_data_a'),
        TACCE_NOTE =       lambda doc: doc.checkItem('concessione_annotazioni'),
        APROG_WKTGEOM =    lambda doc: doc.checkItem('ubicazione_prog_geometry'),
        DAPROG_WKTGEOM =   lambda doc: doc.checkItem('ubicazione_daprog_geometry'),
        PROG_WKTGEOM =     lambda doc: doc.checkItem('ubicazione_aprog_geometry'),
    ),
    frm_concessione_4 = dict(
        PROVV_TIPORIC =   lambda doc: doc.checkItem('concessione_richiesta'),
        PROVV_NUMPROVV =  lambda doc: doc.checkItem('concessione_numero'),
        PROVV_DATAPROVV = lambda doc: doc.checkItem('concessione_data_rilascio'),
        PROVV_DATASCAD =  lambda doc: doc.checkItem('concessione_data_scadenza'),
        PROVV_DTPROROGA = lambda doc: doc.checkItem('concessione_data_proroga'),
        PROVV_NOTE =      lambda doc: doc.checkItem('concessione_annotazioni'),
    ),
    frm_concessione_5 = dict(
        VOL_NUMREPERTORIO =  lambda doc: doc.checkItem('concessione_repertorio_numero'),
        VOL_DATAREPERTORIO = lambda doc: doc.checkItem('concessione_repertorio_data'),
        VOL_INTESTAZIONE =   lambda doc: doc.checkItem('concessione_intestazione_precedente'),
        VOL_MOTIVO =         lambda doc: doc.checkItem('concessione_voltura_motivazione'),
        VOL_COMUNE    =      lambda doc: doc.checkItem('ubicazione_comune'),
        VOL_INDIRIZZO    =   lambda doc: doc.checkItem('ubicazione_indirizzo'),
        VOL_CIVICO    =      lambda doc: doc.checkItem('ubicazione_civico'),
        VOL_CAP    =         lambda doc: doc.checkItem('ubicazione_cap'),
        VOL_FOGLIO =         lambda doc: doc.checkItem('ubicazione_foglio'),
        VOL_MAPPALE =        lambda doc: doc.checkItem('ubicazione_mappale'),
        VOL_MODIFICA =       lambda doc: doc.checkItem('concessione_opt')[1].upper(),
        VOL_NOTEMOD =        lambda doc: doc.checkItem('concessione_modificazioni_altro'),
        #VOL_WKTGEOM
    ),
    frm_concessione_6 = dict(
        #DEP_NUMREPERTORIO
        #DEP_DATAREPERTORIO
        #DEP_INTESTAZIONE
        #DEP_MEZZOBANCA
        #DEP_IBAN
        #DEP_CC
        #DEP_ABI
        #DEP_CAB
    )
    # whatever...
)
        
key = plominoDocument.getForm().getFormName()
assert (key in fieldmaps) and (key in tablenames), 'Layer per la pratica "%s" NON ancora implementato!' % plominoDocument.Title().decode('ascii', errors='replace').encode('ascii', errors='replace')

fieldmap = fieldmaps.get(key) or dict()
out = dict()
for k,fun in fieldmap.items():
    res = fun(plominoDocument)
    if res != None:
        out[k] = res

return {tablenames[key]: (out, )}
    