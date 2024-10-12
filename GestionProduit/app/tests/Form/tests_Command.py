from django.test import TestCase
from app.forms import CommandForm
from app.models import Product, Provider, Command
from django.utils import timezone

class CommandFormTest(TestCase):

    def setUp(self):
        self.product = Product.objects.create(name="Product A", price_ht=100)
        self.provider = Provider.objects.create(name="Provider A", address="123 Main St", phone="123-456-7890", email="provider@example.com")

    def test_form_valid_data(self):
        """
        Tester que le formulaire est valide avec les données correctes
        """
        form = CommandForm(data={
            'product': self.product.id,
            'provider': self.provider.id,
            'quantity': 10,
            'date': timezone.now(),
            'status': 1
        })
        self.assertTrue(form.is_valid())

    def test_form_invalid_data(self):
        """
        Tester que le formulaire est invalide avec les données incorrectes
        """
        form = CommandForm(data={
            'product': "",
            'provider': "",
            'quantity': "",
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 3)
        self.assertEqual(form.errors['product'][0], 'Ce champ est obligatoire.')
        self.assertEqual(form.errors['provider'][0], 'Ce champ est obligatoire.')
        self.assertEqual(form.errors['quantity'][0], 'Ce champ est obligatoire.')
    def test_form_save(self):
        """
        Tester que le formulaire sauvegarde les données correctement
        """
        form = CommandForm(data={
            'product': self.product.id,
            'provider': self.provider.id,
            'quantity': 10,
            'date': timezone.now(),
            'status': 0
        })
        self.assertTrue(form.is_valid())
        command = form.save()
        self.assertEqual(command.product, self.product)
        self.assertEqual(command.provider, self.provider)
        self.assertEqual(command.quantity, 10)
        self.assertEqual(command.status, 0)

    def test_form_save_empty_data(self):
        """
        Tester que le formulaire ne sauvegarde pas les données incorrectes
        """
        form = CommandForm(data={
            'product': "",
            'provider': "",
            'quantity': "",
            'date': "",
            'status': ""
        })
        self.assertFalse(form.is_valid())