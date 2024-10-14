from django.test import TestCase, SimpleTestCase
from django.urls import reverse, resolve
from app.views import Command, Commands, CommandCreate, CommandUpdate, CommandDelete
from django.utils import timezone

class CommandUrlTest(SimpleTestCase):

    def list_test_view_url_is_resolved(self):
        """
        Tester que l'URL de la vue de liste de commandes est résolue
        """
        url = reverse('commands')
        self.assertEqual(resolve(url).func.view_class, Commands)

    def detail_test_view_url_is_resolved(self):
        """
        Tester que l'URL de la vue de détail de commande est résolue
        """
        url = reverse('command', args=[1])
        self.assertEqual(resolve(url).func.view_class, Command)

    def create_test_view_url_is_resolved(self):
        """
        Tester que l'URL de la vue de création de commande est résolue
        """
        url = reverse('command-add')
        self.assertEqual(resolve(url).func.view_class, CommandCreate)

    def update_test_view_url_is_resolved(self):
        """
        Tester que l'URL de la vue de mise à jour de commande est résolue
        """
        url = reverse('command-update', args=[1])
        self.assertEqual(resolve(url).func.view_class, CommandUpdate)
    
    def delete_test_view_url_is_resolved(self):
        """
        Tester que l'URL de la vue de suppression de commande est résolue
        """
        url = reverse('command-delete', args=[1])
        self.assertEqual(resolve(url).func.view_class, CommandDelete)

class CommandTestUrlResponses(TestCase):

    def create_test_view_status_code(self):
        response = self.client.get(reverse('command-add'))
        self.assertEqual(response.status_code, 200)

    def list_test_view_status_code(self):
        response = self.client.get(reverse('commands'))
        self.assertEqual(response.status_code, 200)
    
class CommandTestUrlResponsesWithParameters(TestCase):
    
    def setUp(self):
        """Create a command"""
        self.command = Command.objects.create(
            product_id=1,
            provider_id=1,
            quantity=10,
            date=timezone.now(),
            status=0
        )
    
    def test_detail_view_status_code(self):
        response = self.client.get(reverse('command', args=[self.command.id]))
        self.assertEqual(response.status_code, 200)

    def test_detail_view_invalid_status_code(self):
        response = self.client.get(reverse('command', args=[1000]))
        self.assertEqual(response.status_code, 404)
    
    def test_update_view_status_code(self):
        response = self.client.get(reverse('command-update', args=[self.command.id]))
        self.assertEqual(response.status_code, 200)

    def test_delete_view_status_code(self):
        response = self.client.get(reverse('command-delete', args=[self.command.id]))
        self.assertEqual(response.status_code, 200)
    
class CommandTestUrlRedirect(TestCase):

    def setUp(self):
        """Create a command"""
        self.command = Command.objects.create(
            product_id=1,
            provider_id=1,
            quantity=10,
            date=timezone.now(),
            status=0
        )
    
    def test_redirect_after_creation(self):
        response = self.client.post(reverse('command-add'), self.command.__dict__)
        self.assertEqual(response.status_code, 302)
        new_command = Command.objects.latest('id')
        self.assertRedirects(response, reverse('command', args=[new_command.id]))

    def test_redirect_after_update(self):
        response = self.client.post(reverse('command-update', args=[self.command.id]), self.command.__dict__)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('command', args=[self.command.id]))
    
    def test_redirect_after_deletion(self):
        response = self.client.post(reverse('command-delete', args=[self.command.id]), self.command.__dict__)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('commands'))