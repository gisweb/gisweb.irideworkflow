# -*- coding: utf-8 -*-

from suds.client import Client
from datetime import datetime, date
from base64 import b64encode

from lxml import etree

from DateTime import DateTime

from gisweb.utils import XmlDictConfig

# this url is good if you
# ssh siti.provincia.sp.it -L 3340:10.94.128.230:80 -p 2211 (or 2222)
#URL = 'http://127.0.0.1:3340/ulissetest/iride/web_services_20/WSProtocolloDM/WSProtocolloDM.asmx?WSDL'
# This one is good at Spezia
#URL = 'http://10.94.128.230/ulissetest/iride/web_services_20/WSProtocolloDM/WSProtocolloDM.asmx?WSDL'

UTENTE = 'AMMINISTRATORE'
RUOLO = 'AMMINISTRATORE'
APPARTENENZA = 'DOCUMENTO'

def get_current_datetime_as_string():
    return datetime.now().isoformat()

def prepare_string(data, docid):
    """ """
    result = ["<DatiUtenteIn>"]
    for tablename, rows in data.items():
        result.append('<table name="%s">' % tablename)
        for i, row_original in enumerate(rows):
            row = dict(row_original,
                #IRIDE_DOCID=docid,
                #IRIDE_PROGR=i,
                #IRIDE_FONTE='GW',
                #IRIDE_DATINS=get_current_datetime_as_string(),
            )
            result.append('<row>')
            for keyvalue in row.items():
                result.append('<field name="%s">%s</field>' % keyvalue)
            result.append('</row>')
        result.append('</table>')
    result.append("</DatiUtenteIn>")
    return ''.join(result)

def prepare_string2(data, docid):
    root = etree.Element('DatiUtenteIn')
    doc = etree.ElementTree(root)
    for tablename, rows in data.items():
        locals()[tablename] = etree.SubElement(root, 'table', name=tablename)
        for i, row in enumerate(rows):
            # a quanto pare NON servono più
            #row.update(
                #dict(
                    #IRIDE_DOCID = docid,
                    #IRIDE_PROGR = i,
                    #IRIDE_FONTE = 'GW',
                    #IRIDE_DATINS = get_current_datetime_as_string(),
                #)
            #)
            locals()['row_%s' % i] = etree.SubElement(locals()[tablename], 'row')
            for key,value in row.items():
                locals()['%s_%s' % (key, i)] = etree.SubElement(locals()['row_%s' % i], 'field', name=key)
                locals()['%s_%s' % (key, i)].text = u"%s" % value
    return doc
                
                
    
def assign_value(obj, value, validator, transform):
    if value in ('', None, ):
        obj.text = ''
    else:
        assert validator(value), 'Errore di validazione del dato (%s: %s)' % (obj, value, )
        obj.text = transform(value)

xsi = '{http://www.w3.org/2001/XMLSchema-instance}noNamespaceSchemaLocation'

def doc2xml(root, pprint=False):
    return etree.tostring(root, pretty_print=pprint)

