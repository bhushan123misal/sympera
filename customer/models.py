from django.db import models
from django.core.validators import MinLengthValidator

# Create your models here.
class Customer(models.Model):
    phone = models.CharField(max_length=10, primary_key=True, validators=[MinLengthValidator(10)])
    firstName = models.CharField(max_length=20)
    lastName = models.CharField(max_length=20)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.firstName + " " + self.lastName



