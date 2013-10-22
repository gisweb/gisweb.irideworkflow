# -*- coding: utf-8 -*-

from Products.CMFPlomino.PlominoUtils import csv_to_array
import os

path = 'src/gisweb.irideworkflow/gisweb/irideworkflow/iride/'
# in case spervisord is used
if os.getcwd().endswith('bin'):
    path = '../' + path
filepath = 'utils/dbo_GEO_COMUNE.csv'

def getcci():
    with open(path+filepath, 'r') as source:
        # Codici Comuni Iride
        CCI =  csv_to_array(source.read(), delimiter=';', quotechar='"')
    return CCI
    
def getCodcom(codfisco):
    """
    dato un codice fiscale di un comune voglio il corrispondente codice ISTAT.
    """
    assert codfisco, 'Variable has to be evaluated as True'
    CCI = getcci()
    i = CCI[0].index('GCO_ISTAT')
    flt = lambda row : row[4].upper()==codfisco.upper()
    res = filter(flt, CCI)
    vals = tuple(set([j[i] for j in res]))
    assert len(vals)==1, 'Too many values obtained from file %s.' % filepath
    return int(vals[0])

    