def prepare_xml_richiesta(dati_allegati=[], **kw):
    """
    doc url: http://projects.gisweb.it/projects/gisweb-irideworkflow/wiki/Wiki#Descrizione-degli-argomenti-wap
    
    Le chiavi per i vari sub-nodi sono uniche quindi ho previsto possano anche essere
    passate direttamente come parametri di richiesta. In alternativa possono essere
    passati 3/4 dizionari distinti (dati_richiedente, dati_titolare,
    dati_integrazione (opzionale) e dati_allegati) contenenti ognuno la valorizzazione
    dei rispettivi parametri.

    Per dettagli vedere xml_templates
    """

    root_attributes = {xsi: "C:\Documents and Settings\VitDe\Desktop\pratiche\wm_attiva_procedimento.xsd"}
    root = etree.Element('wm_attiva_procedimento', encoding='ISO-8859-1', **root_attributes)
    doc = etree.ElementTree(root)

    dati_procedimento = etree.SubElement(root, 'dati_procedimento')

    from xml_templates import titolare, richiedente, allegati

    # almeno il titolare della richiesta è obbligatorio
    dati_titolare = etree.SubElement(dati_procedimento, 'dati_titolare')
    test = dict()
    for el,v in titolare.items():
        locals()[el] = etree.SubElement(dati_titolare, el)
        if 'dati_titolare' in kw and el in kw['dati_titolare']:
            assign_value(locals()[el], kw['dati_titolare'][el], *v)
        elif el in kw:
            assign_value(locals()[el], kw[el], *v)
            test[el] = kw[el]

    if 'dati_richiedente' in kw or any([i.startswith('ric_') for i in kw]):
        # se non viene fornita informazione riguardante il richiedente evito
        dati_richiedente = etree.SubElement(dati_procedimento, 'dati_richiedente')
        for el,v in richiedente.items():
            locals()[el] = etree.SubElement(dati_richiedente, el)
            if 'dati_richiedente' in kw and el in kw['dati_richiedente']:
                assign_value(locals()[el], kw['dati_richiedente'][el], *v)
            elif el in kw:
                assign_value(locals()[el], kw[el], *v)

    inc = 0
    for allnfo in dati_allegati:
        locals()['dati_allegati_%s' % inc] = etree.SubElement(dati_procedimento, 'dati_allegati')
        for knfo,vnfo in allnfo.items():
            locals()[knfo] = etree.SubElement(locals()['dati_allegati_%s' % inc], knfo)
            v = allegati[knfo]
            assign_value(locals()[knfo], vnfo, *v)
        inc += 1

    if any([i.startswith('int_') for i in kw]):
        from xml_templates import integrazione
        dati_integrazione = etree.SubElement(dati_procedimento, 'dati_integrazione')
        for el,v in integrazione.items():
            locals()[el] = etree.SubElement(dati_integrazione, el)
            if 'dati_integrazione' in kw and el in kw['dati_integrazione']:
                assign_value(locals()[el], kw['dati_integrazione'][el], *v)
            elif el in kw:
                assign_value(locals()[el], kw[el], *v)

    return doc

def prepare_dati_procedimento(**kw):
    """
    doc url: http://projects.gisweb.it/projects/gisweb-irideworkflow/wiki/Wiki#Descrizione-degli-argomenti-wap
    """

    root_attributes = {xsi: "http:www.cedaf.it\schema\dati_procedimento.xsd"}
    root = etree.Element('dati_procedimento', encoding='ISO-8859-1', **root_attributes)
    doc = etree.ElementTree(root)

    from xml_templates import procedimento
    for el,v in procedimento.items():
        locals()[el] = etree.SubElement(root, el)
        if el in kw: assign_value(locals()[el], kw[el], *v)

    return doc

def prepare_ls_oneri(**wk):
    """
    """

    root_attributes = {xsi: "http:www.cedaf.it\schema\dati_procedimento.xsd"}
    root = etree.Element('dati_procedimento', encoding='ISO-8859-1', **root_attributes)
    doc = etree.ElementTree(root)
    from xml_templates import oneri
    for el,v in oneri.items():
        locals()[el] = etree.SubElement(root, el)
        if el in kw: assign_value(locals()[el], kw[el], *v)

    return doc

def deep_normalize(d):
    """ Normalize content of object returned from functions and methods """
    if 'sudsobject' in str(d.__class__):
        d = deep_normalize(dict(d))
    else:
        for k,v in d.iteritems():
            if 'sudsobject' in str(v.__class__):
                #print k, v, '%s' % v.__class__
                r = deep_normalize(dict(v))
                d[k] = r
            elif isinstance(v, dict):
                r = deep_normalize(v)
                d[k] = r
            elif isinstance(v, list):
                d[k] = [deep_normalize(i) for i in v]
            elif isinstance(v, datetime):
                # per problemi di permessi sugli oggetti datetime trasformo
                # in DateTime di Zope
                d[k] = DateTime(v.isoformat())
    return d

