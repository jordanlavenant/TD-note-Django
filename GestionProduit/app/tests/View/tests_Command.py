from django.test import TestCase
from django.urls import reverse
from app.models import Command, Product, Provider

class CommandCreateViewTest(TestCase):
    
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
        response = self.client.get(reverse('command-add'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'command/add.html')

    def test_create_view_post(self):
        response = self.client.post(reverse('command-add'), {
            'product': self.product.id,
            'provider': self.provider.id,
            'quantity': 10,
            'date': '2023-10-01',
            'status': 0
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('command', args=[Command.objects.latest('id').id]))

class CommandUpdateViewTest(TestCase):
    
    def setUp(self):
        """Create a product, a provider, and a command"""
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
        self.command = Command.objects.create(
            product=self.product,
            provider=self.provider,
            quantity=10,
            date='2023-10-01',
            status=0
        )
    
    def test_update_view_get(self):
        response = self.client.get(reverse('command-update', args=[self.command.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'command/update.html')

    def test_update_view_post(self):
        response = self.client.post(reverse('command-update', args=[self.command.id]), {
            'product': self.product.id,
            'provider': self.provider.id,
            'quantity': 20,
            'date': '2023-10-01',
            'status': 1
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('command', args=[self.command.id]))

class CommandDeleteViewTest(TestCase):
    
    def setUp(self):
        """Create a product, a provider, and a command"""
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
        self.command = Command.objects.create(
            product=self.product,
            provider=self.provider,
            quantity=10,
            date='2023-10-01',
            status=0
        )
    
    def test_delete_view_get(self):
        response = self.client.get(reverse('command-delete', args=[self.command.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'command/delete.html')

    def test_delete_view_post(self):
        response = self.client.post(reverse('command-delete', args=[self.command.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('commands'))

class CommandDetailViewTest(TestCase):
    
    def setUp(self):
        """Create a product, a provider, and a command"""
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
        self.command = Command.objects.create(
            product=self.product,
            provider=self.provider,
            quantity=10,
            date='2023-10-01',
            status=0
        )
    
    def test_detail_view_get(self):
        response = self.client.get(reverse('command', args=[self.command.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'command/command.html')