# -*- coding: utf-8 -*-

from Products.CMFPlomino.PlominoUtils import csv_to_array
from pkg_resources import resource_string
filepath = 'utils/dbo_GEO_COMUNE.csv'
CCI = csv_to_array(resource_string(__name__, filepath), delimiter=';', quotechar='"')

def getCodcom(codfisco, error=False):
    """
    dato un codice fiscale di un comune voglio il corrispondente codice ISTAT.
    """

    if codfisco in (None, '', ): return None

    i = CCI[0].index('GCO_ISTAT')
    j = CCI[0].index('GCO_CODCAT')
    flt = lambda row : row[j].upper()==codfisco.upper()
    res = filter(flt, CCI)

    vals = tuple(set([j[i] for j in res]))
    if error:
        assert len(vals)==1, 'CODCAT: %s corresponds too may values: %s' % (codfisco, vals)
    # in case of multiple results I get the last one (hoping it's an updated version)
    return int(vals[0])