class Iride():
    """ Base class for interfacing to Iride web services """
    HOST = 'http://10.94.128.230' # 'http://127.0.0.1:3340' #
    SPATH = 'ulissetest/iride/web_services_20'
    Utente = UTENTE
    Ruolo = RUOLO
    timeout = 180

    def __init__(self, testinfo=False, **kw):
        self.testinfo = testinfo
        for k,v in kw.items():
            setattr(self, k, v)
        url = '/'.join((self.HOST, self.SPATH, self.service))
        self.url = url
        self.client = Client(url, location=url, timeout=self.timeout)

    def build_xml(self, name, **kw):
        """ Generic XML helper """
        xml = self.client.factory.create(name)
        # a quanto pare iride ha qualche problema con i valori settati a None
        # come è di default per cui i valori non forniti li setto a '' (stringa vuota)
        for k,v in dict(xml).items():
            # considero gli oggetti semplici
            if v == None:
                xml[k] = kw.get(k) or ''
            # qui ho considerato che la struttura o contiene oggetti semplici (vedi sopra)
            # o contiene oggetti ArrayOf<something>-like.
            elif k in kw and kw[k]:
                # l'elemento k di kw a questo punto sarà una lista di dizionari
                for o in kw[k]:
                    xml[k][xml[k].__keylist__[0]].append(self.build_xml(str(v).split('\n')[0][8:-2], **o))
        return xml
        
    def build_obj(self, name, **kw):
        """
        Helper for getting a dictionary with keys loaded from the correspondent
        xml-like object
        """
        xml = self.client.factory.create(name)
        obj = dict()
        for k in dict(xml):
            obj[k] = kw.get(k) or ''
        return obj

    def build_mittente(self, **kw):
        """ XML helper for MittenteDestinatarioIn-like object creation """
        return self.build_xml('MittenteDestinatarioIn', **kw)

    def build_allegato(self, **kw):
        """ XML helper for AllegatoIn-like object creation """

        # Image parameter value is required to be base64 encoded
        # I don't know how to verify if it's already encoded so DO NOT ENCODE! I do.
        if 'Image' in kw:
            kw['Image'] = b64encode(kw['Image'].data or '')

        return self.build_xml('AllegatoIn', **kw)

    def parse_response(self, res):
        """ Common response parsing """
        return deep_normalize(dict(res))

    def query_service(self, methodname, request):
        """ Standardize the output """
        service = getattr(self.client.service, methodname)
        out = dict(success=0, service=methodname)
        if self.testinfo: t0 = datetime.now()
        try:
            if isinstance(request, dict):
                res = service(**request)
            else:
                res = service(request)
        except Exception as err:
            out['message'] = '%s' % err
            # for debug purposes in case of exception reasons are in input data
            out['request'] = deep_normalize(dict(request))
        else:
            out['result'] = self.parse_response(res)
            if any([i in out['result'] for i in ('Errore', 'cod_err', )]):
                out['request'] = deep_normalize(dict(request))
            else:
                out['success'] = 1
            if self.testinfo:
                # for backward compatibility with python 2.6
                total_seconds = lambda x: x.seconds + x.microseconds*10**-6
                out['time_elapsed'] = total_seconds(datetime.now()-t0)
            
        return out

    def get_ProtocolloIn(self, mittenti=[], allegati=[], **kw):
        """ XML helper for ProtocolloIn-like object creation """

        defaults = dict(
            Utente = UTENTE,
            Ruolo = RUOLO,
            Origine = 'A',
            MittenteInterno = 'PROTO02',
            Data = date.today().isoformat(),
            Classifica = 'XVIII.02.03.'
        )

        request = self.build_xml('ProtocolloIn', **dict(defaults, **kw))

        for info in mittenti:
            mittente = self.build_mittente(**info)
            request.MittentiDestinatari.MittenteDestinatario.append(mittente)

        for info in allegati:
            allegato = self.build_allegato(**info)
            request.Allegati.Allegato.append(allegato)

        return request


