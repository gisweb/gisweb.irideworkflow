## Script (Python) "compilafisica"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=tit=True
##title=
##
# Example code:

"""
da fisica a soggetto (tit o ric)
"""

from gisweb.irideworkflow import getCodcom

plominoDocument = context.getParentDocument()

prefix = 'tit' if tit else 'ric'

return {
    # (Stringa)  Codice fiscale;
    '%s_codfisc' % prefix: plominoDocument.checkItem('fisica_cf', format=None),
    # (Stringa)  Tipo soggetto:persona fisica / giuridica;
    '%s_tiposog' % prefix: 'FI',
    '%s_cognome' % prefix: plominoDocument.checkItem('fisica_cognome', format=None),
    '%s_nome' % prefix: plominoDocument.checkItem('fisica_nome', format=None),
    # (Stringa)  Codice luogo di nascita (istat);
    '%s_codluon' % prefix: getCodcom(plominoDocument.checkItem('fisica_cod_cat_nato', format=None)),
    # (Stringa)  Descrizione luogo di nascita;
    '%s_desluon' % prefix: plominoDocument.checkItem('fisica_loc_nato', format=None),
    # (Stringa)  Sigla provincia luogo di nascita (o stato estero);
    '%s_codpron' % prefix: plominoDocument.checkItem('fisica_provincia_nato', format=None),
    # (Stringa)  Data di nascita;
    '%s_dtnas' % prefix: plominoDocument.checkItem('fisica_data_nato', format=None),
    # (Stringa)  sesso;
    '%s_sesso' % prefix: plominoDocument.checkItem('fisica_sesso', format=None),
    # (Stringa)  Codice comune di residenza (istat); TODO
    '%s_codcomr' % prefix: getCodcom(plominoDocument.checkItem('fisica_cod_cat', format=None)),
    # (Stringa)  Descrizione comune di residenza;
    '%s_descomr' % prefix: plominoDocument.checkItem('fisica_comune', format=None),
    # (Stringa)  Sigla provincia luogo di residenza (o stato estero);
    '%s_codpror' % prefix: plominoDocument.checkItem('fisica_provincia', format=None),
    # (Stringa)  CAP residenza;
    '%s_capr' % prefix: plominoDocument.checkItem('fisica_cap', format=str),
    # (Stringa)  Codice residenza;
    '%s_codres' % prefix: '', # ??? TODO
    # (Stringa)  Descrizione indirizzo di residenza;
    '%s_desindr' % prefix: '%s, %s' % (plominoDocument.checkItem('fisica_indirizzo', format=None), plominoDocument.checkItem('fisica_civico', format=None), ),
    # (Numerico) Numero civico; # WARNING: civico non è detto che sia numerico
    '%s_numciv' % prefix: '', #plominoDocument.checkItem('fisica_civico', format=None),
    # (Stringa)  Descrizione natura giuridica;
    '%s_desnatg' % prefix: '',
    # (Stringa)  Numero telefono;
    '%s_numtel' % prefix: plominoDocument.checkItem('fisica_telefono', format=None),
    # (Stringa)  Codice cittadinanza (istat);
    '%s_codcit' % prefix: '', # ??? TODO
    # (Stringa)  Descrizione cittadinanza;
    '%s_descit' % prefix: plominoDocument.checkItem('fisica_cittadinanza', format=None),
    # (Stringa)  indirizzo email;
    '%s_email' % prefix: plominoDocument.checkItem('fisica_email', format=None),
    # (Stringa)  indirizzo email posta certificata;
    '%s_pec' % prefix: plominoDocument.checkItem('fisica_pec', format=None),
    # (Stringa)  telefono cellulare;
    '%s_cell' % prefix: plominoDocument.checkItem('fisica_cellulare', format=None),
}
