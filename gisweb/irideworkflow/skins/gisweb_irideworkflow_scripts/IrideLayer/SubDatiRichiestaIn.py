## Script (Python) "SubDatiRichiestaIn"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##
# Example code:

"""

Chiavi da restituire:
    ProcessID            (Stringa) Identificativo del processo proveniente dal portale;
    Oggetto              (Stringa) Oggetto del processo proveniente dal portale;
    Stato                (Stringa) Stato del processo proveniente dal portale;
    protocolloAutomatico (Stringa) Indicatore di protocollazione automatica del
        documento relativo al procedimento. Valori ammessi: Si/No, default = Si;

    int_numeropr (Stringa)  Numero di protocollo del procedimento da integrare;
    int_annopr   (Numerico) Anno di protocollazione del procedimento da integrare;
    int_datapr   (Data)     Data di protocollazione del procedimento da integrare;

    tit_codfisc (Stringa)  Codice fiscale;
    tit_tiposog (Stringa)  Tipo soggetto:persona fisica / giuridica;
    tit_cognome (Stringa)  cognome;
    tit_nome    (Stringa)  nome;
    tit_codluon (Stringa)  Codice luogo di nascita (istat);
    tit_desluon (Stringa)  Descrizione luogo di nascita;
    tit_codpron (Stringa)  Sigla provincia luogo di nascita (o stato estero);
    tit_dtnas   (Data)     Data di nascita;
    tit_sesso   (Stringa)  sesso;
    tit_codcomr (Stringa)  Codice comune di residenza (istat);
    tit_descomr (Stringa)  Descrizione comune di residenza;
    tit_codpror (Stringa)  Sigla provincia luogo di residenza (o stato estero);
    tit_capr    (Stringa)  CAP residenza;
    tit_codres  (Stringa)  Codice residenza;
    tit_desindr (Stringa)  Descrizione indirizzo di residenza;
    tit_numciv  (Numerico) Numero civico;
    tit_desnatg (Stringa)  Descrizione natura giuridica;
    tit_numtel  (Stringa)  Numero telefono;
    tit_codcit  (Stringa)  Codice cittadinanza (istat);
    tit_descit  (Stringa)  Descrizione cittadinanza;
    tit_email   (Stringa)  indirizzo email;
    tit_pec     (Stringa)  indirizzo email posta certificata;
    tit_cell    (Stringa)  telefono cellulare;

    ric_codfisc (Stringa)  Codice fiscale
    ric_tiposog (Stringa)  Tipo soggetto:persona fisica / giuridica
    ric_cognome (Stringa)  cognome
    ric_nome    (Stringa)  nome
    ric_codluon (Stringa)  Codice luogo di nascita (istat)
    ric_desluon (Stringa)  Descrizione luogo di nascita
    ric_codpron (Stringa)  Sigla provincia luogo di nascita (o descrizione stato estero)
    ric_dtnas   (Data)     Data di nascita
    ric_sesso   (Stringa)  sesso
    ric_codcomr (Stringa)  Codice comune di residenza (istat)
    ric_descomr (Stringa)  Descrizione comune di residenza
    ric_codpror (Stringa)  Sigla provincia luogo di residenza (o descrizione stato estero)
    ric_capr    (Stringa)  CAP residenza
    ric_codres  (Stringa)  Codice residenza
    ric_desindr (Stringa)  Descrizione indirizzo di residenza
    ric_numciv  (Numerico) Numero civico
    ric_desnatg (Stringa)  Descrizione natura giuridica
    ric_numtel  (Stringa)  Numero telefono
    ric_codcit  (Stringa)  Codice cittadinanza (istat)
    ric_descit  (Stringa)  Descrizione cittadinanza
    ric_email   (Stringa)  indirizzo email
    ric_pec     (Stringa)  indirizzo email posta certificata
    ric_cell    (Stringa)  telefono cellulare

    all_blob     (BinBase64) Documento binario
    all_descri   (Stringa)   Descrizione documento
    all_tipo     (Stringa)   Tipo documento (word, pdf, rtf, p7m, …)
    all_nomefile (Stringa)   Nome file
    all_firma    (Stringa)   Documento firmato digitalmente: S/N
"""

plominoDocument = context.getParentDocument()

out = dict()

out['ProcessID'] = plominoDocument.getId()
out['Oggetto'] = plominoDocument.Title()
out['Stato'] = ''
out['protocolloAutomatico'] = 'Si'

if plominoDocument.getItem('giuridica_opt', ''):
    out.update(plominoDocument.IrideLayer.compilagiuridica())
    out.update(plominoDocument.IrideLayer.compilafisica(tit=False))
else:
    out.update(plominoDocument.IrideLayer.compilafisica())

items = plominoDocument.getItems()
fields = plominoDocument.getForm().getFormFields(includesubforms=True)
out['dati_allegati'] = list()
for fld in fields:
    fldname = fld.getId()
    if (fldname in items) and (fld.getFieldType() == 'ATTACHMENT'):
        value = plominoDocument.getItem(fldname, {}) or {}
        for fname,ftype in value.items():
            out['dati_allegati'].append(
                dict(
                    all_descri = '',
                    all_tipo = ftype.split('/')[1],
                    all_nomefile = fname,
                    all_blob = plominoDocument.getfile(filename=fname),
                    all_firma = 'N'
                )
            )

return out