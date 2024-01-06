from unittest.mock import patch, MagicMock

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken

from food.models.food import Food
from restaurant.models.restaurant import Restaurant
from user.models import CustomUser
from user.views import CustomUserViewSet

User = get_user_model()


class TokenObtainPairViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            name='Test User',
            password='strongpassword'
        )

    @patch('user.views.authenticate')
    def test_valid_credentials_return_token(self, mock_authenticate):
        mock_authenticate.return_value = self.user

        url = '/api/token/'
        data = {'username': 'test@example.com', 'password': 'strongpassword'}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access_token', response.data)

    @patch('user.views.authenticate')
    def test_invalid_credentials_return_unauthorized(self, mock_authenticate):
        mock_authenticate.return_value = None

        url = '/api/token/'
        data = {'username': 'test@example.com', 'password': 'wrongpassword'}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotIn('access_token', response.data)


class RegisterUserViewTests(APITestCase):

    def test_email_verification_view_valid_token(self):
        token = 'valid_token'
        user = User.objects.create(email='test@example.com', verification_token=token)

        with patch('user.views.CustomUser.objects.get') as mock_get_user:
            mock_get_user.return_value = user
            user.verification_token_expired = MagicMock(return_value=False)
            user.verified = False

            url = reverse('email-verification', kwargs={'token': token})
            response = self.client.get(url)

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.content.decode(), "Email verified successfully")

    def test_register_user_missing_required_fields(self):
        data = {
            'name': 'Test User',
            # 'email': 'test@example.com', # Email is missing
            'password': 'test_password',
        }
        with patch('user.views.UserRegistrationForm') as MockUserRegistrationForm:
            mock_form_instance = MockUserRegistrationForm.return_value
            mock_form_instance.is_valid.return_value = False
            mock_form_instance.errors = {'email': ['This field is required.']}  # Simulate missing email error

            url = reverse('register')
            response = self.client.post(url, data, format='json')

            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertIn('email', response.data)

    def test_register_user_invalid_email(self):
        data = {
            'name': 'Test User',
            'email': 'invalid_email',  # Invalid email format
            'password': 'test_password',
        }
        with patch('user.views.UserRegistrationForm') as MockUserRegistrationForm:
            mock_form_instance = MockUserRegistrationForm.return_value
            mock_form_instance.is_valid.return_value = False
            mock_form_instance.errors = {'email': ['Enter a valid email address.']}

            url = reverse('register')
            response = self.client.post(url, data, format='json')

            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertIn('email', response.data)

    def test_email_verification_view_expired_token(self):
        expired_token = 'expired_token'
        user = User.objects.create(email='test@example.com', verification_token=expired_token)

        with patch('user.views.CustomUser.objects.get') as mock_get_user:
            mock_get_user.return_value = user
            user.verification_token_expired = MagicMock(return_value=True)

            url = reverse('email-verification', kwargs={'token': expired_token})
            response = self.client.get(url)

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.content.decode(), "The verification link has expired.")

    def test_email_verification_view_already_verified(self):
        verified_token = 'verified_token'
        user = User.objects.create(email='test@example.com', verification_token=verified_token, verified=True)

        with patch('user.views.CustomUser.objects.get') as mock_get_user:
            mock_get_user.return_value = user

            url = reverse('email-verification', kwargs={'token': verified_token})
            response = self.client.get(url)

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.content.decode(), "Email already verified.")

    def test_email_verification_view_invalid_token(self):
        invalid_token = 'invalid_token'

        with patch('user.views.CustomUser.objects.get') as mock_get_user:
            mock_get_user.side_effect = User.DoesNotExist

            url = reverse('email-verification', kwargs={'token': invalid_token})
            response = self.client.get(url)

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.content.decode(), "Invalid verification token.")


class PasswordResetViewTests(APITestCase):
    def test_password_reset_request_success(self):
        email = 'test@example.com'
        user = User.objects.create(email=email)

        with patch('user.views.CustomUser.objects.filter') as mock_filter, \
                patch('user.views.CustomUser.generate_password_reset_token') as mock_generate_token, \
                patch('user.views.CustomUser.send_password_reset_email') as mock_send_email:
            mock_filter.return_value.first.return_value = user
            url = reverse('password-reset')
            data = {'email': email}
            response = self.client.post(url, data, format='json')

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data['message'], "Password reset link sent to your email.")
            mock_generate_token.assert_called_once()
            mock_send_email.assert_called_once()

    def test_password_reset_request_user_not_found(self):
        non_existing_email = 'non_existing@example.com'

        with patch('user.views.CustomUser.objects.filter') as mock_filter:
            mock_filter.return_value.first.return_value = None
            url = reverse('password-reset')
            data = {'email': non_existing_email}
            response = self.client.post(url, data, format='json')

            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
            self.assertEqual(response.data['message'], "User not found.")

    def test_password_reset_confirm_invalid_token(self):
        invalid_token = 'invalid_token'

        with patch('user.views.CustomUser.objects.filter') as mock_filter:
            mock_filter.return_value.first.return_value = None

            url = reverse('password-reset-confirm', kwargs={'token': invalid_token})
            response = self.client.post(url, {}, format='json')

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.content.decode(), "Invalid or expired token.")


class AddToFavoritesViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='test@example.com')
        self.access_token = str(AccessToken.for_user(self.user))

    def test_add_to_favorites_success(self):
        user = self.user
        restaurant = Restaurant.objects.create(name='Test Restaurant')
        food = Food.objects.create(name='Test Food', restaurant=restaurant, price=1400, max_time_to_delivery=80, min_time_to_delivery=60)

        request_data = {
            'restaurant_ids': [restaurant.id],
            'food_ids': [food.id]
        }

        with patch('user.views.CustomUser.objects.get') as mock_get_user, \
                patch('restaurant.models.restaurant.Restaurant.objects.get') as mock_get_restaurant, \
                patch('food.models.food.Food.objects.get') as mock_get_food:
            mock_get_user.return_value = user
            mock_get_restaurant.return_value = restaurant
            mock_get_food.return_value = food

            url = reverse('add_to_favorites')
            headers = {'HTTP_AUTHORIZATION': f'Bearer {self.access_token}'}
            response = self.client.post(url, request_data, format='json', **headers)

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data['message'], 'Added to favorites successfully')

            user.refresh_from_db()
            self.assertTrue(user.favorite_restaurants.filter(pk=restaurant.id).exists())
            self.assertTrue(user.favorite_foods.filter(pk=food.id).exists())

    def test_add_to_favorites_missing_data(self):
        request_data = {}  # Missing 'restaurant_ids' and 'food_ids'

        url = reverse('add_to_favorites')
        headers = {'HTTP_AUTHORIZATION': f'Bearer {self.access_token}'}
        response = self.client.post(url, request_data, format='json', **headers)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Both restaurant_ids and food_ids are required and must be a list!')

    def test_add_to_favorites_no_ids_provided(self):
        # Test case for no restaurant_ids or food_ids provided
        request_data = {'restaurant_ids': [], 'food_ids': []}  # Empty lists for both

        url = reverse('add_to_favorites')
        headers = {'HTTP_AUTHORIZATION': f'Bearer {self.access_token}'}
        response = self.client.post(url, request_data, format='json', **headers)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'At least one restaurant_id or food_id is required')

    def test_add_to_favorites_invalid_restaurant_id(self):
        invalid_restaurant_id = 9999  # Non-existing restaurant_id
        request_data = {'restaurant_ids': [invalid_restaurant_id], 'food_ids': []}

        with patch('user.views.CustomUser.objects.get') as mock_get_user, \
                patch('restaurant.models.restaurant.Restaurant.objects.get') as mock_get_restaurant:
            mock_get_user.return_value = self.user
            mock_get_restaurant.side_effect = Restaurant.DoesNotExist

            url = reverse('add_to_favorites')
            headers = {'HTTP_AUTHORIZATION': f'Bearer {self.access_token}'}
            response = self.client.post(url, request_data, format='json', **headers)

            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
            self.assertEqual(response.data['message'], f'Restaurant with ID {invalid_restaurant_id} not found')


class RemoveFromFavoritesViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='test@example.com')
        self.access_token = str(AccessToken.for_user(self.user))
        self.restaurant = Restaurant.objects.create(name='Test Restaurant')
        self.food = Food.objects.create(name='Test Food', restaurant=self.restaurant, price=1400, max_time_to_delivery=80, min_time_to_delivery=60)

    def test_remove_from_favorites_success(self):
        request_data = {
            'restaurant_ids': [self.restaurant.id],
            'food_ids': [self.food.id]
        }

        with patch('user.views.CustomUser.objects.get') as mock_get_user, \
                patch('restaurant.models.restaurant.Restaurant.objects.get') as mock_get_restaurant, \
                patch('food.models.food.Food.objects.get') as mock_get_food:
            mock_get_user.return_value = self.user
            mock_get_restaurant.return_value = self.restaurant
            mock_get_food.return_value = self.food

            url = reverse('remove_from_favorites')
            headers = {'HTTP_AUTHORIZATION': f'Bearer {self.access_token}'}
            response = self.client.post(url, request_data, format='json', **headers)

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data['message'], 'Removed from favorites successfully')

            # Check if the user's favorites are updated
            user = User.objects.get(email='test@example.com')
            self.assertFalse(user.favorite_restaurants.filter(pk=self.restaurant.id).exists())
            self.assertFalse(user.favorite_foods.filter(pk=self.food.id).exists())

    def test_remove_from_favorites_no_ids_provided(self):
        request_data = {}  # Missing 'restaurant_ids' and 'food_ids'

        url = reverse('remove_from_favorites')
        headers = {'HTTP_AUTHORIZATION': f'Bearer {self.access_token}'}
        response = self.client.post(url, request_data, format='json', **headers)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'At least one restaurant_id or food_id is required')

    def test_remove_from_favorites_invalid_restaurant_id(self):
        invalid_restaurant_id = 9999  # Non-existing restaurant_id
        request_data = {'restaurant_ids': [invalid_restaurant_id], 'food_ids': []}

        with patch('user.views.CustomUser.objects.get') as mock_get_user, \
                patch('restaurant.models.restaurant.Restaurant.objects.get') as mock_get_restaurant:
            mock_get_user.return_value = self.user
            mock_get_restaurant.side_effect = Restaurant.DoesNotExist

            url = reverse('remove_from_favorites')
            headers = {'HTTP_AUTHORIZATION': f'Bearer {self.access_token}'}
            response = self.client.post(url, request_data, format='json', **headers)

            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
            self.assertEqual(response.data['message'], f'Restaurant with ID {invalid_restaurant_id} not found')


class UpdateProfileViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='test@example.com', name='Test User')
        self.access_token = str(AccessToken.for_user(self.user))

    def test_update_profile_name_success(self):
        request_data = {'name': 'Updated Name'}

        with patch('user.views.CustomUser.objects.get') as mock_get_user:
            mock_get_user.return_value = self.user

            url = reverse('update_profile')
            headers = {'HTTP_AUTHORIZATION': f'Bearer {self.access_token}'}
            response = self.client.patch(url, request_data, format='json', **headers)

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data['name'], 'Updated Name')

            user = User.objects.get(email='test@example.com')
            self.assertEqual(user.name, 'Updated Name')

    def test_update_profile_mobile_number_success(self):
        request_data = {'mobile_number': '1234567890'}

        with patch('user.views.CustomUser.objects.get') as mock_get_user:
            mock_get_user.return_value = self.user

            url = reverse('update_profile')
            headers = {'HTTP_AUTHORIZATION': f'Bearer {self.access_token}'}
            response = self.client.patch(url, request_data, format='json', **headers)

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data['mobile_number'], '1234567890')

            user = User.objects.get(email='test@example.com')
            self.assertEqual(user.mobile_number, '1234567890')

    # def test_update_profile_photo_success(self):
    #     request_data = {'photo': 'test_photo.jpg'}
    #
    #     with patch('user.views.CustomUser.objects.get') as mock_get_user:
    #         mock_get_user.return_value = self.user
    #
    #         url = reverse('update_profile')
    #         headers = {'HTTP_AUTHORIZATION': f'Bearer {self.access_token}'}  # Replace self.access_token with your actual token
    #         response = self.client.patch(url, request_data, format='json', **headers)
    #         print(response.data)
    #         self.assertEqual(response.status_code, status.HTTP_200_OK)
    #         self.assertEqual(response.data['photo'], 'test_photo.jpg')
    #
    #         # Check if the user's photo is updated in the database
    #         user = User.objects.get(email='test@example.com')
    #         self.assertEqual(user.photo, 'test_photo.jpg')

    def test_update_profile_invalid_user_id(self):
        request_data = {'name': 'Updated Name'}

        with patch('user.views.CustomUser.objects.get') as mock_get_user:
            mock_get_user.side_effect = User.DoesNotExist

            url = reverse('update_profile')
            headers = {'HTTP_AUTHORIZATION': f'Bearer {self.access_token}'}
            response = self.client.patch(url, request_data, format='json', **headers)

            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class CustomUserViewSetTests(APITestCase):
    def setUp(self):
        self.view = CustomUserViewSet.as_view({'get': 'list', 'post': 'create', 'patch': 'update', 'delete': 'destroy'})
        self.user = CustomUser.objects.create(email='test@example.com', name='Test User')

    def test_list_users(self):
        response = self.client.get('/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_user(self):
        response = self.client.get(f'/users/{self.user.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_user(self):
        data = {'name': 'New User', 'password': 'New User', 'email': 'newuser@example.com'}
        response = self.client.post('/users/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_user(self):
        data = {'name': 'Updated Name'}
        response = self.client.patch(f'/users/{self.user.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_user(self):
        response = self.client.delete(f'/users/{self.user.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
