from django.test import TestCase
from django.urls import reverse
from app.models import Provider
from django.contrib.auth.models import User

class ProviderCreateViewTest(TestCase):
    
    def setUp(self):
        """Create a provider and a user"""
        self.provider_data = {
            'name': "Fournisseur A",
            'address': "123 Rue Exemple",
            'phone': "0123456789",
            'email': "fournisseur@example.com"
        }
        self.user = User.objects.create_user(
            username='admin',
            password='admin'
        )

    def test_create_view_get_unauthenticated(self):
        response = self.client.get(reverse('provider-add'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/app/login/?next=/app/providers/add/')

    def test_create_view_get_authenticated(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('provider-add'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'provider/add.html')

    def test_create_view_post_unauthenticated(self):
        response = self.client.post(reverse('provider-add'), self.provider_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/app/login/?next=/app/providers/add/')

    def test_create_view_post_authenticated(self):
        self.client.login(username='admin', password='admin')
        response = self.client.post(reverse('provider-add'), self.provider_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Provider.objects.count(), 1)
        self.assertEqual(Provider.objects.first().name, "Fournisseur A")

class ProviderUpdateViewTest(TestCase):

    def setUp(self):
        """Create a provider and a user"""
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

    def test_update_view_get_unauthenticated(self):
        response = self.client.get(reverse('provider-update', args=[self.provider.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/app/login/?next=/app/providers/{self.provider.id}/update/')

    def test_update_view_get_authenticated(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('provider-update', args=[self.provider.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'provider/update.html')

    def test_update_view_post_unauthenticated(self):
        data = {
            'name': 'Fournisseur A Updated',
            'address': '123 Rue Exemple',
            'phone': '0123456789',
            'email': 'fournisseur@example.com'
        }
        response = self.client.post(reverse('provider-update', args=[self.provider.id]), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/app/login/?next=/app/providers/{self.provider.id}/update/')

    def test_update_view_post_authenticated(self):
        self.client.login(username='admin', password='admin')
        data = {
            'name': 'Fournisseur A Updated',
            'address': '123 Rue Exemple',
            'phone': '0123456789',
            'email': 'fournisseur@example.com'
        }
        response = self.client.post(reverse('provider-update', args=[self.provider.id]), data)
        self.assertEqual(response.status_code, 302)
        self.provider.refresh_from_db()
        self.assertEqual(self.provider.name, 'Fournisseur A Updated')

class ProviderDeleteViewTest(TestCase):

    def setUp(self):
        """Create a provider and a user"""
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

    def test_delete_view_get_unauthenticated(self):
        response = self.client.get(reverse('provider-delete', args=[self.provider.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/app/login/?next=/app/providers/{self.provider.id}/delete/')

    def test_delete_view_get_authenticated(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('provider-delete', args=[self.provider.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'provider/delete.html')

    def test_delete_view_post_unauthenticated(self):
        response = self.client.post(reverse('provider-delete', args=[self.provider.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/app/login/?next=/app/providers/{self.provider.id}/delete/')

    def test_delete_view_post_authenticated(self):
        self.client.login(username='admin', password='admin')
        response = self.client.post(reverse('provider-delete', args=[self.provider.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Provider.objects.count(), 0)