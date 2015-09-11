 ## Script (Python) "iride_ricerca_procedimento"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=cf, docid, format='json', testinfo=False
##title=
##
"""
Estrae le informazioni del procedimento direttamente a partire da una pratica.

Parametri:
    cf    (str): codice fiscale del soggetto richiedente;
    docid (int): id iride del documento (item corrispondente: irideIdDocumento).
"""

from gisweb.irideworkflow import procedimento_pratica
from gisweb.utils import json_dumps, Type
#from Products.CMFPlomino.PlominoUtils import htmlencode

query_params = dict(
    cf = cf,
    docid = int(docid),
    testinfo = testinfo,
    **context.Iride_loadPortalSettings()
)

sdm = context.session_data_manager
sd = sdm.getSessionData()

if not sd.has_key('gisweb.irideworkflow.procedimento_pratica'):
    sd['gisweb.irideworkflow.procedimento_pratica'] = dict()

def query_web_service():
    try:
        out = procedimento_pratica(**query_params)
    except Exception as err:
        errmsg = str(err)
        errtype = Type(err)
        out = dict(success=0, message='%s: %s' % (errtype, errmsg))

    sd['gisweb.irideworkflow.procedimento_pratica'][json_dumps(query_params)] = out
    
    return out

data = sd['gisweb.irideworkflow.procedimento_pratica'].get(json_dumps(query_params)) or dict()

if not data.get('success'):
    data = query_web_service()

if format=='json':
    context.REQUEST.RESPONSE.setHeader("Content-type", "application/json")
    print json_dumps(data, customformat='ISO')
    return printed
elif format.endswith('.pt'):
    pt = getattr(context, format[:-3])
    if pt:
        context.REQUEST.RESPONSE.setHeader("Content-type", "text/html")
        print pt(**data).strip()
        return printed

return data
