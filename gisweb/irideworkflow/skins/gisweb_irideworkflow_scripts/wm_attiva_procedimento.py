## Script (Python) "wm_attiva_procedimento"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=oggetto=None, data=None, protocollo_automatico=True, testinfo=False, json=False, pmsg=True
##title=
##
# Example code:

from Products.CMFPlomino.PlominoUtils import StringToDate
from gisweb.irideworkflow import wm_attiva_procedimento
from gisweb.utils import json_dumps

DataIn = context.IrideLayer.WMAttivaProcedimentoIn(protocollo_automatico=protocollo_automatico)
res = wm_attiva_procedimento(DataIn, testinfo=testinfo, **context.Iride_loadPortalSettings())
msg = ''

if res['success']:
    docid = res['result']['pro_id']
    nprot = res['result']['pro_nrprot']
    dprot = StringToDate(res['result']['pro_dtprot'])
    context.setItem('irideIdDocumento', docid)
    context.setItem('numero_protocollo', nprot)
    context.setItem('data_protocollo', dprot)

    if pmsg:
        msg = 'Pratica inviata con successo!'
        msgtype = 'info'
elif pmsg:
    msg = res.get('message') or ('Errore n. %s: %s' % (res['result'].get('cod_err'), res['result'].get('des_err'), ))
    msgtype = 'error'

if pmsg:
    context.addPortalMessage(msg, msg_type=msgtype)
if json:
    context.REQUEST.RESPONSE.setHeader("Content-type", "application/json")
    print json_dumps(res, prettyxml=True)
    return printed
else:
    return res