class IridePratiche(Iride):
    """ Class for interfacing to Iride WS_Pratiche web service """

    service = 'WS_Pratiche/WS_Pratiche.asmx?WSDL'

    def __init__(self, **kw):
        Iride.__init__(self, **kw)

    def check(self):
        """ Check whether the connection is up """
        # TODO
        raise Exception("TODO")

    def parse_response(self, res):
        """ Custom response parsing """
        if 'sudsobject' in str(res.__class__):
            return deep_normalize(dict(res))
        else:
            encres = res.encode('utf-8')
            parser = etree.XMLParser(ns_clean=True, recover=True, encoding='utf-8')
            root = etree.fromstring(encres, parser=parser)
            xmldict = XmlDictConfig(root)
            return dict(xmldict)

    def wm_lista_procedimenti(self, ls_cod_fis, **kw):
        """
        Scopo: acquisizione della lista dei procedimenti amministrativi attivi per
            il soggetto in input.

        Argomenti:
            ls_cod_fis: codice fiscale del soggetto (persona fisica/giuridica);
            ls_sesid: sessione;
            ls_dtinizio: procedimenti validi dal;
            ls_dtfine: procedimenti validi dal;
            ls_stato: stato della pratica (i.e.: "In corso", "Terminati", "Tutti");
            wm_lista_procedimenti:  elenco dei procedimento amministrativi attivi
                per il soggetto indicato in entrata in formato XML.
        """

        request = self.build_xml('wm_lista_procedimenti',
            ls_cod_fis = ls_cod_fis,
            **kw
        )

        return self.query_service('wm_lista_procedimenti', request)

    def wm_procedimento(self, li_idproc, **kw):
        """
        Scopo:
            acquisizione di tutti gli attributi del procedimento amministrativo
            indicato in input.

        Argomenti:
            li_idproc: identificativo del procedimento;
        """

        request = self.build_xml('wm_procedimento',
            li_idproc = li_idproc,
            **kw
        )

        return self.query_service('wm_procedimento', request)

    def wm_attiva_procedimento(self,
        codice_fiscale_titolare,
        anagrafica_titolare,
        tipo_procedimento,
        oggetto,
        dati_procedimento,
        dati_richiesta,
        codice_fiscale_richiedente="",
        anagrafica_richiedente="",
    ):
        """
        Scopo:
            Inoltro al sistema legacy della richiesta di attivazione di un procedimento
            amministrativo. Tale WebMethod sarà invocato on-line in corrispondenza
            di ciascuna richiesta.

        Argomenti (monovalore)
            codice_fiscale_titolare : identificativo del soggetto intestatario del
                procedimento
            anagrafica_titolare: cognome/nome/ragione sociale dell'intestatario
                del  procedimento
            codice_fiscale_richiedente : identificativo del soggetto che attiva
                il procedimento
            anagrafica_richiedente: cognome/nome/ragione sociale del soggetto
                che attiva il procedimento
            tipo_procedimento: codifica del procedimento;
            oggetto: oggetto o breve descrizione della domanda (riportare alcuni
                attributi significativi del procedimento);
        Argomenti (xml)
            dati_procedimento: dizionario contenente i valori per la costruzione di
                un documento XML contenente tutti gli attributi del procedimento
                amministrativo eventualmente già attivato.
            dati_richiesta: dizionario contenente i valori per la costruzione di un
                documento XML contenente gli attributi necessari all'attivazione
                del procedimento amministrativo. Tale oggetto avrà una struttura
                variabile e dipendente dal tipo di procedimento amministrativo.
        """

        procedimento = doc2xml(prepare_dati_procedimento(**dati_procedimento))
        richiesta = doc2xml(prepare_xml_richiesta(**dati_richiesta))
        request = self.build_xml('wm_attiva_procedimento',
            codice_fiscale_titolare = codice_fiscale_titolare,
            anagrafica_titolare = anagrafica_titolare,
            codice_fiscale_richiedente = codice_fiscale_richiedente,
            anagrafica_richiedente = anagrafica_richiedente,
            tipo_procedimento = tipo_procedimento,
            argomento = oggetto,
            dati_procedimento = procedimento,
            xml_richiesta = richiesta
        )

        return self.query_service('wm_attiva_procedimento', request)

    def wm_doc(self, blo_id):
        """
        Scopo
            Recupero del file allegato relativo ad una pratica per una successiva
            visualizzazione

        Argomenti
            blo_id (int): identificativo univoco del blob da prelevare
        """

        request = self.build_xml('wm_doc',
            blo_id = blo_id
        )

        return self.query_service('wm_doc', request)

    def wm_oneri(self, docid):
        """
        Scopo
            Visualizzazione della situazione che riguarda gli oneri e le relative
            rate da pagare e/o quelle già pagate

        Argomenti
            docid: identificativo univoco del documento da prelevare
        """

        request = self.build_xml('wm_oneri',
            docid = docid
        )

        return self.query_service('wm_oneri', request)

    def wm_lista_oneri(self, codice_fiscale, filtro=''):
        """
        Scopo
            Visualizzazione della lista degli oneri legati ad un individuo

        Argomenti
            codice_fiscale: stringa in ingresso che fornisce il codice fiscale della
                persona della quale si vuole otenere la lista degli oneri.
            filtro: stringa in base la quale è possibile filtrare la lista degli oneri
                (i.e.: "T" tutti (default), "P" pagati e "N" da pagare)
        """

        
        request = self.build_xml('wm_lista_oneri',
            codice_fiscale = codice_fiscale,
            filtro = filtro
        )

        return self.query_service('wm_lista_oneri', request)

    def wm_pagato(self, dati_oneri):
        """
        Scopo
            Aggiornamento del campo data pagamento

        Argomenti
            ls_oneri: stringa in ingresso che fornisce il codice documento, il codice
            onere, la data pagamento e numero rata, necessari per la individuazione
            del record richiesto.
        """

        oneri = doc2xml(prepare_ls_oneri(**dati_oneri))
        
        request = self.build_xml('wm_pagato',
            ls_oneri = oneri
        )

        return self.query_service('wm_pagato', request)


