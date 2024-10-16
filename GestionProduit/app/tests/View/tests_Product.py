from django.test import TestCase
from django.urls import reverse
from app.views import Product
from django.contrib.auth.models import User

class ProductCreateViewTest(TestCase):
    
    def setUp(self):
        """Create a product"""
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
    

    def test_create_view_get_unauthenticated(self):
        response = self.client.get(reverse('product-add'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/app/login/?next=/app/products/add/')

    def test_create_view_get_authenticated(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('product-add'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product/add.html')

    def test_create_view_post(self):
        response = self.client.post(reverse('product-add'), self.product.__dict__)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(Product.objects.last().name, "Écran LCD")

class ProductDetailViewTest(TestCase):
        
        def setUp(self):
            """Create a product"""
            self.product = Product.objects.create(
                name="Écran LCD",
                price_ht=100,
                status=1,
                stock=100
            )
        
        def test_detail_view(self):
            response = self.client.get(reverse('product', args=[1]))
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'product/product.html')
            self.assertContains(response, "Écran LCD")


class ProductUpdateViewTest(TestCase):

    def setUp(self):
        """Create a product"""
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

    def test_update_view_get_unauthenticated(self):
        response = self.client.get(reverse('product-update', args=[self.product.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/app/login/?next=/app/products/{self.product.id}/update/')

    def test_update_view_get_authenticated(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('product-update', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product/update.html')


class ProductDeleteViewTest(TestCase):

    def setUp(self):
        """Create a product"""
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

    def test_delete_view_get_unauthenticated(self):
        response = self.client.get(reverse('product-delete', args=[self.product.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/app/login/?next=/app/products/{self.product.id}/delete/')

    def test_delete_view_get_authenticated(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('product-delete', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product/delete.html')


    def test_delete_view_post(self):
        response = self.client.post(reverse('product-delete', args=[1]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Product.objects.count(), 1)

class ProductListViewSet(TestCase):

    def setUp(self):
        """Create a product"""
        self.product = Product.objects.create(
            name="Écran LCD",
            price_ht=100,
            status=1,
            stock=100
        )

    def test_list_view(self):
        response = self.client.get(reverse('products'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product/products.html')
        self.assertContains(response, "Écran LCD")