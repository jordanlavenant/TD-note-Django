from django.test import TestCase
from django.urls import reverse
from app.models import Stock, Product, Provider
from django.contrib.auth.models import User

class StockCreateViewTest(TestCase):
    
    def setUp(self):
        """Create a product, a provider, and a user"""
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
        self.user = User.objects.create_user(
            username='admin',
            password='admin'
        )
        self.stock_data = {
            'product': self.product.id,
            'provider': self.provider.id,
            'quantity': 50,
            'rate': 10
        }

    def test_create_view_get_unauthenticated(self):
        response = self.client.get(reverse('stock-add'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/app/login/?next=/app/stocks/add/')

    def test_create_view_get_authenticated(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('stock-add'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'stock/add.html')

    def test_create_view_post_unauthenticated(self):
        response = self.client.post(reverse('stock-add'), self.stock_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/app/login/?next=/app/stocks/add/')

    def test_create_view_post_authenticated(self):
        self.client.login(username='admin', password='admin')
        response = self.client.post(reverse('stock-add'), self.stock_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Stock.objects.count(), 1)
        self.assertEqual(Stock.objects.first().quantity, 50)

class StockUpdateViewTest(TestCase):

    def setUp(self):
        """Create a product, a provider, a stock, and a user"""
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
            rate=10
        )
        self.user = User.objects.create_user(
            username='admin',
            password='admin'
        )

    def test_update_view_get_unauthenticated(self):
        response = self.client.get(reverse('stock-update', args=[self.stock.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/app/login/?next=/app/stocks/{self.stock.id}/update/')

    def test_update_view_get_authenticated(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('stock-update', args=[self.stock.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'stock/update.html')

    def test_update_view_post_unauthenticated(self):
        data = {
            'product': self.product.id,
            'provider': self.provider.id,
            'quantity': 100,
            'rate': 20
        }
        response = self.client.post(reverse('stock-update', args=[self.stock.id]), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/app/login/?next=/app/stocks/{self.stock.id}/update/')

    def test_update_view_post_authenticated(self):
        self.client.login(username='admin', password='admin')
        data = {
            'product': self.product.id,
            'provider': self.provider.id,
            'quantity': 100,
            'rate': 20
        }
        response = self.client.post(reverse('stock-update', args=[self.stock.id]), data)
        self.assertEqual(response.status_code, 302)
        self.stock.refresh_from_db()
        self.assertEqual(self.stock.quantity, 100)
        self.assertEqual(self.stock.rate, 20)

class StockDeleteViewTest(TestCase):

    def setUp(self):
        """Create a product, a provider, a stock, and a user"""
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
            rate=10
        )
        self.user = User.objects.create_user(
            username='admin',
            password='admin'
        )

    def test_delete_view_get_unauthenticated(self):
        response = self.client.get(reverse('stock-delete', args=[self.stock.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/app/login/?next=/app/stocks/{self.stock.id}/delete/')

    def test_delete_view_get_authenticated(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('stock-delete', args=[self.stock.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'stock/delete.html')

    def test_delete_view_post_unauthenticated(self):
        response = self.client.post(reverse('stock-delete', args=[self.stock.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/app/login/?next=/app/stocks/{self.stock.id}/delete/')

    def test_delete_view_post_authenticated(self):
        self.client.login(username='admin', password='admin')
        response = self.client.post(reverse('stock-delete', args=[self.stock.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Stock.objects.count(), 0)