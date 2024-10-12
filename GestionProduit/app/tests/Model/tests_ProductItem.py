from django.test import TestCase
from app.models import Product, Provider, ProductItem
from django.utils import timezone

class ProductItemModelTest(TestCase):
    
    def setUp(self):
        """Create a product and a provider"""
        self.product = Product.objects.create(
            name="Écran LCD",
            price_ht=100,
            status=1,
            date_creation=timezone.now()
        )
        self.provider = Provider.objects.create(
            name="Provider A",
            address="123 Main St",
            phone="123-456-7890",
            email="provider@example.com"
        )
        self.product_item = ProductItem.objects.create(
            product=self.product,
            provider=self.provider,
            quantity=10,
            rate=15
        )
    
    def test_create_product_item(self):
        """Test if the product item is created"""
        self.assertEqual(self.product_item.product.name, "Écran LCD")
        self.assertEqual(self.product_item.provider.name, "Provider A")
        self.assertEqual(self.product_item.quantity, 10)
        self.assertEqual(self.product_item.rate, 15)

    def test_product_item_str(self):
        """Test the string representation of the product item"""
        self.assertEqual(str(self.product_item), "Écran LCD - Provider A")
    
    def test_update_product_item(self):
        """Test if the product item is updated"""
        self.product_item.quantity = 20
        self.product_item.rate = 20
        self.product_item.save()
        self.assertEqual(self.product_item.quantity, 20)
        self.assertEqual(self.product_item.rate, 20)

    def test_delete_product_item(self):
        """Test if the product item is deleted"""
        self.product_item.delete()
        self.assertEqual(ProductItem.objects.count(), 0)