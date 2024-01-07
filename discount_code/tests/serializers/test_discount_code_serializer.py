import unittest
from discount_code.models.discount_code import DiscountCode
from discount_code.serializers.discount_code_serializer import DiscountCodeSerializer


class DiscountCodeSerializerTestCase(unittest.TestCase):

    def test_discount_code_serializer_fields(self):
        serializer = DiscountCodeSerializer()
        self.assertEqual(serializer.Meta.model, DiscountCode)  # Assert model is DiscountCode
        self.assertEqual(serializer.Meta.fields, '__all__')  # Assert fields attribute is '__all__'
        self.assertEqual(serializer.Meta.read_only_fields, ('id',))  # Assert read_only_fields includes 'id'

if __name__ == '__main__':
    unittest.main()
