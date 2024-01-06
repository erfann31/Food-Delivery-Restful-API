from rest_framework import status
from rest_framework.test import APITestCase

from discount_code.models.discount_code import DiscountCode
from discount_code.views import DiscountCodeViewSet


class DiscountCodeViewSetTests(APITestCase):
    def setUp(self):
        self.view = DiscountCodeViewSet.as_view({'get': 'list', 'post': 'create', 'patch': 'update', 'delete': 'destroy'})
        self.discount_code = DiscountCode.objects.create(code_text='TESTCODE', discount_percent=10.0)

    def test_list_discount_codes(self):
        response = self.client.get('/discount_codes/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_discount_code(self):
        response = self.client.get(f'/discount_codes/{self.discount_code.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_discount_code(self):
        data = {'code_text': 'NEWCODE', 'discount_percent': 15.0}
        response = self.client.post('/discount_codes/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_discount_code(self):
        data = {'discount_percent': 20.0}
        response = self.client.patch(f'/discount_codes/{self.discount_code.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_discount_code(self):
        response = self.client.delete(f'/discount_codes/{self.discount_code.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
