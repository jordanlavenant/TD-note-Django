from django.db import models
import django.utils.timezone as timezone

# Create your models here.

PRODUCT_STATUS = (
    (0, 'Offline'),
    (1, 'Online'),
    (2, 'Out of stock')              
)

COMMAND_STATUS = (
    (0, 'Pending'),
    (1, 'Delivered'),
    (2, 'Canceled')              
)

class Status(models.Model):
    numero  = models.IntegerField()
    libelle = models.CharField(max_length=100)

    def __str__(self):
        return "{0} {1}".format(self.numero, self.libelle)

class Product(models.Model):

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

    name          = models.CharField(max_length=100)
    price_ht      = models.DecimalField(max_digits=8, decimal_places=2,  null=True, blank=True, verbose_name="Prix unitaire HT")
    status        = models.SmallIntegerField(choices=PRODUCT_STATUS, default=0)
    date_creation = models.DateTimeField(blank=True, verbose_name="Date création", default=timezone.now()) 

    def __str__(self):
        return "{0}".format(self.name)

class Provider(models.Model):
    class Meta:
        verbose_name = "Provider"
        verbose_name_plural = "Providers"

    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)

    def __str__(self):
        return "{0}".format(self.name)
    
class Stock(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    rate = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, verbose_name="Marge")
    quantity = models.IntegerField(default=0, verbose_name="Quantité")

    class Meta:
        unique_together = ('product', 'provider')

    def __str__(self):
        return "{0} {1}".format(self.product, self.provider)

class Command(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    date = models.DateTimeField(blank=True, verbose_name="Date de commande", default=timezone.now())
    status = models.SmallIntegerField(choices=COMMAND_STATUS, default=0)

    def __str__(self):
        return "{0} {1}".format(self.product, self.provider)