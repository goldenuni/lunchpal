from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from .models import Restaurant, Menu
from datetime import date
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class RestaurantMenuTests(APITestCase):

    def setUp(self):
        self.superuser = User.objects.create_superuser(
            email='superuser@example.com', password='testpass'
        )
        self.manager = User.objects.create_user(
            email='manager@example.com',
            password='testpass',
            user_type="manager"
        )
        self.employee = User.objects.create_user(
            email='employee@example.com', password='testpass'
        )

        self.restaurant = Restaurant.objects.create(
            name='Test Restaurant',
            address='123 Test St',
            cuisine='Test Cuisine'
        )

        self.menu = Menu.objects.create(
            restaurant=self.restaurant,
            items='Pizza, Salad',
            date=date.today(),
            price=9.99
        )

    def authenticate(self, user):
        """Helper function to authenticate the user and return the token."""
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    def test_create_restaurant_as_superuser(self):
        token = self.authenticate(self.superuser)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        url = reverse('lunchpal:restaurant-list-create')
        data = {
            'name': 'New Restaurant',
            'address': '456 New St',
            'cuisine': 'New Cuisine'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_menu_as_manager(self):
        token = self.authenticate(self.manager)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        url = reverse('lunchpal:menu-list-create')
        data = {
            'restaurant': self.restaurant.id,
            'items': 'Burger, Fries',
            'date': date.today(),
            'price': 10.99
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_vote_for_menu_as_employee(self):
        token = self.authenticate(self.employee)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        url = reverse(
            'lunchpal:vote-for-menu',
            kwargs={'menu_id': self.menu.id}
        )
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_current_day_menu(self):
        token = self.authenticate(self.employee)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        url = reverse('lunchpal:current-day-menu')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_today_results(self):
        token = self.authenticate(self.employee)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        url = reverse('lunchpal:current-day-menu-result')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_restaurant_as_employee(self):
        token = self.authenticate(self.employee)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        url = reverse('lunchpal:restaurant-list-create')
        data = {
            'name': 'Invalid Restaurant',
            'address': '789 Invalid St',
            'cuisine': 'Invalid Cuisine'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_menu_not_found(self):
        token = self.authenticate(self.employee)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        url = reverse('lunchpal:vote-for-menu', kwargs={'menu_id': 999})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_restaurant_with_missing_name(self):
        token = self.authenticate(self.superuser)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        url = reverse('lunchpal:restaurant-list-create')
        data = {
            'address': '456 New St',
            'cuisine': 'New Cuisine'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_vote_for_menu_as_unauthorized_user(self):
        url = reverse(
            'lunchpal:vote-for-menu',
            kwargs={'menu_id': self.menu.id}
        )
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_today_results_no_menus(self):
        Menu.objects.all().delete()

        token = self.authenticate(self.employee)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        url = reverse('lunchpal:current-day-menu-result')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("No menus found for today", response.data['Error'])
