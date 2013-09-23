## Script (Python) "checkItem"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=itemname, default=None, format='ISO'
##title=
##
# Example code:

items = context.getItems()
fields = [i.getId() for i in context.getForm().getFormFields(includesubforms=True)]

# il test serve per verificare l'allineamento tra i form e questo script,
# caso mai venissero aggiornati i nomi di alcuni campi.
# In tal caso voglio essere avvertito prima possibile!!
assert itemname in items+fields, 'Missing PlominoField %s' % (itemname)

value = context.getItem(itemname, default)

if isinstance(value, DateTime):
    if format in ('ISO', ):
        return value.ISO()
    elif format:
        return value.strftime(format)

elif isinstance(1, (bool, int, basestring, )):
    if format == 'S/N':
        if value:
            return 'S'
        else:
            return 'N'

return value