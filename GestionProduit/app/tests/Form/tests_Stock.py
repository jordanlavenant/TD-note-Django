from django.test import TestCase
from app.forms import StockForm
from app.models import Product, Provider, Stock

class StockFormTest(TestCase):

    def setUp(self):
        self.product = Product.objects.create(name="Product A", price_ht=100)
        self.provider = Provider.objects.create(name="Provider A", address="123 Main St", phone="123-456-7890", email="provider@example.com")

    def test_form_valid_data(self):
        """
        Tester que le formulaire est valide avec les données correctes
        """
        form = StockForm(data={
            'product': self.product.id,
            'provider': self.provider.id,
            'quantity': 10,
            'rate': 5.00
        })
        self.assertTrue(form.is_valid())

    def test_form_invalid_data(self):
        """
        Tester que le formulaire est invalide avec les données incorrectes
        """
        form = StockForm(data={
            'product': "",
            'provider': "",
            'quantity': "",
            'rate': ""
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 4)
        self.assertEqual(form.errors['product'][0], 'Ce champ est obligatoire.')
        self.assertEqual(form.errors['provider'][0], 'Ce champ est obligatoire.')
        self.assertEqual(form.errors['quantity'][0], 'Ce champ est obligatoire.')
        self.assertEqual(form.errors['rate'][0], 'Ce champ est obligatoire.')

    def test_form_save(self):
        """
        Tester que le formulaire sauvegarde les données correctement
        """
        form = StockForm(data={
            'product': self.product.id,
            'provider': self.provider.id,
            'quantity': 10,
            'rate': 5.00
        })
        self.assertTrue(form.is_valid())
        stock = form.save()
        self.assertEqual(stock.product, self.product)
        self.assertEqual(stock.provider, self.provider)
        self.assertEqual(stock.quantity, 10)
        self.assertEqual(stock.rate, 5.00)

    def test_form_save_empty_data(self):
        """
        Tester que le formulaire ne sauvegarde pas les données incorrectes
        """
        form = StockForm(data={
            'product': "",
            'provider': "",
            'quantity': "",
            'rate': ""
        })
        self.assertFalse(form.is_valid())