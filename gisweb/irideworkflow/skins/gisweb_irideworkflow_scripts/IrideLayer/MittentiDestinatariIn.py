## Script (Python) "MittentiDestinatariIn"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=index=0
##title=Build a MittenteDestinatarioIn-like object
##
# Example code:

"""
Ricava dal PlominoDocument le informazioni utili per costruire un oggetto
MittenteDestinatarioIn-like.
"""

plominoDocument = context.getParentDocument()

MittentiDestinatari = []

def get_recapiti(formname, doc):
    form = doc.getParentDatabase().getForm(formname)
    return [dict(
        TipoRecapito = field.getId().split('_')[1].upper(),
        ValoreRecapito = doc.getItem(field.getId(), '') or ''
    ) for field in form.getFormFields()]


PersonaFisica = dict(
    CodiceFiscale = lambda doc: doc.checkItem('fisica_cf'),
    CognomeNome = lambda doc: '%s %s' % (doc.checkItem('fisica_cognome'), doc.checkItem('fisica_nome'), ),
    Nome = lambda doc: doc.checkItem('fisica_nome'),
    Localita = lambda doc: doc.checkItem('fisica_loc_nato'),
    Indirizzo = lambda doc: '%s, %s' % (doc.checkItem('fisica_indirizzo'), doc.checkItem('fisica_civico'), ),
    CodiceComuneResidenza = lambda doc: doc.checkItem('fisica_cod_cat'),
    DataNascita = lambda doc: doc.checkItem('fisica_data_nato'),
    CodiceComuneNascita = lambda doc: doc.checkItem('fisica_cod_cat_nato'),
    Nazionalita = lambda doc: 'IT' if doc.getItem('fisica_cod_cat_nato') != 'EE' else doc.getItem('fisica_comune_nato'),
    TipoSogg = lambda doc: 'S',
    TipoPersona = lambda doc: 'FI',
    Recapiti = lambda doc: get_recapiti('sub_fisica_recapiti', doc)
)

PersonaGiuridica = dict(
    CodiceFiscale = lambda doc: doc.checkItem('giuridica_cf'),
    CognomeNome = lambda doc: doc.checkItem('giuridica_denominazione'),
    Localita = lambda doc: doc.checkItem('giuridica_localita'),
    Indirizzo = lambda doc: '%s, %s' % (doc.checkItem('giuridica_indirizzo'), doc.checkItem('giuridica_civico'), ),
    CodiceComuneResidenza = lambda doc: doc.checkItem('giuridica_cod_cat'),
    # questi campi direi che non hanno un corrispettivo riferito alla persona giuridica
    # DataNascita = lambda doc: doc.checkItem('fisica_data_nato')
    # CodiceComuneNascita = lambda doc: doc.checkItem('fisica_cod_cat_nato')
    Nazionalita = lambda doc: 'IT' if doc.getItem('giuridica_cod_cat') != 'EE' else doc.getItem('giuridica_comune'),
    TipoSogg = lambda doc: 'I',
    TipoPersona = lambda doc: 'GI',
    Recapiti = lambda doc: get_recapiti('sub_giuridica_recapiti', doc)
)

cointestatario = dict(
    CodiceFiscale = lambda doc: doc.checkItem('fisica_cf_cointestatari'),
    CognomeNome = lambda doc: '%s %s' % (doc.checkItem('fisica_cognome_cointestatari'), doc.checkItem('fisica_nome_cointestatari'), ),
    Indirizzo = lambda doc: '%s, %s' % (doc.checkItem('fisica_indirizzo_cointestatari'), doc.checkItem('fisica_civico_cointestatari'), ),
    CodiceComuneResidenza = lambda doc: doc.checkItem('fisica_cod_cat_cointestatari'),
    DataNascita = lambda doc: doc.checkItem('fisica_data_nato_cointestatari'),
    CodiceComuneNascita = lambda doc: doc.checkItem('fisica_cod_cat_nato_cointestatari'),
    Nazionalita = lambda doc: 'IT' if doc.getItem('fisica_cod_cat_nato_cointestatari') != 'EE' else doc.getItem('fisica_comune_nato_cointestatari'),
    TipoSogg = lambda doc: 'S',
    TipoPersona = lambda doc: 'FI',
    Recapiti = lambda doc: get_recapiti('sub_fisica_cointestatari', doc)
)

def get_cointestatario(rec):
    form = plominoDocument.getForm()
    fld = form.getFormField('elenco_cointestatari')
    gridfields = fld.getSettings().field_mapping.split(',')
    nfo = dict(zip(gridfields, rec))

    cointestatario = dict(
        CodiceFiscale = lambda doc: doc['fisica_cf_cointestatari'],
        CognomeNome = lambda doc: '%s %s' % (doc['fisica_cognome'], doc['fisica_nome'], ),
        Indirizzo = lambda doc: '%s, %s' % (doc['fisica_indirizzo'], doc['fisica_civico'], ),
        CodiceComuneResidenza = lambda doc: doc['fisica_cod_cat'],
        DataNascita = lambda doc: doc['fisica_data_nato'],
        CodiceComuneNascita = lambda doc: doc['fisica_cod_cat_nato'],
        Nazionalita = lambda doc: 'IT' if doc['fisica_cod_cat_nato'] != 'EE' else doc['fisica_comune_nato'],
        TipoSogg = lambda doc: 'S',
        TipoPersona = lambda doc: 'FI',
    )

    return dict([(k,f(nfo)) for k,f in cointestatario.items()])

for el in (PersonaFisica, PersonaGiuridica, ):
    MittentiDestinatari.append(dict([(k,f(plominoDocument)) for k,f in el.items()]))

#if 'sub_fisica_cointestatari' in plominoDocument.getForm().getSubforms():
    #MittentiDestinatari.append(dict([(k,f(plominoDocument)) for k,f in cointestatario.items()]))

if plominoDocument.hasItem('elenco_altri_cointestatari'):
    cointestatari = plominoDocument.getItem('elenco_cointestatari', []) or []
    MittentiDestinatari += [get_cointestatario(rec) for rec in cointestatari]

if index:
    idx = int(index)-1
    return MittentiDestinatari[idx]
return MittentiDestinatari
