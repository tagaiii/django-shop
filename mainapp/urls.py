from django.urls import path
from django.contrib.auth.views import LogoutView

from .views import *

urlpatterns = [
    path('', BaseView.as_view(), name='base'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('staff/', StaffBase.as_view(), name='staff_base'),
    path('staff/registration/', StaffRegistration.as_view(), name='staff_registration'),
    path('cart/', CartView.as_view(), name='cart' ),
    path('add-to-cart/<str:slug>/', AddToCart.as_view(), name='add_to_cart'),
    path('delete-from-cart/<str:slug>/', DeleteFromCart.as_view(), name='delete_from_cart'),
    path('change-product-qty/<str:slug>/', ChangeProductQty.as_view(), name='change_product_qty'),
    path('catalog/', Catalog.as_view(), name='catalog'),
    path('catalog/<str:slug>/', ManufacturerCategory.as_view(), name='manufacturer_category'),
    path('catalog/<str:manufacturer>/<str:slug>/', ProductDetail.as_view(), name='product_detail'),
    path('search/', SearchProduct.as_view(), name='search_product'),
]