from django.db import models

class Transactions(models.Model):
    customer = models.ForeignKey("customer.Customer", on_delete=models.CASCADE, related_name="Customer")
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    type = models.CharField(
        max_length=20,
        choices={"deposit":"DEPOSIT", "withdraw":"WITHDRAW", "transfer":"TRANSFER"}
    )
    customer_to = models.ForeignKey("customer.Customer", on_delete=models.CASCADE, null=True, related_name="Customer_to")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.customer.firstName + " has " + self.type + "ed " + str(self.amount) + " to " + str(self.customer_to)
