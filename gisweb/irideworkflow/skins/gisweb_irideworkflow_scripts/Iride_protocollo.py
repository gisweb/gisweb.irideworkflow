## Script (Python) "Iride_protocollo"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=oggetto=None, data=None, protocollo_automatico='SI', pmsg=True, testinfo=False, json=False
##title=
##
# Example code:

"""
    oggetto (String):
        se non specificato diversamente viene considerato il titolo del documento;
    data (String):
        data della richiesta di protocollazione (se mancante verrà usata quella
        corrente dalle procedure interne)
    protocollo_automatico (String):
        valori accettai: SI/NO. utile per inibire la protocollazione.
        caso d'uso: invio di pratiche pregresse già protocollate
    pmsg (Boolean):
        se i messaggi di errore debbano essere passati al PortalMessage

    testinfo e json sono parametri di test/debug.
"""

assert context.isAuthor(), "You need edit permission on this document!"
from gisweb.irideworkflow import leggi_documento

out = []

if not context.getItem('irideIdDocumento'):
    res1 = context.wm_attiva_procedimento(oggetto=oggetto, data=data,
        testinfo=testinfo, protocollo_automatico=protocollo_automatico, json=False, pmsg=pmsg)

    out.append(res1)

docid = context.getItem('irideIdDocumento')
if docid:
    res2 = context.InserisciDatiUtente(testinfo=testinfo, json=False, pmsg=pmsg)
    out.append(res2)

    # 1. richiamare il servizio LeggiDocumento con ID del documento

    # OutLeggiDocumento = leggi_documento(docid)

    ## 2. compilare l'array MittentiDestinatari con i dati della lettura completa
    # tramite il servizio LeggiAnagrafica per ciascun id di soggetto per
    # preservare i soggetti mittenti esistenti

    # 3. inserire in aggiunta nell'array MittentiDestinatari i nuovi soggetti
    # cointestatari

    res3 = context.ModificaSoloAnagrafiche(testinfo=testinfo, json=False)
    out.append(res3)

if json:
    from gisweb.utils import json_dumps
    context.REQUEST.RESPONSE.setHeader("Content-type", "application/json")
    print json_dumps(out, prettyxml=True)
    return printed
else:
    return out