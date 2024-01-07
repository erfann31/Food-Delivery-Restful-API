import unittest

from django.test import TestCase

from discount_code.models.discount_code import DiscountCode


class DiscountCodeModelTestCase(TestCase):

    def setUp(self):
        self.discount_code = DiscountCode.objects.create(
            discount_percent=10.00,
            code_text='TESTCODE',
            is_active=True
        )

    def test_discount_code_str_method(self):
        expected_result = 'TESTCODE - 10.0% Discount'
        self.assertEqual(str(self.discount_code), expected_result)

    def test_discount_percent_field(self):
        self.assertEqual(self.discount_code.discount_percent, 10.00)

    def test_code_text_field_unique_constraint(self):
        # Create a DiscountCode with an existing code_text
        with self.assertRaises(Exception):
            DiscountCode.objects.create(
                discount_percent=20.00,
                code_text='TESTCODE',  # Trying to create a duplicate code_text
                is_active=True
            )

    def test_is_active_field_default_value(self):
        new_discount_code = DiscountCode.objects.create(
            discount_percent=15.00,
            code_text='NEWCODE',
        )
        self.assertTrue(new_discount_code.is_active)  # Checking if default value is True


if __name__ == '__main__':
    unittest.main()
