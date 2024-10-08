import json
import re

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

from customer.models import Customer
from .models import Transactions


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def deposit(request, phone):
    if len(phone)!=10 or not re.match(r'^[0-9]', phone):
        # Validate the number - 10 digit & numeric
        return HttpResponse("phone number must be numeric and 10 digits", status=status.HTTP_400_BAD_REQUEST)
    amount = json.loads((request.body.decode("utf-8")))["amount"]
    try:
        customer = Customer.objects.get(phone=phone)
    except Exception as E:
        return HttpResponse(E, status=status.HTTP_404_NOT_FOUND)

    if amount and amount>0: # Negative deposit not acceptable
        customer.balance = float(customer.balance) + amount
        customer.save()

        Transactions.objects.create(
            customer = customer,
            amount = amount,
            type = "deposit",
        )
        return HttpResponse(str(amount) + " was deposited to " + phone + ". Current balance is " + str(customer.balance),
                        status=status.HTTP_201_CREATED)

    return HttpResponse("Unacceptable amount", status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def withdraw(request, phone):
    if len(phone)!=10 or not re.match(r'^[0-9]', phone):
        # Validate the number - 10 digit & numeric
        return HttpResponse("phone number must be numeric and 10 digits", status=status.HTTP_400_BAD_REQUEST)
    amount = json.loads((request.body.decode("utf-8")))["amount"]
    try:
        customer = Customer.objects.get(phone=phone)
    except Exception as E:
        return HttpResponse(E, status=status.HTTP_400_BAD_REQUEST)

    if amount and amount>0 and float(customer.balance) >= amount:
        # Negative withdrawal not acceptable & withdrawal amount should be lesser than account balance
        customer.balance = float(customer.balance) - amount
        customer.save()

        Transactions.objects.create(
            customer = customer,
            amount = amount,
            type = "withdraw",
        )
        return HttpResponse(str(amount) + " was withdrawn from " + phone + ". Current balance is " + str(customer.balance),
                        status=status.HTTP_201_CREATED)

    return HttpResponse("Unacceptable amount", status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def transfer(request, from_phone, to_phone):
    if from_phone == to_phone:
        return HttpResponse("Same sender & receiver", status=status.HTTP_400_BAD_REQUEST)
    if len(from_phone)!=10 or not re.match(r'^[0-9]', from_phone) or \
            len(to_phone)!=10 or not re.match(r'^[0-9]', to_phone):
        # Validate both numbers - 10 digit & numeric

        return HttpResponse("phone number must be numeric and 10 digits", status=status.HTTP_400_BAD_REQUEST)

    amount = json.loads((request.body.decode("utf-8")))["amount"]

    try:
        customer_from = Customer.objects.get(phone=from_phone)
        customer_to = Customer.objects.get(phone=to_phone)
    except Exception as E:
        return HttpResponse(E, status=status.HTTP_400_BAD_REQUEST)

    if amount and amount>0 and float(customer_from.balance)>=amount:
        # Negative transfer amount not acceptable & sender's balance must be greater than transfer amount
        customer_from.balance = float(customer_from.balance) - amount
        customer_to.balance = float(customer_to.balance) + amount
        customer_from.save()
        customer_to.save()

        Transactions.objects.create(
            customer = customer_from,
            amount = amount,
            type = "transfer",
            customer_to = customer_to
        )
        return HttpResponse(str(amount) + " was transfered from " + from_phone + " to " + to_phone + " Current balance is " + str(customer_to.balance),
                        status=status.HTTP_201_CREATED)

    return HttpResponse("Unacceptable amount", status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def history(request, phone):
    if len(phone)!=10 or not re.match(r'^[0-9]', phone):
        # Validate the number - 10 digit & numeric
        return HttpResponse("phone number must be numeric and 10 digits", status=status.HTTP_400_BAD_REQUEST)
    try:
        customer = Customer.objects.get(phone=phone)
    except Exception as E:
        return HttpResponse(E, status=status.HTTP_400_BAD_REQUEST)

    history = Transactions.objects.filter(Q(customer=customer) | Q(customer_to=customer))
    result = []
    for i in history:
        result.append(
            {
                "customer": i.customer_id,
                "amount": float(i.amount),
                "type": i.type,
                "customer_to": i.customer_to_id
            }
        )
    return HttpResponse(json.dumps(result))

