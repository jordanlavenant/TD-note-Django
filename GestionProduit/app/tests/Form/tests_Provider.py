from django.test import TestCase
from app.forms import ProviderForm
from app.models import Provider

class ProviderFormTest(TestCase):

    def test_form_valid_data(self):
        """
        Tester que le formulaire est valide avec les données correctes
        """
        form = ProviderForm(data={
            'name': "Provider A",
            'address': "123 Main St",
            'phone': "123-456-7890",
            'email': "provider@example.com"
        })
        self.assertTrue(form.is_valid())

    def test_form_invalid_data(self):
        """
        Tester que le formulaire est invalide avec les données incorrectes
        """
        form = ProviderForm(data={
            'name': "",
            'address': "",
            'phone': "",
            'email': ""
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 4)
        self.assertEqual(form.errors['name'][0], 'Ce champ est obligatoire.')
        self.assertEqual(form.errors['address'][0], 'Ce champ est obligatoire.')
        self.assertEqual(form.errors['phone'][0], 'Ce champ est obligatoire.')
        self.assertEqual(form.errors['email'][0], 'Ce champ est obligatoire.')

    def test_form_save(self):
        """
        Tester que le formulaire sauvegarde les données correctement
        """
        form = ProviderForm(data={
            'name': "Provider A",
            'address': "123 Main St",
            'phone': "123-456-7890",
            'email': "provider@example.com"
        })
        self.assertTrue(form.is_valid())
        provider = form.save()
        self.assertEqual(provider.name, "Provider A")
        self.assertEqual(provider.address, "123 Main St")
        self.assertEqual(provider.phone, "123-456-7890")
        self.assertEqual(provider.email, "provider@example.com")

    def test_form_save_empty_data(self):
        """
        Tester que le formulaire ne sauvegarde pas les données incorrectes
        """
        form = ProviderForm(data={
            'name': "",
            'address': "",
            'phone': "",
            'email': ""
        })
        self.assertFalse(form.is_valid())