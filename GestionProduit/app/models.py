from django.db import models
import django.utils.timezone as timezone

# Create your models here.

PRODUCT_STATUS = (
    (0, 'Hors ligne'),
    (1, 'En ligne'),
    (2, 'En rupture de stock')              
)

COMMAND_STATUS = (
    (0, 'En préparation'),
    (1, "Passée"),
    (2, 'Reçue'),
    (3, 'Annulée')              
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

    name          = models.CharField(max_length=100, verbose_name="Nom")
    price_ht      = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Prix unitaire HT")
    status        = models.SmallIntegerField(choices=PRODUCT_STATUS, default=0, verbose_name="Statut")
    date_creation = models.DateTimeField(verbose_name="Date création", default=timezone.now()) 

    def __str__(self):
        return "{0}".format(self.name)
    
    def get_status(self):
        return PRODUCT_STATUS[self.status][1]

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
    
    def get_stocks(self):
        return Stock.objects.filter(provider=self)
    
class Attribute(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class ProductItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_items')
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, related_name='product_items')
    quantity = models.IntegerField(default=0, verbose_name="Quantité")
    rate = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, verbose_name="Marge")
    attributes = models.ManyToManyField('Attribute', blank=True)

    class Meta:
        unique_together = ('product', 'provider')

    def __str__(self):
        return "{0} - {1}".format(self.product.name, self.provider.name)

    def get_price_ttc(self):
        return self.product.price_ht * (1 + self.rate / 100)

class Stock(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    rate = models.DecimalField(max_digits=4, decimal_places=2, default=0.00, verbose_name="Marge")
    quantity = models.IntegerField(default=0, verbose_name="Quantité")

    class Meta:
        unique_together = ('product', 'provider')

    def __str__(self):
        return "{0} {1}".format(self.product, self.provider)
    
    def get_price_ttc(self):
        return self.product.price_ht * (1 + self.rate / 100)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        product_item, created = ProductItem.objects.get_or_create(
            product=self.product,
            provider=self.provider,
            defaults={'quantity': self.quantity, 'rate': self.rate}
        )
        if not created:
            product_item.quantity = self.quantity
            product_item.rate = self.rate
            product_item.save()

class Command(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Produit")
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, verbose_name="Fournisseur")
    quantity = models.IntegerField(verbose_name="Quantité")
    date = models.DateTimeField(blank=True, verbose_name="Date de commande", default=timezone.now())
    status = models.SmallIntegerField(choices=COMMAND_STATUS, default=0, verbose_name="Statut")

    def __str__(self):
        return "{0} {1}".format(self.product, self.provider)
    
    def get_status(self):
        return COMMAND_STATUS[self.status][1]

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.status == 2:
            stock, created = Stock.objects.get_or_create(
                product=self.product,
                provider=self.provider,
                defaults={'quantity': 0, 'rate': 0}
            )
            stock.quantity += self.quantity
            stock.save()

            product_item, created = ProductItem.objects.get_or_create(
                product=self.product,
                provider=self.provider,
                defaults={'quantity': 0, 'rate': 0}
            )
            product_item.save()