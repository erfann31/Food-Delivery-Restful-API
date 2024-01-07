import unittest
from unittest.mock import patch, Mock
from discount_code.models.discount_code import DiscountCode
from discount_code.repositories.discount_code_repository import DiscountCodeRepository


class DiscountCodeRepositoryTestCase(unittest.TestCase):

    @patch('discount_code.models.discount_code.DiscountCode.objects')
    def test_get_discount_code_by_text_found(self, mock_objects):
        # Mocking the objects.get method to simulate a found DiscountCode
        mock_objects.get.return_value = DiscountCode(code_text='TESTCODE', is_active=True)

        # Calling the method being tested
        result = DiscountCodeRepository.get_discount_code_by_text('TESTCODE')

        self.assertIsNotNone(result)  # Assert that a DiscountCode is returned
        mock_objects.get.assert_called_once_with(code_text='TESTCODE', is_active=True)

    @patch('discount_code.models.discount_code.DiscountCode.objects')
    def test_get_discount_code_by_text_not_found(self, mock_objects):
        # Mocking the objects.get method to simulate a DiscountCode not found
        mock_objects.get.side_effect = DiscountCode.DoesNotExist

        # Calling the method being tested
        result = DiscountCodeRepository.get_discount_code_by_text('NONEXISTENT')

        self.assertIsNone(result)  # Assert that None is returned for a non-existent code
        mock_objects.get.assert_called_once_with(code_text='NONEXISTENT', is_active=True)


if __name__ == '__main__':
    unittest.main()
