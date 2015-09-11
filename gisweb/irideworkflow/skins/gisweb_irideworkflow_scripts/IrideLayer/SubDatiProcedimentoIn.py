## Script (Python) "SubDatiProcedimentoIn"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##
# Example code:

"""
Parametri:
    protocollo_automatico (Stringa) Indicatore di protocollazione automatica del
        documento relativo al procedimento. Valori ammessi: Si/No, default = Si;

Chiavi da restituire:
    pro_id                (Numerico) Numero identificativo del procedimento
    pro_nrprot            (Numerico) Numero del protocollo
    pro_dtprot            (Data)     Data protocollo
    pro_anno_proc         (Numerico) Anno di riferimento del procedimento
    pro_respon            (Stringa)  Responsabile del procedimento
    pro_stato             (Stringa)  Stato del procedimento
    pro_dtarr             (Data)     Data arrivo procedimento
    pro_ricpro            (Stringa)  Flag di richiesta protocollazione al procedimento
    protocollo_automatico (Stringa)  SI/NO ???
"""

return dict()