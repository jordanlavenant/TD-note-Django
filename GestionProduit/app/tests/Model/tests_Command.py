from django.test import TestCase
from app.models import Product, Provider, Command, Stock
from django.utils import timezone

class CommandModelTest(TestCase):
    
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
        self.command = Command.objects.create(
            product=self.product,
            provider=self.provider,
            quantity=10,
            date=timezone.now(),
            status=0
        )
    
    def test_create_command(self):
        """Test if the command is created"""
        self.assertEqual(self.command.product.name, "Écran LCD")
        self.assertEqual(self.command.provider.name, "Provider A")
        self.assertEqual(self.command.quantity, 10)
        self.assertEqual(self.command.status, 0)

    def test_command_str(self):
        """Test the string representation of the command"""
        self.assertEqual(str(self.command), "Écran LCD Provider A")
    
    def test_update_command(self):
        """Test if the command is updated"""
        self.command.quantity = 20
        self.command.status = 1
        self.command.save()
        self.assertEqual(self.command.quantity, 20)
        self.assertEqual(self.command.status, 1)

    def test_delete_command(self):
        """Test if the command is deleted"""
        self.command.delete()
        self.assertEqual(Command.objects.count(), 0)