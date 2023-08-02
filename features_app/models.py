from django.db import models

class Feature(models.Model):
    name = models.CharField(max_length=50, verbose_name="Название характеристики")
    product = models.ForeignKey("mainapp.Product", verbose_name="Смартфон", on_delete=models.CASCADE)
    unit = models.CharField(max_length=30, blank=True, null=True, verbose_name="Единица измерения")
    value = models.CharField(max_length=100, verbose_name="Значение")

    def __str__(self):
        return "Характеристика {} для {}. Значение - {} {}".format(self.name, self.product.title, self.value, self.unit)