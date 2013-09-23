## Script (Python) "DatiUtenteIn"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Build a DatiUtenteIn-like object
##
# Example code:

"""
Ricava dal PlominoDocument le informazioni utili per costruire un oggetto
DatiUtenteIn-like.
"""

from gisweb.irideworkflow import conf2dict
from gisweb.utils import json_dumps, json_loads

plominoDocument = context.getParentDocument()
conf_name = '%s.txt' % plominoDocument.getForm().getFormName()
resources = plominoDocument.getParentDatabase().resources

msg = 'Layer per la pratica "%s" NON ancora implementato!' % plominoDocument.Title().decode('ascii', errors='replace').encode('ascii', errors='replace')

if conf_name in script.config.keys():
    conf = conf2dict(str(getattr(script.config, conf_name)))
elif 'IrideLayer' in resources.keys() and conf_name in resources.IrideLayer.keys():
    conf = conf2dict(str(getattr(resources.IrideLayer, conf_name)))
else:
    assert False, msg

out = dict()

def getrecords(doc, values):

    if isinstance(doc, basestring):
        doc = plominoDocument.getParentDatabase().getDocument(doc)
    
    record = dict()
    for k,raw in values.items():
            # per valore semplicemente mancante nel file di configurazione
            # considero <nome campo> == <nome colonna>
            if not raw: raw=k
            v = raw.split(',')
            value = doc.checkItem(*v)
            if value:
                record[k] = value
    return record

def foo(v):
    return json_loads(json_dumps(v))
    
for tablename,values in conf.items():
    record = dict()
    if tablename not in ['CONFIG'] + conf['CONFIG'].keys():
        out[tablename] = (getrecords(plominoDocument, values), )

    elif tablename != 'CONFIG':
        fieldcontainer = conf['CONFIG'][tablename]
        plominoForm = plominoDocument.getForm()
        plominoField = plominoForm.getFormField(fieldcontainer)
        fieldtype = plominoField.getFieldType()
        itemvalue = plominoDocument.getItem(fieldcontainer, []) or []
        if fieldtype == 'DOCLINK':
            if itemvalue:
                out[tablename] = tuple()
                for docid in itemvalue:
                    out[tablename] = out[tablename] + (getrecords(docid, values), )
        if fieldtype == 'DATAGRID':
            if itemvalue:
                out[tablename] = tuple()
                sortedfields = plominoField.getSettings().field_mapping.split(',')
                for rec in itemvalue:
                    record = dict()
                    for k,raw in values.items():
                        v = raw.split(',')[0] # non uso checkItem, non considero eventuali attributi
                        record[k] = foo(rec[sortedfields.index(v)])
                    out[tablename] = out[tablename] + (record, )

return out



#fieldmap = fieldmaps.get(key) or dict()
#out = dict()
#for k,fun in fieldmap.items():
    #res = fun(plominoDocument)
    #if res != None:
        #out[k] = res

#return {tablenames[key]: (out, )}