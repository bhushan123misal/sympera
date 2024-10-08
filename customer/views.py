import json
import re

from django.http import HttpResponse
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

from drf_yasg.utils import swagger_auto_schema

from .models import Customer
from.serializers import CustomerSerializer
from .swagger import open_account_request_body, check_balance_response_201, authorization_header



@swagger_auto_schema(method='post',
                     request_body=open_account_request_body,
                     responses={201:"Account Created", 400:"Bad Request"},
                     manual_parameters=[authorization_header],
                     operation_description="Create a new customer account with a name, phone and an initial balance")
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def open_account(request):
    body = json.loads((request.body.decode("utf-8")))
    serializer = CustomerSerializer(data=body)
    if serializer.is_valid():
        serializer.save()
        return HttpResponse(serializer.data, status=status.HTTP_201_CREATED)
    return HttpResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@swagger_auto_schema(method='get',
                     responses={201: check_balance_response_201, 400:"Bad Request"},
                     manual_parameters=[authorization_header],
                     operation_description="Show balance for given customer (phone number)")
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_balance(request, phone):
    if len(phone)!=10 or not re.match(r'^[0-9]', phone):
        return HttpResponse("phone number must be numeric and 10 digits", status=status.HTTP_400_BAD_REQUEST)

    try:
        customer = Customer.objects.get(phone=phone)
    except Exception as E:
        return HttpResponse(E, status=status.HTTP_400_BAD_REQUEST)
    serializer = CustomerSerializer(customer)
    return HttpResponse(float(serializer.data["balance"]), status=status.HTTP_200_OK)
