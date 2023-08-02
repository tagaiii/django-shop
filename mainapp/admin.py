from django.contrib import admin

from .models import *
from features_app.models import *

admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Manufacturer)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(Staff)
admin.site.register(OrderDetail)
admin.site.register(Feature)
admin.site.register(Images)