from django.test import TestCase
from django.urls import reverse
from app.models import Command, Product, Provider
from django.contrib.auth.models import User

class CommandCreateViewTest(TestCase):
    
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
        self.command_data = {
            'product': self.product.id,
            'provider': self.provider.id,
            'quantity': 10,
            'date': '2023-10-01',
            'status': 0
        }

    def test_create_view_get_unauthenticated(self):
        response = self.client.get(reverse('command-add'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/app/login/?next=/app/commands/add/')

    def test_create_view_get_authenticated(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('command-add'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'command/add.html')

    def test_create_view_post_unauthenticated(self):
        response = self.client.post(reverse('command-add'), self.command_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/app/login/?next=/app/commands/add/')

    def test_create_view_post_authenticated(self):
        self.client.login(username='admin', password='admin')
        response = self.client.post(reverse('command-add'), self.command_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('command', args=[Command.objects.latest('id').id]))

class CommandUpdateViewTest(TestCase):
    
    def setUp(self):
        """Create a product, a provider, a command, and a user"""
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
        self.user = User.objects.create_user(
            username='admin',
            password='admin'
        )

    def test_update_view_get_unauthenticated(self):
        response = self.client.get(reverse('command-update', args=[self.command.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/app/login/?next=/app/commands/{self.command.id}/update/')

    def test_update_view_get_authenticated(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('command-update', args=[self.command.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'command/update.html')

    def test_update_view_post_unauthenticated(self):
        data = {
            'product': self.product.id,
            'provider': self.provider.id,
            'quantity': 20,
            'date': '2023-10-01',
            'status': 1
        }
        response = self.client.post(reverse('command-update', args=[self.command.id]), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/app/login/?next=/app/commands/{self.command.id}/update/')

    def test_update_view_post_authenticated(self):
        self.client.login(username='admin', password='admin')
        data = {
            'product': self.product.id,
            'provider': self.provider.id,
            'quantity': 20,
            'date': '2023-10-01',
            'status': 1
        }
        response = self.client.post(reverse('command-update', args=[self.command.id]), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('command', args=[self.command.id]))

class CommandDeleteViewTest(TestCase):
    
    def setUp(self):
        """Create a product, a provider, a command, and a user"""
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
        self.user = User.objects.create_user(
            username='admin',
            password='admin'
        )

    def test_delete_view_get_unauthenticated(self):
        response = self.client.get(reverse('command-delete', args=[self.command.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/app/login/?next=/app/commands/{self.command.id}/delete/')

    def test_delete_view_get_authenticated(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('command-delete', args=[self.command.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'command/delete.html')

    def test_delete_view_post_unauthenticated(self):
        response = self.client.post(reverse('command-delete', args=[self.command.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/app/login/?next=/app/commands/{self.command.id}/delete/')

    def test_delete_view_post_authenticated(self):
        self.client.login(username='admin', password='admin')
        response = self.client.post(reverse('command-delete', args=[self.command.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('commands'))
        self.assertEqual(Command.objects.count(), 0)

class CommandDetailViewTest(TestCase):
    
    def setUp(self):
        """Create a product, a provider, a command, and a user"""
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