class IrideProtocollo(Iride):
    """
    Class for interfacing to Iride WSProtocolloDM web service
    """

    service = 'WSProtocolloDM/WSProtocolloDM.asmx?WSDL'

    def __init__(self, **kw):
        Iride.__init__(self, **kw)

    def check(self):
        """ Check whether the connection is up """
        out = self.LeggiDocumento('000')
        if 'success' in out and 'result' in out:
            out.pop('result')
        else:
            out.pop('request')
        return out

    def LeggiDocumento(self, IdDocumento, **kw):
        """
        Restituisce i dati di un documento eventualmente protocollato a
        partire da IdDocumento.

        IdDocumento: identificativo del documento (str)
        """

        defaults = dict(
            Utente = UTENTE,
            Ruolo = RUOLO,
        )

        request = self.build_xml('LeggiDocumento',
            IdDocumento = IdDocumento,
            **dict(defaults, **kw)
        )

        return self.query_service('LeggiDocumento', request)

    def InserisciProtocollo(self, mittenti=[], allegati=[], **kw):
        """
        Inserisce un documento protocollato e le anagrafiche (max 100)
        ed eventualmente esegue l'avvio dell'iter.

        mittenti e allegati: liste di dizionari delle informazioni per la
            costruzione di oggetti xml MittenteDestinatarioIn-like e AllegatoIn-like
            attraverso i rispettivi metodi build_mittente e buil_allegato.
        """

        defaults = dict(
            Utente = UTENTE,
            Ruolo = RUOLO,
            Origine = 'A',
            MittenteInterno = 'PROTO02',
            Data = date.today().isoformat(),
            #Classifica = 'XVIII.02.03.',
        )

        request = self.build_xml('ProtocolloIn', **dict(defaults, **kw))

        for info in mittenti:
            mittente = self.build_mittente(**info)
            request.MittentiDestinatari.MittenteDestinatario.append(mittente)

        for info in allegati:
            allegato = self.build_allegato(**info)
            request.Allegati.Allegato.append(allegato)

        return self.query_service('InserisciProtocollo', request)

    def InserisciDatiUtente(self, Identificativo, DatiUtente, **kw):
        """
        Inserisce i dati utente associati a un documento, un soggetto o un'attivita'

        Identificativo: identificativo del documento (str);
        DatiUtente: dizionario delle informazioni per costruire un oggetto xml
                    contenente oggetti di DatiUtenteIn-like usando la funzione
                    prepare_string;
        """

        defaults = dict(
            Utente = UTENTE,
            Ruolo = RUOLO,
            Appartenenza = APPARTENENZA,
            CodiceAmministrazione = '',
            CodiceAOO = ''
        )

        request = self.build_obj('InserisciDatiUtente',
            Identificativo = Identificativo,
            DatiUtente = doc2xml(prepare_string2(DatiUtente, Identificativo)),
            **dict(defaults, **kw)
        )

        return self.query_service('InserisciDatiUtente', request)

    def InserisciDocumentoEAnagrafiche(self, mittenti=[], allegati=[], **kw):
        """
        Inserisce un documento non protocollato e le anagrafiche (max 100) ed
        eventualmente esegue l'avvio dell'iter
        """

        request = self.get_ProtocolloIn(mittenti=mittenti, allegati=allegati, **kw)

        return self.query_service('InserisciDocumento', request)

    def RicercaPerCodiceFiscale(self, CodiceFiscale, SoloProtocollo=False, **kw):
        """ Restituisce gli estremi dei documenti per codice fiscale
        dell'intestatario (eventualmente solo i protocollati).
        """

        defaults = dict(
            Utente = UTENTE,
            Ruolo = RUOLO,
        )

        request = self.build_xml('RicercaPerCodiceFiscale', **dict(defaults, **kw))

        return self.query_service('RicercaPerCodiceFiscale', request)

    def ModificaDocumentoEAnagrafiche(self, **kw):
        """ Partendo dal docid, o in sua assenza dall'anno e numero protocollo,
        il sistema provvederà a recuperare il documento e ad aggiornarlo con le
        informazioni presenti nell'xml di richiesta.
        """

        request = self.build_xml('ModificaDocumentoEAnagrafiche')
        sub_request = self.build_xml('ModificaProtocolloIn', **kw)
        request.ProtoIn = sub_request
        return self.query_service('ModificaDocumento', sub_request)


