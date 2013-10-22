# -*- coding: utf-8 -*-
from datetime import datetime
from base64 import b64encode
try:
    from DateTime import DateTime
except:
    DateTime = datetime


tstr = (lambda x: isinstance(x, basestring), lambda x: x, )
tint =  (lambda x: isinstance(x, int), lambda x: str(x), )
tdate = (lambda x: isinstance(x, (DateTime, datetime)), lambda x: x.strftime('%Y-%m-%d'), )
tblob = (lambda x: True, lambda x: b64encode(x))
tflt = (lambda x: isinstance(x, float), lambda x: '%.3f' % x)

tblob2 = (lambda x: True, lambda x: '') # TODO: remove!
tcodcom = (lambda x: True, lambda x: '40007') # TODO: remove!
tdescomr = (lambda x: True, lambda x: 'CESENA') # TODO: remove!

titolare = dict(
    tit_codfisc = tstr,
    tit_tiposog = tstr,
    tit_cognome = tstr,
    tit_nome = tstr,
    tit_codluon = tint,
    tit_desluon = tstr,
    tit_codpron = tstr,
    tit_dtnas = tdate,
    tit_sesso = tstr,
    tit_codcomr = tint,
    tit_descomr = tstr,
    tit_codpror = tstr,
    tit_capr = tstr,
    tit_codres = tstr,
    tit_desindr = tstr,
    tit_numciv = tint,
    tit_desnatg = tstr,
    tit_numtel = tstr,
    tit_codcit = tstr,
    tit_descit = tstr,
    tit_email = tstr,
    tit_pec = tstr,
    tit_cell = tstr,
)

richiedente = dict([(k.replace('tit_', 'ric_'),v) for k,v in titolare.items()])

allegati = dict(
    all_blob = tblob,
    all_descri = tstr,
    all_tipo = tstr,
    all_nomefile = tstr,
    all_firma = tstr
)

integrazione = dict(
    int_numeropr = tstr,
    int_annopr = tint,
    int_datapr = tdate
)

procedimento = dict(
    pro_id = tint,
    pro_nrprot = tint,
    pro_dtprot = tdate,
    pro_anno_proc = tint,
    pro_respon = tstr,
    pro_stato = tstr,
    pro_dtarr = tdate,
    pro_ricpro = tstr
)

oneri = dict(
    one_docid = tint,
    one_ogg = tstr,
    one_nrata = tint,
    one_codice = tstr,
    one_descr = tstr,
    one_datascad = tdate,
    one_datapag = tdate,
    one_importo  = tflt,
    one_mora = tflt
)