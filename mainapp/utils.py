from django.db import models

def calculate_cart(cart):
    cart_data = cart.products.aggregate(models.Sum('total_price'))
    if cart_data.get('total_price__sum'):
        cart.total_price = cart_data['total_price__sum']
        print(cart.total_price)
        print(cart_data['total_price__sum'])
    else:
        cart.total_price = 0
    cart.save()