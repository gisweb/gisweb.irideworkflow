## Script (Python) "InserisciDatiUtente"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=testinfo=False, json=False, pmsg=True
##title=
##
# Example code:

docid = context.getItem('irideIdDocumento')
test = context.getItem('InserisciDatiUtenteFailed')

assert docid, 'Nessun ID trovato NON posso procedere'
#assert not test, ''

from gisweb.irideworkflow import InserisciDatiUtente
from gisweb.utils import json_dumps

UtenteIn = context.IrideLayer.DatiUtenteIn()
res = InserisciDatiUtente(docid, UtenteIn, testinfo=True, **context.Iride_loadPortalSettings())

msgtype = 'info'
if not res['success']:
    context.setItem('InserisciDatiUtenteFailed', True)
    if pmsg:
        msg = res.get('message') or res['result'].get('Errore')
        msgtype = 'error'
else:
    if test:
        context.removeItem('InserisciDatiUtenteFailed')
    msg = ''
    # WARNING: il messaggio di conferma in uscita da Iride non è di interesse per 
    # un semplice utente che compila la domanda.
    # TODO: al limite si può rendere visibile per debug.
    #if pmsg:
        #msg = res['result']['Messaggio']

if pmsg and msg:
    context.addPortalMessage(msg, msg_type=msgtype)

if json:
    context.REQUEST.RESPONSE.setHeader("Content-type", "application/json")
    print json_dumps(res, prettyxml=True)
    return printed
else:
    return res