from django.test import TestCase
from .models import Customer
from .serializers import CustomerSerializer


class CustomerTestCase(TestCase):
    def setUp(self):
        Customer.objects.create(**{
                "phone": 0000000000,
                "firstName": "Test",
                "lastName": "Name",
                "balance": 11
        })

    def test_customer_phone_number_exists(self):
        test_customer = Customer.objects.get(phone=0000000000)
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

