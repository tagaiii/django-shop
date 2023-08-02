from django.urls import path

from .views import *

urlpatterns = [
    path('', BaseSpecs.as_view(), name='base_specs'),
    path('new-feature/', NewFeature.as_view(), name='new_feature'),
    path('new-manufacturer/', NewManufacturer.as_view(), name='new_manufacturer'),
]