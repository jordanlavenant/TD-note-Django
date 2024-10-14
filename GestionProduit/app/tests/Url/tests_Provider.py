from django.test import TestCase, SimpleTestCase
from django.urls import reverse, resolve
from app.views import Provider, Providers, ProviderCreate, ProviderUpdate, ProviderDelete
from django.utils import timezone

class ProviderUrlTest(SimpleTestCase):

    def list_test_view_url_is_resolved(self):
        """
        Tester que l'URL de la vue de liste de fournisseurs est résolue
        """
        url = reverse('providers')
        self.assertEqual(resolve(url).func.view_class, Providers)

    def detail_test_view_url_is_resolved(self):
        """
        Tester que l'URL de la vue de détail de fournisseur est résolue
        """
        url = reverse('provider', args=[1])
        self.assertEqual(resolve(url).func.view_class, Provider)

    def create_test_view_url_is_resolved(self):
        """
        Tester que l'URL de la vue de création de fournisseur est résolue
        """
        url = reverse('provider-add')
        self.assertEqual(resolve(url).func.view_class, ProviderCreate)

    def update_test_view_url_is_resolved(self):
        """
        Tester que l'URL de la vue de mise à jour de fournisseur est résolue
        """
        url = reverse('provider-update', args=[1])
        self.assertEqual(resolve(url).func.view_class, ProviderUpdate)
    
    def delete_test_view_url_is_resolved(self):
        """
        Tester que l'URL de la vue de suppression de fournisseur est résolue
        """
        url = reverse('provider-delete', args=[1])
        self.assertEqual(resolve(url).func.view_class, ProviderDelete)

class ProviderTestUrlResponses(TestCase):

    def create_test_view_status_code(self):
        response = self.client.get(reverse('provider-add'))
        self.assertEqual(response.status_code, 200)

    def list_test_view_status_code(self):
        response = self.client.get(reverse('providers'))
        self.assertEqual(response.status_code, 200)
    
class ProviderTestUrlResponsesWithParameters(TestCase):
    
    def setUp(self):
        """Create a provider"""
        self.provider = Provider.objects.create(
            name="Fournisseur A",
            address="123 Rue Exemple",
            phone="0123456789",
            email="fournisseur@example.com"
        )
    
    def test_detail_view_status_code(self):
        response = self.client.get(reverse('provider', args=[self.provider.id]))
        self.assertEqual(response.status_code, 200)

    def test_detail_view_invalid_status_code(self):
        response = self.client.get(reverse('provider', args=[1000]))
        self.assertEqual(response.status_code, 404)
    
    def test_update_view_status_code(self):
        response = self.client.get(reverse('provider-update', args=[self.provider.id]))
        self.assertEqual(response.status_code, 200)

    def test_delete_view_status_code(self):
        response = self.client.get(reverse('provider-delete', args=[self.provider.id]))
        self.assertEqual(response.status_code, 200)
    
class ProviderTestUrlRedirect(TestCase):

    def setUp(self):
        """Create a provider"""
        self.provider = Provider.objects.create(
            id='1',
            name="Fournisseur A",
            address="123 Rue Exemple",
            phone="0123456789",
            email="fournisseur@example.com"
        )
    
    def test_redirect_after_creation(self):
        response = self.client.post(reverse('provider-add'), self.provider.__dict__)
        self.assertEqual(response.status_code, 302)
        new_provider = Provider.objects.latest('id')
        self.assertRedirects(response, reverse('provider', args=[new_provider.id]))

    def test_redirect_after_update(self):
        response = self.client.post(reverse('provider-update', args=[self.provider.id]), self.provider.__dict__)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('provider', args=[self.provider.id]))
    
    def test_redirect_after_deletion(self):
        response = self.client.post(reverse('provider-delete', args=[self.provider.id]), self.provider.__dict__)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('providers'))