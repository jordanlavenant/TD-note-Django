from django.test import TestCase, SimpleTestCase
from django.urls import reverse, resolve
from app.views import Stock, Stocks, StockCreate, StockUpdate, StockDelete
from django.utils import timezone

class StockUrlTest(SimpleTestCase):

    def list_test_view_url_is_resolved(self):
        """
        Tester que l'URL de la vue de liste de stocks est résolue
        """
        url = reverse('stocks')
        self.assertEqual(resolve(url).func.view_class, Stocks)

    def detail_test_view_url_is_resolved(self):
        """
        Tester que l'URL de la vue de détail de stock est résolue
        """
        url = reverse('stock', args=[1])
        self.assertEqual(resolve(url).func.view_class, Stock)

    def create_test_view_url_is_resolved(self):
        """
        Tester que l'URL de la vue de création de stock est résolue
        """
        url = reverse('stock-add')
        self.assertEqual(resolve(url).func.view_class, StockCreate)

    def update_test_view_url_is_resolved(self):
        """
        Tester que l'URL de la vue de mise à jour de stock est résolue
        """
        url = reverse('stock-update', args=[1])
        self.assertEqual(resolve(url).func.view_class, StockUpdate)
    
    def delete_test_view_url_is_resolved(self):
        """
        Tester que l'URL de la vue de suppression de stock est résolue
        """
        url = reverse('stock-delete', args=[1])
        self.assertEqual(resolve(url).func.view_class, StockDelete)

class StockTestUrlResponses(TestCase):

    def create_test_view_status_code(self):
        response = self.client.get(reverse('stock-add'))
        self.assertEqual(response.status_code, 200)

    def list_test_view_status_code(self):
        response = self.client.get(reverse('stocks'))
        self.assertEqual(response.status_code, 200)
    
class StockTestUrlResponsesWithParameters(TestCase):
    
    def setUp(self):
        """Create a stock"""
        self.stock = Stock.objects.create(
            product_id=1,
            provider_id=1,
            quantity=100,
            rate=10.0
        )
    
    def test_detail_view_status_code(self):
        response = self.client.get(reverse('stock', args=[self.stock.id]))
        self.assertEqual(response.status_code, 200)

    def test_detail_view_invalid_status_code(self):
        response = self.client.get(reverse('stock', args=[1000]))
        self.assertEqual(response.status_code, 404)
    
    def test_update_view_status_code(self):
        response = self.client.get(reverse('stock-update', args=[self.stock.id]))
        self.assertEqual(response.status_code, 200)

    def test_delete_view_status_code(self):
        response = self.client.get(reverse('stock-delete', args=[self.stock.id]))
        self.assertEqual(response.status_code, 200)
    
class StockTestUrlRedirect(TestCase):

    def setUp(self):
        """Create a stock"""
        self.stock = Stock.objects.create(
            product_id=1,
            provider_id=1,
            quantity=100,
            rate=10.0
        )
    
    def test_redirect_after_creation(self):
        response = self.client.post(reverse('stock-add'), self.stock.__dict__)
        self.assertEqual(response.status_code, 302)
        new_stock = Stock.objects.latest('id')
        self.assertRedirects(response, reverse('stock', args=[new_stock.id]))

    def test_redirect_after_update(self):
        response = self.client.post(reverse('stock-update', args=[self.stock.id]), self.stock.__dict__)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('stock', args=[self.stock.id]))
    
    def test_redirect_after_deletion(self):
        response = self.client.post(reverse('stock-delete', args=[self.stock.id]), self.stock.__dict__)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('stocks'))