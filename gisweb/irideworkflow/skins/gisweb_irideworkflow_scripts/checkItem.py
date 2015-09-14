## Script (Python) "checkItem"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=itemname, default=None, format='%d/%m/%Y', check=True
##title=
##
# Example code:

items = context.getItems()
fields = [i.getId() for i in context.getForm().getFormFields(includesubforms=True)]

# il test serve per verificare l'allineamento tra i form e questo script,
# caso mai venissero aggiornati i nomi di alcuni campi.
# In tal caso voglio essere avvertito prima possibile!!
if check:
    assert itemname in items+fields, 'Missing PlominoField %s' % (itemname)

value = context.getItem(itemname, default)

fld = context.getForm().getFormField(itemname)

if fld and fld.getFieldType() in ('SELECTION', ) and fld.getSettings('widget') in ('SELECT', 'RADIO', ):
    nfo = dict([i.split('|')[::-1] for i in fld.getSettings().getSelectionList(context)])
    return nfo.get(value)

if format==None:
    return value

elif callable(format):
    return format(value)

elif isinstance(value, DateTime):
    if format.upper() in ('ISO', ):
        return value.ISO()
    elif format:
        return value.strftime(format)

elif format == 'S/N':
    if value:
        return 'S'
    else:
        return 'N'

return value