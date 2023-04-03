from django.contrib import admin
from myapp.models import customer, category, product, brands, cart, mail, order

admin.site.site_header='Electronic Store'

class productAdmin(admin.ModelAdmin):
    list_display = ['product_name','create_date']

admin.site.register(customer)
admin.site.register(category)
admin.site.register(product,productAdmin)
admin.site.register(brands)
admin.site.register(cart)
admin.site.register(mail)
admin.site.register(order)
