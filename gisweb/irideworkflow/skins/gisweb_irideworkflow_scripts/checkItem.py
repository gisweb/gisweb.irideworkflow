## Script (Python) "checkItem"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=itemname, default=None, dateformat='ISO'
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
    if dateformat in ('ISO', ):
        return value.ISO()
    else:
        return value.strftime(dateformat)
else:
    return value