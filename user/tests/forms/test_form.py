import unittest

from django import forms
from django.test import TestCase

from user.forms.forms import UserRegistrationForm
from user.models import CustomUser


class UserRegistrationFormTestCase(TestCase):
    def test_form_fields(self):
        form = UserRegistrationForm()
        self.assertTrue('name' in form.fields)
        self.assertTrue('email' in form.fields)
        self.assertTrue('password' in form.fields)

    def test_password_widget(self):
        form = UserRegistrationForm()
        self.assertIsInstance(form.fields['password'].widget, forms.PasswordInput)

    def test_model_association(self):
        self.assertEqual(UserRegistrationForm._meta.model, CustomUser)

    # def test_form_save_method(self):
    #     user_data = {'name': 'John Doe', 'email': 'john@example.com', 'password': 'password123'}
    #     form = UserRegistrationForm(data=user_data)
    #     self.assertTrue(form.is_valid(), msg=form.errors.as_text())
    #
    #     with patch.object(CustomUser.objects, 'create_user') as mock_create_user:
    #         form.save()
    #         mock_create_user.assert_called_once_with(
    #             name=user_data['name'],
    #             email=user_data['email'],
    #             password=user_data['password']
    #         )


if __name__ == '__main__':
    unittest.main()
