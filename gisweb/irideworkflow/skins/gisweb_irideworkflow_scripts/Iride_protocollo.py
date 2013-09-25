## Script (Python) "Iride_protocollo"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=tipo, oggetto=None, data=None, testinfo=False, results=0
##title=
##
# Example code:

"""
tipo: tipo di protocollo (E o A: Entrata/Arrivo, U o P: Uscita/Partenza, I: Interno)
oggetto:
data: data della richiesta di protocollazione (se mancante verrà usata quella
    corrente dalle procedure interne)

testinfo e results sono parametri di test
"""

assert context.isAuthor(), "You need edit permission on this document!"

from gisweb.irideworkflow import inserisci_protocollo

# così mantengo la compatibilità con il comportamento degli script di workflow
# basati sulle API del protocollo del Comune della Spezia:
# U: protocollo in uscita (o partenza)
# E: protocollo in entrata (o arrivo)
# il valore I (protocollo interno) non ha corrispondenze
diz = dict(E='A', U='P')

MittentiIn = context.IrideLayer.MittentiDestinatariIn()
AllegatiIn = context.IrideLayer.AllegatoIn()
UtenteIn = context.IrideLayer.DatiUtenteIn()
ProtocolloIn = context.IrideLayer.ProtocolloIn()

ProtocolloIn['Origine'] = diz.get(tipo) or tipo
if oggetto!=None:
    ProtocolloIn['Oggetto'] = oggetto
if data != None:
    ProtocolloIn['Data'] = data

res_protocollo, res_utente = inserisci_protocollo(MittentiIn, AllegatiIn,
    UtenteIn, ProtocolloIn, testinfo=testinfo, **context.Iride_loadPortalSettings())

if 'result' in res_protocollo:
    if not res_protocollo['result'].get('Errore'):
        context.setItem('numero_protocollo', res_protocollo['result']['NumeroProtocollo'])
        context.setItem('data_protocollo', res_protocollo['result']['DataProtocollo'])
        context.setItem('irideIdDocumento', res_protocollo['result']['IdDocumento'])
        context.addPortalMessage(res_protocollo['result']['Messaggio'], msg_type='info')
    else:
        context.addPortalMessage(res_protocollo['result']['Errore'], msg_type='error')
else:
    context.addPortalMessage(res_protocollo['message'], msg_type='error')

# for test porposes only
if results == 1:
    return res_protocollo
elif results == 2:
    return res_protocollo, res_utente