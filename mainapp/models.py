from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify

User = get_user_model()

def upload_image_function(instance, filename):
    if hasattr(instance, 'title'):
        return "catalog/{}/{}".format(instance.title, filename)
    return "catalog/{}/{}".format(instance.phone.title, filename)

def generate_slug(s):
    new_slug = slugify(s)
    return new_slug


class Manufacturer(models.Model):
    name = models.CharField(max_length=100, verbose_name="Производитель")
    slug = models.SlugField(blank=True, unique=True)
    logo = models.ImageField(upload_to="logos/", verbose_name="Лого производителя")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = generate_slug(self.name)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('manufacturer_category', kwargs={'slug': self.slug})


class Product(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название смартфона")
    manufacturer = models.ForeignKey(Manufacturer, verbose_name="Производитель", on_delete=models.CASCADE)
    description = models.TextField(blank=True, verbose_name="Описание")
    slug = models.SlugField(blank=True, unique=True)
    image = models.ImageField(upload_to=upload_image_function,verbose_name="Изображение смартфона")
    all_images = models.ManyToManyField('Images', blank=True, verbose_name='Галерея изображений')
    price = models.PositiveIntegerField(verbose_name="Цена")
    prime_cost = models.PositiveIntegerField(verbose_name="Себестоимость")
    features = models.ManyToManyField('features_app.Feature', blank=True, verbose_name="Характеристики", related_name='products')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = generate_slug(self.title)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'slug': self.slug, 'manufacturer': self.manufacturer.slug})


class Images(models.Model):
    phone = models.ForeignKey(Product, max_length=100, verbose_name='Название товара', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=upload_image_function, blank=True, verbose_name="Изображения")

    def __str__(self):
        return "Изображение для {}".format(self.phone.title)


class Customer(models.Model):
    
    user = models.OneToOneField(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    phone = models.CharField(max_length=25, blank=True, verbose_name='Номер телефона')
    address = models.CharField(max_length=255, blank=True, verbose_name='Адрес')
    orders = models.ManyToManyField('Order', verbose_name='Заказы покупателя', blank=True, related_name='related_customer')

    def __str__(self):
        return "Покупатель: {} {}".format(self.user.first_name, self.user.last_name)


class Cart(models.Model):
    owner = models.ForeignKey(Customer, null=True, verbose_name="Покупатель", on_delete=models.CASCADE)
    products = models.ManyToManyField('CartItem', blank=True, verbose_name="Товары в корзине", default=0, related_name="related_cart")
    total_price = models.PositiveIntegerField(default=0, verbose_name="Общая стоимость")
    for_anonymous = models.BooleanField(default=False)

    def __str__(self):
        return "Корзина номер {} ".format(str(self.id))


class CartItem(models.Model):
    owner = models.ForeignKey(Customer, verbose_name="Покупатель", on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, verbose_name="Корзина", on_delete=models.CASCADE, related_name="related_products")
    product = models.ForeignKey(Product, verbose_name="Товар", on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=1, verbose_name="Количество товара")
    sale_price = models.PositiveIntegerField(default=0, verbose_name="Цена товара в момент покупки")
    total_price = models.PositiveIntegerField(default=0, verbose_name="Общая стоимость")

    def __str__(self):
        return "Продукт: {} для корзины {}".format(self.product.title, str(self.cart.id))

    def save(self, *args, **kwargs):
        self.total_price = self.qty * self.product.price
        super().save(*args, **kwargs)


class Staff(models.Model):
    
    user = models.OneToOneField(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    phone = models.CharField(max_length=25, verbose_name='Номер телефона')
    orders = models.ManyToManyField('Order', verbose_name='Заказы покупателя', blank=True, related_name='related_staff')

    def __str__(self):
        return "Оператор-продавец {}".format(self.user.first_name, self.user.last_name)


class Order(models.Model):
    
    STATUS_NEW = 'new'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_READY = 'is_ready'
    STATUS_COMPLETED = 'completed'

    ORDER_TYPE_SELF = 'self'
    ORDER_TYPE_DELIVERY = 'delivery'

    PAYMENT_TYPE_CASH = 'cash'
    PAYMENT_TYPE_CARD = 'card'

    STATUS_CHOICES = (
        (STATUS_NEW, 'Новый заказ'),
        (STATUS_IN_PROGRESS, 'Заказ в обработке'),
        (STATUS_READY, 'Заказ готов'),
        (STATUS_COMPLETED, 'Заказ выполнен')
    )

    ORDER_TYPE_CHOICES = (
        (ORDER_TYPE_SELF, 'Самовывоз'),
        (ORDER_TYPE_DELIVERY, 'Доставка')
    )

    PAYMENT_TYPE_CHOICES = (
        (PAYMENT_TYPE_CASH, 'Наличные'),
        (PAYMENT_TYPE_CARD, 'Банковская карта')
    )

    customer = models.ForeignKey(Customer, verbose_name="Заказчик", on_delete=models.CASCADE, related_name="related_order")
    staff = models.ForeignKey('Staff', verbose_name="Оператор-продавец", on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, verbose_name="Корзина", on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, verbose_name="Имя")
    last_name = models.CharField(max_length=50, verbose_name="Фамилия")
    phone = models.CharField(max_length=10, verbose_name="Номер телефона")
    address = models.CharField(max_length=100, verbose_name="Адрес")
    total_price = models.PositiveIntegerField(verbose_name="Общая стоимость")
    order_type = models.CharField(
        max_length=100, choices=ORDER_TYPE_CHOICES, verbose_name="Способ доставки", default=ORDER_TYPE_DELIVERY
        )
    status = models.CharField(
        max_length=100, choices=STATUS_CHOICES, verbose_name="Состояние заказа", default=STATUS_NEW
        )
    payment_type = models.CharField(
        max_length=100, choices=PAYMENT_TYPE_CHOICES, verbose_name="Способ оплаты", default=PAYMENT_TYPE_CASH
        )
    order_date = models.DateTimeField(verbose_name="Дата заказа", default=timezone.now)
    total_price = models.PositiveIntegerField(verbose_name="Общая стоимость")

    def __str__(self):
        return str(self.id)


class OrderDetail(models.Model):
    order = models.ForeignKey('Order', verbose_name="Заказ", on_delete=models.CASCADE)
    product = models.ForeignKey('Product', verbose_name="Товар", on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=1, verbose_name="Количество товара")
    sale_price = models.PositiveIntegerField(verbose_name="Цена товара в момент покупки")
    total_price = models.PositiveIntegerField(verbose_name="Общая стоимость")

    def __str__(self):
        return "Продукт: {} для заказа {}".format(self.product.title, str(self.order.id))