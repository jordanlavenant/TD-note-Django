from django.test import TestCase
from app.models import Product, Provider, Stock
from django.utils import timezone

class StockModelTest(TestCase):
    
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
        self.stock = Stock.objects.create(
            product=self.product,
            provider=self.provider,
            rate=10,
            quantity=50
        )
    
    def test_create_stock(self):
        """Test if the stock is created"""
        self.assertEqual(self.stock.product.name, "Écran LCD")
        self.assertEqual(self.stock.provider.name, "Provider A")
        self.assertEqual(self.stock.rate, 10)
        self.assertEqual(self.stock.quantity, 50)

    def test_stock_str(self):
        """Test the string representation of the stock"""
        self.assertEqual(str(self.stock), "Écran LCD Provider A")
    
    def test_update_stock(self):
        """Test if the stock is updated"""
        self.stock.rate = 15
        self.stock.quantity = 100
        self.stock.save()
        self.assertEqual(self.stock.rate, 15)
        self.assertEqual(self.stock.quantity, 100)

    def test_delete_stock(self):
        """Test if the stock is deleted"""
        self.stock.delete()
        self.assertEqual(Stock.objects.count(), 0)