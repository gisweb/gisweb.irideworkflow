## Script (Python) "MittenteDestinatarioIn"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Build a MittenteDestinatarioIn-like object
##
# Example code:

"""
Ricava dal PlominoDocument le informazioni utili per costruire un oggetto
MittenteDestinatarioIn-like.
"""

plominoDocument = context.getParentDocument()

fieldmap = dict(
    CodiceFiscale =       lambda doc: doc.checkItem('fisica_cf'),
    CognomeNome =         lambda doc: "%s %s" % (doc.checkItem('fisica_cognome'), doc.checkItem('fisica_nome')),
    Nome =                lambda doc: doc.checkItem('fisica_nome'),
    Indirizzo =           lambda doc: doc.checkItem('fisica_indirizzo'),
    Localita =            lambda doc: doc.checkItem('fisica_loc'),
    DataNascita =         lambda doc: doc.checkItem('fisica_data_nato', dateformat='%d/%m/%Y'),
    Nazionalita =         lambda doc: doc.checkItem('fisica_cittadinanza'),
    CodiceComuneNascita = lambda doc: doc.checkItem('fisica_cod_cat_nato'),
    # CodiceComuneResidenza = lambda doc: doc.checkItem('fisica_cod_cat'),
    ############### I have NO IDEA about how to set those: ############################
    # DataInvio_DataProt
    # Spese_NProt
    # Mezzo
    # DataRicevimento
    # TipoSogg
    # TipoPersona
    # Recapiti
)

out = dict()
for k,fun in fieldmap.items():
    res = fun(plominoDocument)
    if res != None:
        out[k] = res
return out    