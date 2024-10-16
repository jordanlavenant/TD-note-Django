from django.test import TestCase, SimpleTestCase
from django.urls import reverse, resolve
from app.views import Product, Products, ProductCreate, ProductUpdate, ProductDelete
from django.contrib.auth.models import User

class ProductUrlTest(SimpleTestCase):

    def list_test_view_url_is_resolved(self):
        """
        Tester que l'URL de la vue de liste de produits est résolue
        """
        url = reverse('products')
        self.assertEqual(resolve(url).func.view_class, Products)

    def detail_test_view_url_is_resolved(self):
        """
        Tester que l'URL de la vue de détail de produit est résolue
        """
        url = reverse('product', args=[1])
        self.assertEqual(resolve(url).func.view_class, Product)

    def create_test_view_url_is_resolved(self):
        """
        Tester que l'URL de la vue de création de produit est résolue
        """
        url = reverse('product-add')
        self.assertEqual(resolve(url).func.view_class, ProductCreate)

    def update_test_view_url_is_resolved(self):
        """
        Tester que l'URL de la vue de mise à jour de produit est résolue
        """
        url = reverse('product-update', args=[1])
        self.assertEqual(resolve(url).func.view_class, ProductUpdate)
    
    def delete_test_view_url_is_resolved(self):
        """
        Tester que l'URL de la vue de suppression de produit est résolue
        """
        url = reverse('product-delete', args=[1])
        self.assertEqual(resolve(url).func.view_class, ProductDelete)

class ProductTestUrlResponses(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='admin',
            password='admin'
        )

    def create_test_view_status_code(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('product-add'))
        self.assertEqual(response.status_code, 200)

    def list_test_view_status_code(self):
        response = self.client.get(reverse('products'))
        self.assertEqual(response.status_code, 200)
    
class ProductTestUrlResponsesWithParameters(TestCase):
    
    def setUp(self):
        """Create a product and a user"""
        self.product = Product.objects.create(
            name="Écran LCD",
            price_ht=100,
            status=1,
            stock=100
        )
        self.user = User.objects.create_user(
            username='admin',
            password='admin'
        )
    
    def test_detail_view_status_code(self):
        response = self.client.get(reverse('product', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)

    def test_detail_view_invalid_status_code(self):
        response = self.client.get(reverse('product', args=[1000]))
        self.assertEqual(response.status_code, 404)
    
    def test_update_view_status_code(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('product-update', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)

    def test_delete_view_status_code(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('product-delete', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)
    
class ProductTestUrlRedirect(TestCase):

    def setUp(self):
        """Create a product and a user"""
        self.product = Product.objects.create(
            id='1',
            name="Écran LCD",
            price_ht=100,
            status=1,
            stock=100
        )
        self.user = User.objects.create_user(
            username='admin',
            password='admin'
        )
    
    def test_redirect_after_creation(self):
        self.client.login(username='admin', password='admin')
        response = self.client.post(reverse('product-add'), self.product.__dict__)
        self.assertEqual(response.status_code, 302)
        new_product = Product.objects.latest('id')
        self.assertRedirects(response, reverse('product', args=[new_product.id]))

    def test_redirect_after_update(self):
        self.client.login(username='admin', password='admin')
        response = self.client.post(reverse('product-update', args=[self.product.id]), self.product.__dict__)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('product', args=[self.product.id]))
    
    def test_redirect_after_deletion(self):
        self.client.login(username='admin', password='admin')
        response = self.client.post(reverse('product-delete', args=[self.product.id]), self.product.__dict__)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('products'))

    def test_create_view_redirect_unauthenticated(self):
        response = self.client.get(reverse('product-add'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/app/login/?next=/app/products/add/')

    def test_update_view_redirect_unauthenticated(self):
        response = self.client.get(reverse('product-update', args=[self.product.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/app/login/?next=/app/products/{self.product.id}/update/')

    def test_delete_view_redirect_unauthenticated(self):
        response = self.client.get(reverse('product-delete', args=[self.product.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/app/login/?next=/app/products/{self.product.id}/delete/')