class IrideProcedimento(Iride):
    """
    WARNING: deprecated?!?
    Class for interfacing to Iride WSProcedimenti web service
    """

    service = 'WSProcedimenti/WSProcedimenti.asmx?WSDL'

    def __init__(self, **kw):
        Iride.__init__(self, **kw)

    def DettaglioProcedimento(self, IDProcedimento, **kw):
        """ Estrazione dei dati di dettaglio di un procedimento """

        defaults = dict(
            #Utente = UTENTE, Ruolo = RUOLO
        )
        request = self.build_xml('DettaglioProcedimento',
            **dict(defaults, IDProcedimento=IDProcedimento, **kw))
        return self.query_service('DettaglioProcedimento', request)


    def ListaProcedimenti(self, **kw):
        """
        Estrazione dei procedimenti / Extraction of the proceedings of a subject.

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

        request = self.build_xml('ListaProcedimenti', **kw)
        res = self.query_service('ListaProcedimenti', request)
        if self.testinfo and 'result' in res:
            res['length'] = len(res['result']['Procedimenti']) and \
                len(res['result']['Procedimenti']['Procedimento'])

        return res


    def AttivaProcedimento(self, NumeroPratica, mittenti=[], allegati=[], **kw):
        """ Attivazione di un procedimento """

        request = self.get_ProtocolloIn(
            mittenti = mittenti,
            allegati = allegati,
            NumeroPratica = NumeroPratica,
            **kw)
        return self.query_service('AttivaProcedimento', request)


if __name__ == '__main__':

    import sys
    from os import getcwd as os_getcwd
    from os.path import join as os_join
    sys.path.append(os_join(os_getcwd(), 'src/gisweb.irideworkflow/gisweb/irideworkflow/iride/'))

    doc = prepare_xml_richiesta(tit_desindr='VIA ARNIER',
        tit_codfisc='NNNMRC65R12H294J', tit_dtnas=datetime(1965, 4, 2), int_annopr=1984)
    print doc2xml(doc, pprint=True)