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
    '%s_codfisc' % prefix: ('%s' % plominoDocument.checkItem('giuridica_piva', format=None)) or plominoDocument.checkItem('giuridica_piva', format=None),
    # (Stringa)  Tipo soggetto:persona fisica / giuridica;
    '%s_tiposog' % prefix: 'GI',
    '%s_cognome' % prefix: plominoDocument.checkItem('giuridica_denominazione', format=None),
    '%s_nome' % prefix: '',
    # (Stringa)  Codice luogo di nascita (istat);
    '%s_codluon' % prefix: '',
    # (Stringa)  Descrizione luogo di nascita;
    '%s_desluon' % prefix: '',
    # (Stringa)  Sigla provincia luogo di nascita (o stato estero);
    '%s_codpron' % prefix: '',
    # (Stringa)  Data di nascita;
    '%s_dtnas' % prefix: '',
    # (Stringa)  sesso;
    '%s_sesso' % prefix: '',
    # (Stringa)  Codice comune di residenza (istat);
    '%s_codcomr' % prefix: getCodcom(plominoDocument.checkItem('giuridica_cod_cat', format=None)),
    # (Stringa)  Descrizione comune di residenza;
    '%s_descomr' % prefix: plominoDocument.checkItem('giuridica_comune', format=None),
    # (Stringa)  Sigla provincia luogo di residenza (o stato estero);
    '%s_codpror' % prefix: plominoDocument.checkItem('giuridica_provincia', format=None),
    # (Stringa)  CAP residenza;
    '%s_capr' % prefix: plominoDocument.checkItem('giuridica_cap', format=str),
    # (Stringa)  Codice residenza;
    '%s_codres' % prefix: '',
    # (Stringa)  Descrizione indirizzo di residenza;
    '%s_desindr' % prefix: '%s, %s' % (plominoDocument.checkItem('giuridica_indirizzo', format=None), plominoDocument.checkItem('giuridica_civico', format=None), ),
    # (Numerico) Numero civico; # WARNING: civico non è detto che sia numerico
    '%s_numciv' % prefix: '', #plominoDocument.checkItem('giuridica_civico', format=None),
    # (Stringa)  Descrizione natura giuridica;
    '%s_desnatg' % prefix: plominoDocument.checkItem('giuridica_qualita'),
    # (Stringa)  Numero telefono;
    '%s_numtel' % prefix: plominoDocument.checkItem('giuridica_telefono', format=None),
    # (Stringa)  Codice cittadinanza (istat);
    '%s_codcit' % prefix: '',
    # (Stringa)  Descrizione cittadinanza;
    '%s_descit' % prefix: '',
    # (Stringa)  indirizzo email;
    '%s_email' % prefix: plominoDocument.checkItem('giuridica_email', format=None),
    # (Stringa)  indirizzo email posta certificata;
    '%s_pec' % prefix: plominoDocument.checkItem('giuridica_pec', format=None),
    # (Stringa)  telefono cellulare;
    '%s_cell' % prefix: plominoDocument.checkItem('giuridica_cellulare', format=None),
}
