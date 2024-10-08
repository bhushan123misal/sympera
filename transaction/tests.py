from django.test import TestCase
from ..customer.models import Customer
from .models import Transactions


class CustomerTestCase(TestCase):
    def setUp(self):
        Customer.objects.create(**{
                "phone": 0000000000,
                "firstName": "Test1",
                "lastName": "Name",
                "balance": 100
        })

        Customer.objects.Create(**{
                "phone": 1000000000,
                "firstName": "Test2",
                "lastName": "Name",
                "balance": 50
        })

    def test_deposit_transaction(self):...




