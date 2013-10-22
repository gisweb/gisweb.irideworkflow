# -*- coding: utf-8 -*-

from Products.CMFPlomino.PlominoUtils import csv_to_array
import os

from pkg_resources import resource_string

CCI = csv_to_array(resource_string(__name__, 'utils/dbo_GEO_COMUNE.csv'), delimiter=';', quotechar='"')
    
def getCodcom(codfisco):
    """
    dato un codice fiscale di un comune voglio il corrispondente codice ISTAT.
    """
    assert codfisco, 'Variable has to be evaluated as True'
    i = CCI[0].index('GCO_ISTAT')
    flt = lambda row : row[4].upper()==codfisco.upper()
    res = filter(flt, CCI)
    vals = tuple(set([j[i] for j in res]))
    assert len(vals)==1, 'Too many values obtained from file %s.' % filepath
    return int(vals[0])

    