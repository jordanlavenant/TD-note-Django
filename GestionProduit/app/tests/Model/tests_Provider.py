from django.test import TestCase
from app.models import Provider
from django.utils import timezone

class ProviderModelTest(TestCase):
    
    def setUp(self):
        """Create a provider"""
        self.provider = Provider.objects.create(
            name="Provider A",
            address="123 Main St",
            phone="123-456-7890",
            email="provider@example.com"
        )
    
    def test_create_provider(self):
        """Test if the provider is created"""
        self.assertEqual(self.provider.name, "Provider A")
        self.assertEqual(self.provider.address, "123 Main St")
        self.assertEqual(self.provider.phone, "123-456-7890")
        self.assertEqual(self.provider.email, "provider@example.com")

    def test_provider_str(self):
        """Test the string representation of the provider"""
        self.assertEqual(str(self.provider), "Provider A")
    
    def test_update_provider(self):
        """Test if the provider is updated"""
        self.provider.name = "Provider B"
        self.provider.address = "456 Elm St"
        self.provider.phone = "987-654-3210"
        self.provider.email = "providerB@example.com"
        self.provider.save()
        self.assertEqual(self.provider.name, "Provider B")
        self.assertEqual(self.provider.address, "456 Elm St")
        self.assertEqual(self.provider.phone, "987-654-3210")
        self.assertEqual(self.provider.email, "providerB@example.com")

    def test_delete_provider(self):
        """Test if the provider is deleted"""
        self.provider.delete()
        self.assertEqual(Provider.objects.count(), 0)