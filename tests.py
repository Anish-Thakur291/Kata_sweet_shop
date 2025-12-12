from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from decimal import Decimal
from .models import Sweet


class UserAuthTests(APITestCase):
    def setUp(self):
        self.register_url = '/api/auth/register'
        self.login_url = '/api/auth/login'
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123',
            'password_confirm': 'testpass123'
        }

    def test_user_registration_success(self):
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('tokens', response.data)
        self.assertIn('access', response.data['tokens'])
        self.assertIn('refresh', response.data['tokens'])
        self.assertEqual(response.data['user']['username'], 'testuser')

    def test_user_registration_password_mismatch(self):
        data = self.user_data.copy()
        data['password_confirm'] = 'wrongpassword'
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_registration_short_password(self):
        data = self.user_data.copy()
        data['password'] = 'short'
        data['password_confirm'] = 'short'
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_login_success(self):
        User.objects.create_user(username='testuser', password='testpass123')
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'testpass123'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('tokens', response.data)

    def test_user_login_invalid_credentials(self):
        response = self.client.post(self.login_url, {
            'username': 'nonexistent',
            'password': 'wrongpass'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class SweetModelTests(TestCase):
    def test_sweet_creation(self):
        sweet = Sweet.objects.create(
            name='Chocolate Bar',
            description='Delicious milk chocolate',
            category='chocolate',
            price=Decimal('2.50'),
            quantity=100
        )
        self.assertEqual(str(sweet), 'Chocolate Bar')
        self.assertEqual(sweet.category, 'chocolate')


class SweetAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.admin = User.objects.create_superuser(username='admin', password='adminpass123')
        self.sweet = Sweet.objects.create(
            name='Chocolate Bar',
            description='Delicious milk chocolate',
            category='chocolate',
            price=Decimal('2.50'),
            quantity=100
        )
        self.sweets_url = '/api/sweets'

    def authenticate_user(self):
        response = self.client.post('/api/auth/login', {
            'username': 'testuser',
            'password': 'testpass123'
        }, format='json')
        token = response.data['tokens']['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    def authenticate_admin(self):
        response = self.client.post('/api/auth/login', {
            'username': 'admin',
            'password': 'adminpass123'
        }, format='json')
        token = response.data['tokens']['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    def test_list_sweets_unauthenticated(self):
        response = self.client.get(self.sweets_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_sweet_unauthenticated(self):
        data = {'name': 'Test', 'category': 'candy', 'price': '1.99', 'quantity': 50}
        response = self.client.post(self.sweets_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_sweet_unauthenticated(self):
        url = f'{self.sweets_url}/{self.sweet.id}'
        data = {'name': 'Hacked', 'price': '0.00', 'category': 'candy', 'quantity': 999}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_sweet_unauthenticated(self):
        url = f'{self.sweets_url}/{self.sweet.id}'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_sweets_authenticated(self):
        self.authenticate_user()
        response = self.client.get(self.sweets_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_sweet_admin(self):
        self.authenticate_admin()
        data = {
            'name': 'Gummy Bears',
            'description': 'Colorful gummy candies',
            'category': 'candy',
            'price': '1.99',
            'quantity': 50
        }
        response = self.client.post(self.sweets_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Sweet.objects.count(), 2)

    def test_create_sweet_regular_user_forbidden(self):
        self.authenticate_user()
        data = {
            'name': 'Gummy Bears',
            'description': 'Colorful gummy candies',
            'category': 'candy',
            'price': '1.99',
            'quantity': 50
        }
        response = self.client.post(self.sweets_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_sweet_admin(self):
        self.authenticate_admin()
        url = f'{self.sweets_url}/{self.sweet.id}'
        data = {'name': 'Updated Chocolate Bar', 'price': '3.00', 'category': 'chocolate', 'quantity': 100}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.sweet.refresh_from_db()
        self.assertEqual(self.sweet.name, 'Updated Chocolate Bar')

    def test_update_sweet_regular_user_forbidden(self):
        self.authenticate_user()
        url = f'{self.sweets_url}/{self.sweet.id}'
        data = {'name': 'Updated Chocolate Bar', 'price': '3.00', 'category': 'chocolate', 'quantity': 100}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_sweet_regular_user_forbidden(self):
        self.authenticate_user()
        url = f'{self.sweets_url}/{self.sweet.id}'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_sweet_admin_success(self):
        self.authenticate_admin()
        url = f'{self.sweets_url}/{self.sweet.id}'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Sweet.objects.count(), 0)


class SweetSearchTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        Sweet.objects.create(name='Chocolate Bar', category='chocolate', price=Decimal('2.50'), quantity=100)
        Sweet.objects.create(name='Gummy Bears', category='candy', price=Decimal('1.50'), quantity=50)
        Sweet.objects.create(name='Vanilla Cake', category='cake', price=Decimal('15.00'), quantity=10)
        self.search_url = '/api/sweets/search'

    def authenticate(self):
        response = self.client.post('/api/auth/login', {
            'username': 'testuser',
            'password': 'testpass123'
        }, format='json')
        token = response.data['tokens']['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    def test_search_by_name(self):
        self.authenticate()
        response = self.client.get(f'{self.search_url}?name=chocolate')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Chocolate Bar')

    def test_search_by_category(self):
        self.authenticate()
        response = self.client.get(f'{self.search_url}?category=candy')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Gummy Bears')

    def test_search_by_price_range(self):
        self.authenticate()
        response = self.client.get(f'{self.search_url}?min_price=2&max_price=10')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Chocolate Bar')


class PurchaseRestockTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.admin = User.objects.create_superuser(username='admin', password='adminpass123')
        self.sweet = Sweet.objects.create(
            name='Chocolate Bar',
            category='chocolate',
            price=Decimal('2.50'),
            quantity=10
        )

    def authenticate_user(self):
        response = self.client.post('/api/auth/login', {
            'username': 'testuser',
            'password': 'testpass123'
        }, format='json')
        token = response.data['tokens']['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    def authenticate_admin(self):
        response = self.client.post('/api/auth/login', {
            'username': 'admin',
            'password': 'adminpass123'
        }, format='json')
        token = response.data['tokens']['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    def test_purchase_success(self):
        self.authenticate_user()
        url = f'/api/sweets/{self.sweet.id}/purchase'
        response = self.client.post(url, {'quantity': 2}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.sweet.refresh_from_db()
        self.assertEqual(self.sweet.quantity, 8)

    def test_purchase_not_enough_stock(self):
        self.authenticate_user()
        url = f'/api/sweets/{self.sweet.id}/purchase'
        response = self.client.post(url, {'quantity': 20}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Not enough stock', response.data['error'])

    def test_restock_admin_success(self):
        self.authenticate_admin()
        url = f'/api/sweets/{self.sweet.id}/restock'
        response = self.client.post(url, {'quantity': 50}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.sweet.refresh_from_db()
        self.assertEqual(self.sweet.quantity, 60)

    def test_restock_regular_user_forbidden(self):
        self.authenticate_user()
        url = f'/api/sweets/{self.sweet.id}/restock'
        response = self.client.post(url, {'quantity': 50}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
