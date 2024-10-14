from django.test import TestCase
from django.urls import reverse
from app.models import Provider

class ProviderCreateViewTest(TestCase):
    
    def setUp(self):
        """Create a provider"""
        self.provider = Provider.objects.create(
            name="Fournisseur A",
            address="123 Rue Exemple",
            phone="0123456789",
            email="fournisseur@example.com"
        )
    
    def test_create_view_get(self):
        response = self.client.get(reverse('provider-add'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'provider/add.html')

    def test_create_view_post(self):
        response = self.client.post(reverse('provider-add'), {
            'name': 'Fournisseur B',
            'address': '456 Rue Exemple',
            'phone': '0987654321',
            'email': 'fournisseurb@example.com'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('provider', args=[Provider.objects.latest('id').id]))

class ProviderUpdateViewTest(TestCase):
    
    def setUp(self):
        """Create a provider"""
        self.provider = Provider.objects.create(
            name="Fournisseur A",
            address="123 Rue Exemple",
            phone="0123456789",
            email="fournisseur@example.com"
        )
    
    def test_update_view_get(self):
        response = self.client.get(reverse('provider-update', args=[self.provider.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'provider/update.html')

    def test_update_view_post(self):
        response = self.client.post(reverse('provider-update', args=[self.provider.id]), {
            'name': 'Fournisseur A Modifié',
            'address': '123 Rue Exemple Modifié',
            'phone': '0123456789',
            'email': 'fournisseur_modifie@example.com'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('provider', args=[self.provider.id]))

class ProviderDeleteViewTest(TestCase):
    
    def setUp(self):
        """Create a provider"""
        self.provider = Provider.objects.create(
            name="Fournisseur A",
            address="123 Rue Exemple",
            phone="0123456789",
            email="fournisseur@example.com"
        )
    
    def test_delete_view_get(self):
        response = self.client.get(reverse('provider-delete', args=[self.provider.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'provider/delete.html')

    def test_delete_view_post(self):
        response = self.client.post(reverse('provider-delete', args=[self.provider.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('providers'))

class ProviderDetailViewTest(TestCase):
    
    def setUp(self):
        """Create a provider"""
        self.provider = Provider.objects.create(
            name="Fournisseur A",
            address="123 Rue Exemple",
            phone="0123456789",
            email="fournisseur@example.com"
        )
    
    def test_detail_view_get(self):
        response = self.client.get(reverse('provider', args=[self.provider.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'provider/provider.html')