## Script (Python) "Iride_protocollo"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=oggetto=None, data=None, testinfo=False, json=False, pmsg=True
##title=
##
# Example code:

"""
oggetto: se non specificato diversamente viene considerato il titolo del documento;
data: data della richiesta di protocollazione (se mancante verrà usata quella
    corrente dalle procedure interne)

testinfo e results sono parametri di test
"""

assert context.isAuthor(), "You need edit permission on this document!"
from gisweb.utils import json_dumps

out = []

if not context.getItem('irideIdDocumento'):
    res1 = context.wm_attiva_procedimento(oggetto=oggetto, data=data, testinfo=testinfo, json=False, pmsg=pmsg)
    out.append(res1)

if context.getItem('irideIdDocumento'):
    res2 = context.InserisciDatiUtente(testinfo=testinfo, json=False, pmsg=pmsg)
    out.append(res2)

    res3 = context.ModificaSoloAnagrafiche(testinfo=testinfo, json=False)
    out.append(res3)

if json:
    context.REQUEST.RESPONSE.setHeader("Content-type", "application/json")
    print json_dumps(out, prettyxml=True)
    return printed
else:
    return out