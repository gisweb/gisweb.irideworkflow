## Script (Python) "WMAttivaProcedimentoIn"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=protocollo_automatico='SI'
##title=
##
# Example code:

"""
Ricava dal PlominoDocument le informazioni utili per costruire un oggetto
dati_procedimento-like.

    protocollo_automatico (String) SI/NO

Chiavi da restituire:
    codice_fiscale_titolare: identificativo del soggetto intestatario del  procedimento;
    anagrafica_titolare: cognome/nome oppure ragione sociale dell'intestatario del
        procedimento;
    codice_fiscale_richiedente: identificativo del soggetto che attiva il procedimento;
    anagrafica_richiedente: cognome/nome oppure ragione sociale del soggetto che
        attiva il procedimento;
    tipo_procedimento: codifica del procedimento
        (i.e.: "<tipo documento>|<classifica>|<unità operativa di carico>");
    argomento: breve descrizione della domanda (riportare alcuni attributi
        significativi del procedimento);

    dati_procedimento: documento XML contenente tutti gli attributi del procedimento
        amministrativo eventualmente già attivato.
    xml_richiesta: documento XML contenente gli attributi necessari all'attivazione
        del procedimento amministrativo. Tale documento avrà una struttura variabile
        e dipendente dal tipo di procedimento amministrativo.
"""

plominoDocument = context.getParentDocument()

dati_richiesta = plominoDocument.IrideLayer.SubDatiRichiestaIn()

out = dict()
out['codice_fiscale_titolare'] = dati_richiesta['tit_codfisc']
out['anagrafica_titolare'] = (' '.join((dati_richiesta['tit_cognome'], dati_richiesta['tit_nome'], ))).strip()

if plominoDocument.getItem('giuridica_opt', ''):
    out['codice_fiscale_richiedente'] = dati_richiesta['ric_codfisc']
    out['anagrafica_richiedente'] = (' '.join((dati_richiesta['ric_cognome'], dati_richiesta['ric_nome'], ))).strip()


datiProtocolloIn = plominoDocument.IrideLayer.ProtocolloIn()
out['tipo_procedimento'] = '%(TipoDocumento)s|%(Classifica)s|%(InCaricoA)s' % datiProtocolloIn

out['oggetto'] = datiProtocolloIn['Oggetto']

# TODO: restituisce ancora un dizionario VUOTO!!
out['dati_procedimento'] = plominoDocument.IrideLayer.SubDatiProcedimentoIn()

out['dati_richiesta'] = plominoDocument.IrideLayer.SubDatiRichiestaIn(protocolloAutomatico=protocollo_automatico)

return out