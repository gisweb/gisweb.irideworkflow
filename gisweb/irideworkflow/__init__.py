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
