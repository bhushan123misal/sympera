from customer.models import Customer
from customer.serializers import CustomerSerializer
from rest_framework.test import APIClient, APITestCase
from django.urls import reverse
from rest_framework import status

class CustomerTestCase(APITestCase):
    def setUp(self):
        customer1 = {
                "phone": '0000000000',
                "firstName": "Test1",
                "lastName": "Name",
                "balance": 11
        }
        customer2 = {
                "phone": 1000000000,
                "firstName": "Test2",
                "lastName": "Name",
                "balance": 11
        }

        self.client = APIClient()
        self.create_account_url = reverse('create_account')
        self.check_balance_url = lambda phone: f'/customer/balance/{phone}/'

        self.customer_1 = Customer.objects.create(**customer1)
        self.customer_2 = Customer.objects.create(**customer2)

    def test_create_account(self):
        data = {
                "phone": 2000000000,
                "firstName": "Test3",
                "lastName": "Name",
                "balance": 11
        }
        response = self.client.post(self.create_account_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_create_account_with_invalid_phone(self):
        data = {
                "phone": 20000000020,
                "firstName": "Test3",
                "lastName": "Name",
                "balance": 11
        }
        response = self.client.post(self.create_account_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_account_with_missing_param(self):
        data = {
                "phone": 20000000020,
                "lastName": "Name",
                "balance": 11
        }
        response = self.client.post(self.create_account_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_check_balance(self):
        data = {
                "phone": 2000000000,
                "firstName": "Test3",
                "lastName": "Name",
                "balance": 11
        }
        response = self.client.post(self.create_account_url, data, format='json')
        # existing number in db
        response = self.client.get(self.check_balance_url('2000000000'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        #non existing in db
        response2 = self.client.get(self.check_balance_url('9000000000'))
        self.assertEqual(response2.status_code, status.HTTP_404_NOT_FOUND)
        #Unaccepted number
        response2 = self.client.get(self.check_balance_url('00000001000'))
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)


    def test_customer_phone_number_exists(self):
        test_customer = Customer.objects.get(phone='0000000000')
        self.assertTrue(test_customer)

    def test_customer_phone_number_does_not_exist(self):
        with self.assertRaises(Exception) as context:
            Customer.objects.get(phone=32132)
            self.assertTrue("Customer matching query does not exist" in context)

    def test_invalid_phone_number(self):
        body = {
                "phone": 7710920,
                "firstName": "Test_invalid_number",
                "lastName": "Name",
                "balance": 11
        }
        serializer = CustomerSerializer(data=body)
        self.assertFalse(serializer.is_valid())

