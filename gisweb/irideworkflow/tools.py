# -*- coding: utf-8 -*-

from iride.interface import IrideProtocollo, IrideProcedimento, IridePratiche
from iride.interface import doc2xml, prepare_string2

def test_di_connessione(**kw):
    """ Verifica lo stato della connessione. """

    out = dict(success=0)
    try:
        conn = IrideProtocollo(testinfo=True, **kw)
    except Exception as err:
        out['message'] = '%s' % err
    else:
        out = IrideProtocollo(testinfo=True, **kw).check()

    return out

def leggi_documento(docid, **kw):
    """
    Returns the data of a document starting from their iride identifier (IdDocumento).

    Args:
        docid (int): the document identifier.
    """
    conn = IrideProtocollo(**kw)
    return conn.LeggiDocumento(docid)

def inserisci_protocollo(MittentiIn, AllegatiIn, UtenteIn, ProtocolloIn, testinfo=False, **ccp):
    """

    TODO:
    * supporto per mittenti multipli (MittentiDestinatariIn)
    """
    conn = IrideProtocollo(testinfo=testinfo, **ccp)

    res_protocollo = conn.InserisciProtocollo(
        mittenti = MittentiIn,
        allegati = AllegatiIn,
        **ProtocolloIn
    )

    res_utente = None
    if res_protocollo['success']:
        if not res_protocollo['result'].get('Errore'):
            docid = res_protocollo['result']['IdDocumento']
            res_utente = conn.InserisciDatiUtente(docid, UtenteIn)

    return (res_protocollo, res_utente, )

#def inserisci_documento(doc, testinfo=False, **ccp):
    # TODO
    #conn = IrideProtocollo(testinfo=testinfo, **ccp)

    #layer = doc.getParentDatabase().resources.irideLayer
    #dati = layer('ProtocolloIn', doc)
    #dati_mittente = layer('MittenteDestinatarioIn', doc)
    #dati_allegato = layer('AllegatoIn', doc)

    #return conn.InserisciDocumentoEAnagrafiche(mittenti=[dati_mittente], allegati=[dati_allegato], **dati)


def lista_procedimenti(testinfo=False, ccp={}, **kw):
    """
    Estrazione dei procedimenti / Extraction of the proceedings of a subject.

    ccp            (dict): Custom connection parameters

    Argomenti possibili:
    CodiceFiscale   (str): codice fiscale dell'utente;
    SessionID       (str): -- NON UTILIZZATO --- ;
    DataInizio (DateTime): Se valorizzata, estrae i procedimenti con data di
                            protocollo a partire dalla data indicata (gg/mm/aaaa);
    DataFine   (DateTime): Se valorizzata, estrae i procedimenti con data di
                            protocollo  fino alla data indicata (gg/mm/aaaa);
    Stato           (str): Valori possibili:
                            "In corso": estrae i procedimenti attivi,
                            "Terminati": estrare i procedimenti terminati,
                            "Tutti": estrae sia i procedimenti attivi sia quelli terminati.
    """
    conn = IrideProcedimento(testinfo=testinfo, **ccp)
    return conn.ListaProcedimenti(**kw)

def leggi_procedimento(IDProcedimento, testinfo=False, ccp={}, **kw):
    """
    Extracts detail data of proceedings

    ccp               (dict): Custom connection parameters

    Args:
        IDProcedimento (int): proceeding Iride idetifier
    """
    conn = IrideProcedimento(testinfo=testinfo, **ccp)
    return conn.DettaglioProcedimento(IDProcedimento, **kw)

#def inserisci_procedimento(doc, testinfo=False, **ccp):
    #""" """
    # TODO

    #conn = IrideProcedimento(testinfo=testinfo, **ccp)

    #layer = doc.getParentDatabase().resources.irideLayer
    #dati_procedimento = layer('ProtocolloIn', doc)
    #dati_mittente = layer('MittenteDestinatarioIn', doc)
    #dati_allegato = layer('AllegatoIn', doc)

    #return conn.AttivaProcedimento(mittenti=[dati_mittente], allegati=[dati_allegato], **dati_procedimento)

def procedimento_pratica(cf, docid, testinfo=False, **ccp):
    """
    Shortcut per ricavare le informazioni del procedimento direttamente a partire
    da una pratica.
    """

    conn = IrideProcedimento(testinfo=True, **ccp)

    # 1. si ricava la lista dei procedimenti in capo al mittente attraverso il CF
    res_procedimenti = conn.ListaProcedimenti(CodiceFiscale=cf)

    if res_procedimenti['success']:
        if not res_procedimenti['result'].get('Errore'):
            # 2. si filtra i procedimenti trovati in base al parametro IdDocumento
            flt_res = [rec['TestataProcedimento'] \
                for rec in res_procedimenti['result']['Procedimenti']['Procedimento'] \
                    if rec['EstremiDocumento']['IdDocumento']==docid] or [{}]
            #if not flt_res:
                    #flt_res = [{}]
            #if testinfo:
                #flt_res[0]['time_elapsed'] = res_procedimenti['time_elapsed']
            res_procedimenti['result'] = flt_res[0]
            return res_procedimenti
        else:
            return res_procedimenti
    else:
        return res_procedimenti

def wm_attiva_procedimento(kw, testinfo=False, **ccp):
    """ """
    conn = IridePratiche(testinfo=testinfo, **ccp)
    res = conn.wm_attiva_procedimento(**kw)
    return res

def InserisciDatiUtente(docid, UtenteIn, testinfo=False, **ccp):
    """ """
    conn = IrideProtocollo(testinfo=testinfo, **ccp)
    return conn.InserisciDatiUtente(docid, UtenteIn)

def ModificaSoloAnagrafiche(IdDocumento, MittentiDestinatari, testinfo=False, **ccp):
    """ Usa il servizio ModificaDocumentoEAnagrafiche per inserire le anagrafiche
    in uno a molti (i.e. eventuali cointestatari)
    """
    conn = IrideProtocollo(testinfo=testinfo, **ccp)
    return conn.ModificaDocumentoEAnagrafiche(IdDocumento=IdDocumento, MittentiDestinatari=MittentiDestinatari)

################################################################# TEST FUNCTIONS #

def test_build_mittente(mitt, **ccp):
    conn = IrideProtocollo(testinfo=True, **ccp)
    return conn.build_mittente(**mitt)

def test_prepare_string(data, docid):
    return doc2xml(prepare_string2(data, docid), pprint=True)

def test_build_xml(name, kw={}, **ccp):
    conn = IridePratiche(testinfo=True, **ccp)
    return conn.build_xml(name, **kw)