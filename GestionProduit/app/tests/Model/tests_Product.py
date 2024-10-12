from django.test import TestCase
from app.models import Product
from django.utils import timezone

class ProductModelTest(TestCase):
    
    def setUp(self):
        """Create a product"""
        self.product = Product.objects.create(
            name="Écran LCD",
            price_ht=100,
            status=1,
            date_creation=timezone.make_aware(timezone.datetime(2021, 1, 1, 0, 0, 0))
        )
    
    def test_create_product(self):
        """Test if the product is created"""
        self.assertEqual(self.product.name, "Écran LCD")
        self.assertEqual(self.product.price_ht, 100)
        self.assertEqual(self.product.status, 1)
        self.assertEqual(self.product.date_creation, timezone.make_aware(timezone.datetime(2021, 1, 1, 0, 0, 0)))

    def test_product_str(self):
        """Test the string representation of the product"""
        self.assertEqual(str(self.product), "Écran LCD")
    
    def test_update_product(self):
        """Test if the product is updated"""
        self.product.name = "Écran LED"
        self.product.price_ht = 200
        self.product.status = 0
        self.product.date_creation = timezone.make_aware(timezone.datetime(2021, 1, 1, 0, 0, 0))
        self.product.save()
        self.assertEqual(self.product.name, "Écran LED")
        self.assertEqual(self.product.price_ht, 200)
        self.assertEqual(self.product.status, 0)
        self.assertEqual(self.product.date_creation, timezone.make_aware(timezone.datetime(2021, 1, 1, 0, 0, 0)))

    def test_delete_product(self):
        """Test if the product is deleted"""
        self.product.delete()
        self.assertEqual(Product.objects.count(), 0)