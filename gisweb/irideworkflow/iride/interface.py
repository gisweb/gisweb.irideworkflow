# -*- coding: utf-8 -*-

from suds.client import Client
from datetime import datetime, date
from base64 import b64encode
from DateTime import DateTime

# this url is good if you
# ssh siti.provincia.sp.it -L 3340:10.94.128.230:80 -p 2229
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
                IRIDE_DOCID=docid,
                IRIDE_PROGR=i,
                IRIDE_FONTE='GW',
                IRIDE_DATINS=get_current_datetime_as_string(),
            )
            result.append('<row>')
            for keyvalue in row.items():
                result.append('<field name="%s">%s</field>' % keyvalue)
            result.append('</row>')
        result.append('</table>')
    result.append("</DatiUtenteIn>")
    return '\n'.join(result)

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

    def __init__(self, SERVICE_NAME, testinfo=False, **kw):
        self.testinfo = testinfo

        for k,v in kw.items():
            setattr(self, k, v)

        self.__set_client__(SERVICE_NAME)

    def __set_client__(self, service):
        """ Set the right client associated to the service as an attribute """
        WSProtocolloDM = 'WSProtocolloDM/WSProtocolloDM.asmx?WSDL'
        WSProcedimenti = 'WSProcedimenti/WSProcedimenti.asmx?WSDL'

        url = '/'.join((self.HOST, self.SPATH, locals()[service]))
        self.url = url
        self.client = Client(url, location=url, timeout=180)

    def build_xml(self, name, **kw):
        """ Generic XML helper """
        xml = self.client.factory.create(name)
        # a quanto pare iride ha qualche problema con i valori settati a None
        # come è di default per cui i valori non forniti li setto a '' (stringa vuota)
        for k,v in dict(xml).items():
            # considero SOLO gli oggetti semplici
            if v == None:
                xml[k] = kw.get(k) or ''
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

    def query_service(self, service, request):
        """ Standardize the output """

        out = dict(success=0)
        if self.testinfo: t0 = datetime.now()
        try:
            if isinstance(request, dict):
                res = service(**request)
            else:
                res = service(request)
        except Exception as err:
            out['message'] = '%s' % err
            # for debug purposes in case of exception (or error) reasons are in input data
            out['request'] = deep_normalize(dict(request))
        else:
            if 'Errore' in res:
                out['request'] = deep_normalize(dict(request))
            if self.testinfo:
                # for backward compatibility with python 2.6
                total_seconds = lambda x: x.seconds + x.microseconds*10**-6
                out['time_elapsed'] = total_seconds(datetime.now()-t0)
            out['success'] = 1
            out['result'] = deep_normalize(dict(res))
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


class IrideProtocollo(Iride):
    """ Class for interfacing to Iride WSProtocolloDM web service """

    #SERVICE_NAME = 'WSProtocolloDM'
    method_to_test = 'RicercaPerCodiceFiscale'

    def __init__(self, **kw):
        Iride.__init__(self, 'WSProtocolloDM', **kw)

    def check(self):
        """ Check whether the connection is up """
        out = self.LeggiDocumento('000')
        if 'success' in out:
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

        return self.query_service(self.client.service.LeggiDocumento, request)

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

        return self.query_service(self.client.service.InserisciProtocollo, request)

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
            DatiUtente = prepare_string(DatiUtente, Identificativo),
            **dict(defaults, **kw)
        )

        return self.query_service(self.client.service.InserisciDatiUtente, request)

    def InserisciDocumentoEAnagrafiche(self, mittenti=[], allegati=[], **kw):
        """
        TODO
        Inserisce un documento non protocollato e le anagrafiche (max 100) ed
        eventualmente esegue l'avvio dell'iter
        """

        request = self.get_ProtocolloIn(mittenti=mittenti, allegati=allegati, **kw)

        return self.query_service(self.client.service.InserisciDocumento, request)

    def RicercaPerCodiceFiscale(self, CodiceFiscale, SoloProtocollo=False, **kw):
        """
        Restituisce gli estremi dei documenti (eventualmente solo i protocollati)
        per codice fiscale dell'intestatario.
        """

        defaults = dict(
            Utente = UTENTE,
            Ruolo = RUOLO,
        )

        request = self.build_xml('RicercaPerCodiceFiscale', **dict(defaults, **kw))

        self.query_service(self.client.service.RicercaPerCodiceFiscale, request)


class IrideProcedimento(Iride):
    """ Class for interfacing to Iride WSProcedimenti web service """

    def __init__(self, **kw):
        Iride.__init__(self, 'WSProcedimenti', **kw)

    def DettaglioProcedimento(self, IDProcedimento, **kw):
        """ Estrazione dei dati di dettaglio di un procedimento """

        defaults = dict(
            #Utente = UTENTE, Ruolo = RUOLO
        )
        request = self.build_xml('DettaglioProcedimento',
            **dict(defaults, IDProcedimento=IDProcedimento, **kw))
        return self.query_service(self.client.service.DettaglioProcedimento, request)


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
        res = self.query_service(self.client.service.ListaProcedimenti, request)
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
        return self.query_service(self.client.service.AttivaProcedimento, request)