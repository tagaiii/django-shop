from django import forms

from .models import Feature
from mainapp.models import Manufacturer

class NewFeatureForm(forms.ModelForm):

    class Meta:
        model = Feature
        fields = ['name', 'product', 'unit', 'value']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'product': forms.Select(attrs={'class': 'form-select'}),
            'unit': forms.TextInput(attrs={'class': 'form-control'}),
            'value': forms.TextInput(attrs={'class': 'form-control'})
        }


class NewManufacturerForm(forms.ModelForm):

    class Meta:
        model = Manufacturer
        fields = ['name', 'logo']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'logo': forms.ClearableFileInput(attrs={'class': 'form-control'})
        }
