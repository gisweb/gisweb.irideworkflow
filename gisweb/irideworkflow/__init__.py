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
        out[session] = dict([(k,v) for k,v in config.items(session) if v])
    return out