from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.shortcuts import HttpResponseRedirect

from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission
from django.db.models import Q

from django.contrib.auth import authenticate
from django.contrib.auth import login

from django.views import View
from django.views.generic import ListView
from .models import *

from .forms import *
from .mixins import CartMixin
from .utils import calculate_cart

class BaseView(CartMixin, View):

    def get(self, request):
        manufacturers = Manufacturer.objects.all()
        phones = Product.objects.all()
        context = {'manufacturers': manufacturers, 'phones': phones, 'cart': self.cart}
        return render(request, 'base.html', context)

class ProductDetail(CartMixin, View):

    def get(self, request, slug, manufacturer):
        phone = get_object_or_404(Product, slug__iexact=slug)
        related_phones = Product.objects.filter(manufacturer=phone.manufacturer.id).exclude(title=phone.title)
        manufacturer = manufacturer
        context = {'phone': phone, 'manufacturer': manufacturer, 'related_phones': related_phones, 'cart': self.cart} 
        return render(request, "mainapp/product_detail.html", context)


class ManufacturerCategory(CartMixin, View):

    def get(self, request, slug):
        manufacturer = get_object_or_404(Manufacturer, slug__iexact=slug)
        phones = Product.objects.filter(manufacturer=manufacturer)
        context = {'manufacturer': manufacturer, 'phones': phones, 'cart': self.cart}
        return render(request, "mainapp/manufacturer_category.html", context)


class Catalog(CartMixin, View):

    def get(self, request):
        manufacturers = Manufacturer.objects.all()
        context = {'manufacturers': manufacturers, 'cart': self.cart}
        return render(request, "mainapp/catalog.html", context)


class CartView(CartMixin, View):

    def get(self, request):
        context = {'cart': self.cart}
        return render(request, 'mainapp/cart.html', context)


class AddToCart(CartMixin, View):

    def get(self, request, *args, **kwargs):
        product = Product.objects.get(slug__iexact=kwargs.get('slug'))
        cartitem, created = CartItem.objects.get_or_create(
            owner=self.cart.owner, cart=self.cart, product=product
        )
        if created:
            self.cart.products.add(cartitem)
        calculate_cart(self.cart)
        return HttpResponseRedirect('/cart/')


class DeleteFromCart(CartMixin, View):

    def get(self, request, *args, **kwargs):
        product = Product.objects.get(slug__iexact=kwargs.get('slug'))
        cartitem = CartItem.objects.get(
            owner=self.cart.owner, cart=self.cart, product=product
        )
        self.cart.products.remove(cartitem)
        cartitem.delete()
        calculate_cart(self.cart)
        if self.cart.products.count() == 0:
            return HttpResponseRedirect('/')
        return HttpResponseRedirect('/cart/')


class ChangeProductQty(CartMixin, View):

    def post(self, request, *args, **kwargs):
        product = Product.objects.get(slug__iexact=kwargs.get('slug'))
        cartitem = CartItem.objects.get(
            owner=self.cart.owner, cart=self.cart, product=product
        )
        qty = int(request.POST.get('qty'))
        cartitem.qty = qty
        cartitem.save()
        calculate_cart(self.cart)
        return HttpResponseRedirect('/cart/')

class RegistrationView(CartMixin, View):

    def get(self, request):
        form = RegistrationForm()
        context = {'form': form, 'cart': self.cart}
        return render(request, 'mainapp/registration.html', context)

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.username = form.cleaned_data['username']
            new_user.email = form.cleaned_data['email']
            new_user.first_name = form.cleaned_data['first_name']
            new_user.last_name = form.cleaned_data['last_name']
            new_user.save()
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            Customer.objects.create(
                user=new_user, 
                phone=form.cleaned_data['phone'],
                address=form.cleaned_data['address']
            )
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            login(request, user)
            return HttpResponseRedirect('/')
        context = {'form': form, 'cart': self.cart}
        return render(request, 'mainapp/registration.html', context)


class LoginView(CartMixin, View):

    def get(self, request):
        form = LoginForm()
        context = {'form': form, 'cart': self.cart}
        return render(request, 'mainapp/login.html', context)

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return HttpResponseRedirect('/')
        context = {'form': form, 'cart': self.cart}
        return render(request, 'mainapp/login.html', context)


class SearchProduct(CartMixin, ListView):
    model = Product
    template_name = 'mainapp/search_result.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = Product.objects.filter(
            Q(title__icontains=query) | Q(manufacturer__name__icontains=query)
        )
        return object_list


class StaffBase(CartMixin, View):

    def get(self, request):
        staffs = Staff.objects.all()
        context = {'staffs': staffs, 'cart': self.cart}
        return render(request, 'mainapp/staff_base.html', context)


class StaffRegistration(CartMixin, View):

    def get(self, request):
        form = StaffRegistrationForm()
        context = {'form': form}
        return render(request, 'mainapp/staff_registration.html', context)
    
    def post(self, request):
        form = StaffRegistrationForm(request.POST)
        if form.is_valid():
            new_staff_user = form.save(commit=False)
            new_staff_user.username = form.cleaned_data['username']
            new_staff_user.first_name = form.cleaned_data['first_name']
            new_staff_user.last_name = form.cleaned_data['last_name']
            new_staff_user.email = form.cleaned_data['email']
            new_staff_user.save()
            content_type = ContentType.objects.get_for_model(Order)
            permissions = Permission.objects.filter(content_type=content_type)
            new_staff_user.is_staff = True
            new_staff_user.user_permissions.set(permissions)
            new_staff_user.set_password(form.cleaned_data['password'])
            new_staff_user.save()
            Staff.objects.create(
                user=new_staff_user,
                phone=form.cleaned_data['phone']
            )
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user:
                login(request, user)
                return HttpResponseRedirect('/')
            context = {'form': form, 'cart': self.cart}
            return render(request, 'mainapp/staff_registration.html', context)