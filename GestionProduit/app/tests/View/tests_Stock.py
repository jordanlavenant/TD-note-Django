from django.test import TestCase
from django.urls import reverse
from app.models import Stock, Product, Provider

class StockCreateViewTest(TestCase):
    
    def setUp(self):
        """Create a product and a provider"""
        self.product = Product.objects.create(
            name="Produit A",
            price_ht=100
        )
        self.provider = Provider.objects.create(
            name="Fournisseur A",
            address="123 Rue Exemple",
            phone="0123456789",
            email="fournisseur@example.com"
        )
    
    def test_create_view_get(self):
        response = self.client.get(reverse('stock-add'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'stock/add.html')

    def test_create_view_post(self):
        response = self.client.post(reverse('stock-add'), {
            'product': self.product.id,
            'provider': self.provider.id,
            'quantity': 50,
            'rate': 10.0
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('stock', args=[Stock.objects.latest('id').id]))

class StockUpdateViewTest(TestCase):
    
    def setUp(self):
        """Create a product, a provider, and a stock"""
        self.product = Product.objects.create(
            name="Produit A",
            price_ht=100
        )
        self.provider = Provider.objects.create(
            name="Fournisseur A",
            address="123 Rue Exemple",
            phone="0123456789",
            email="fournisseur@example.com"
        )
        self.stock = Stock.objects.create(
            product=self.product,
            provider=self.provider,
            quantity=50,
            rate=10.0
        )
    
    def test_update_view_get(self):
        response = self.client.get(reverse('stock-update', args=[self.stock.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'stock/update.html')

    def test_update_view_post(self):
        response = self.client.post(reverse('stock-update', args=[self.stock.id]), {
            'product': self.product.id,
            'provider': self.provider.id,
            'quantity': 100,
            'rate': 15.0
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('stock', args=[self.stock.id]))

class StockDeleteViewTest(TestCase):
    
    def setUp(self):
        """Create a product, a provider, and a stock"""
        self.product = Product.objects.create(
            name="Produit A",
            price_ht=100
        )
        self.provider = Provider.objects.create(
            name="Fournisseur A",
            address="123 Rue Exemple",
            phone="0123456789",
            email="fournisseur@example.com"
        )
        self.stock = Stock.objects.create(
            product=self.product,
            provider=self.provider,
            quantity=50,
            rate=10.0
        )
    
    def test_delete_view_get(self):
        response = self.client.get(reverse('stock-delete', args=[self.stock.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'stock/delete.html')

    def test_delete_view_post(self):
        response = self.client.post(reverse('stock-delete', args=[self.stock.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('stocks'))

class StockDetailViewTest(TestCase):
    
    def setUp(self):
        """Create a product, a provider, and a stock"""
        self.product = Product.objects.create(
            name="Produit A",
            price_ht=100
        )
        self.provider = Provider.objects.create(
            name="Fournisseur A",
            address="123 Rue Exemple",
            phone="0123456789",
            email="fournisseur@example.com"
        )
        self.stock = Stock.objects.create(
            product=self.product,
            provider=self.provider,
            quantity=50,
            rate=10.0
        )
    
    def test_detail_view_get(self):
        response = self.client.get(reverse('stock', args=[self.stock.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'stock/stock.html')