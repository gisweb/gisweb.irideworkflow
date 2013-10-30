# -*- coding: utf-8 -*-
# -*- extra stuff goes here -*-

from AccessControl import allow_module, ModuleSecurityInfo
#from z3c.saconfig import named_scoped_session

allow_module('gisweb.irideworkflow')
#allow_module('gisweb.irideworkflow.iride')

def initialize(context):
    """Initializer called when used as a Zope 2 product."""

from tools import test_di_connessione
from tools import leggi_documento
from tools import inserisci_protocollo
from tools import procedimento_pratica
from tools import test_build_mittente, test_prepare_string, test_build_xml
from tools import wm_attiva_procedimento, InserisciDatiUtente

from iride.xml_templates import titolare as xml_template_titolare
from iride.xml_templates import richiedente as xml_template_richiedente
from iride.xml_templates import integrazione as xml_template_integrazione
from iride.xml_templates import allegati as xml_template_allegati

from iride.interface import prepare_xml_richiesta, doc2xml
from iride.utils import getCodcom

import ConfigParser
try:
    import cStringIO as StringIO
except ImportError:
    import StringIO

def conf2dict(string):

    config = ConfigParser.RawConfigParser(allow_no_value=True)
    config.optionxform=str
    config.readfp(StringIO.StringIO(string))
    
    out = dict()
    for session in config.sections():
        out[session] = dict([(k,v) for k,v in config.items(session)])
    return out
