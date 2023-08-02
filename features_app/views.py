from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect
    
from django.views import View 
from .mixins import SuperuserCheckMixin
from .forms import *

class BaseSpecs(SuperuserCheckMixin, View):
    template = 'features_app/home_specs.html'


class NewFeature(SuperuserCheckMixin, View):
    form = NewFeatureForm()
    template = 'features_app/new_feature.html'

    def post(self, request):
        form = NewFeatureForm(request.POST)
        if form.is_valid():
            new_feature = form.save(commit=False)
            new_feature.name = form.cleaned_data['name']
            new_feature.unit = form.cleaned_data['unit']
            new_feature.value = form.cleaned_data['value']
            new_feature.save()
            new_feature.product.features.add(new_feature)
            return HttpResponseRedirect('/product-specs/')
        context = {'form': form}
        return render(request, 'features_app/new_feature.html', context)


class NewManufacturer(SuperuserCheckMixin, View):
    form = NewManufacturerForm()
    template = 'features_app/new_manufacturer.html'

    def post(self, request):
        form = NewManufacturerForm(request.POST, request.FILES)
        if form.is_valid():
            new_manufacturer = form.save(commit=False)
            new_manufacturer.name = form.cleaned_data['name']
            new_manufacturer.logo = request.FILES['logo']
            new_manufacturer.save()
            return HttpResponseRedirect('/product-specs/')
        context = {'form': form}
        return render(request, 'features_app/new_manufacturer.html', context)