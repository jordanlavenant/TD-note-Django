from django.test import TestCase
from app.forms import ProductForm
from app.models import Product
from django.utils import timezone

class ProductFormTest(TestCase):

    def test_form_valid_data(self):
        """
        Tester que le formulaire est valide avec les données correctes
        """
        form = ProductForm(data={
            'name': "Écran LCD",
            'price_ht': 100,
            'status': 1,
            'date_creation': timezone.make_aware(timezone.datetime(2021, 1, 1, 0, 0, 0))
        })
        self.assertTrue(form.is_valid())

    def test_form_invalid_data(self):
        """
        Tester que le formulaire est invalide avec les données incorrectes
        """
        form = ProductForm(data={
            'name': "",
            'price_ht': "",
            'status': "",
            'date_creation': ""
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 4)
        self.assertEqual(form.errors['name'][0], 'Ce champ est obligatoire.')
        self.assertEqual(form.errors['price_ht'][0], 'Ce champ est obligatoire.')
        self.assertEqual(form.errors['status'][0], 'Ce champ est obligatoire.')
        self.assertEqual(form.errors['date_creation'][0], 'Ce champ est obligatoire.')

    def test_form_save(self):
        """
        Tester que le formulaire sauvegarde les données correctement
        """
        form = ProductForm(data={
            'name': "Écran LCD",
            'price_ht': 100,
            'status': 1,
            'date_creation': timezone.make_aware(timezone.datetime(2021, 1, 1, 0, 0, 0))
        })
        self.assertTrue(form.is_valid())
        product = form.save()
        self.assertEqual(product.name, "Écran LCD")
        self.assertEqual(product.price_ht, 100)
        self.assertEqual(product.status, 1)
        self.assertEqual(product.date_creation, timezone.make_aware(timezone.datetime(2021, 1, 1, 0, 0, 0)))

    def test_form_save_empty_data(self):
        """
        Tester que le formulaire ne sauvegarde pas les données incorrectes
        """
        form = ProductForm(data={
            'name': "",
            'price_ht': "",
            'status': "",
            'date_creation': ""
        })
        self.assertFalse(form.is_valid())