from customer.models import Customer
from rest_framework.test import APIClient, APITestCase
from django.urls import reverse
from rest_framework import status

class Transaction(APITestCase):
    def setUp(self):
        self.customer1_info = customer1 = {
                "phone": '2000000000',
                "firstName": "Test1",
                "lastName": "Name",
                "balance": 11.
        }
        self.customer2_info = customer2 = {
                "phone": 1000000000,
                "firstName": "Test2",
                "lastName": "Name",
                "balance": 11.
        }

        self.client = APIClient()
        self.create_account_url = reverse('create_account')
        self.check_balance_url = lambda phone: f'/customer/balance/{phone}/'
        self.deposit_url = lambda phone: f'/transaction/deposit/{phone}'
        self.withdraw_url = lambda phone: f'/transaction/withdraw/{phone}'
        self.transfer_url = lambda from_phone, to_phone: \
            f'/transaction/transfer/{from_phone}/{to_phone}'

        self.customer_1 = Customer.objects.create(**customer1)
        self.customer_2 = Customer.objects.create(**customer2)

    def test_deposit_funds(self):
        initial_balance = Customer.objects.get(pk=self.customer_1.phone).balance
        response = self.client.post(self.deposit_url(self.customer_1.phone), {"amount":20}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        final_balance = Customer.objects.get(pk=self.customer_1.phone).balance
        self.assertEqual(float(final_balance-initial_balance), 20.)

    def test_withdraw_funds(self):
        initial_balance = Customer.objects.get(pk=self.customer_1.phone).balance
        response = self.client.post(self.withdraw_url(self.customer_1.phone), {"amount":5}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        final_balance = Customer.objects.get(pk=self.customer_1.phone).balance
        self.assertEqual(float(initial_balance-final_balance), 5.)

    def test_tansfer_funds(self):
        initial_balance1 = Customer.objects.get(pk=self.customer_1.phone).balance
        initial_balance2 = Customer.objects.get(pk=self.customer_2.phone).balance
        response = self.client.post(self.transfer_url(self.customer_1.phone, self.customer_2.phone), {"amount":5}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        final_balance1 = Customer.objects.get(pk=self.customer_1.phone).balance
        final_balance2 = Customer.objects.get(pk=self.customer_2.phone).balance
        self.assertEqual(float(initial_balance1-final_balance1), 5.)
        self.assertEqual(float(initial_balance2-final_balance2), -5.)


