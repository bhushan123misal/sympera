from drf_yasg import openapi

transaction_amount_request_body = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=['amount'],
    properties={
        'amount': openapi.Schema(type=openapi.TYPE_NUMBER)
    },
    example={
        "amount": 11
    }
)

transaction_response_body = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=['balance'],
    properties={
        'balance': openapi.Schema(type=openapi.TYPE_STRING)
    },
    example="Current balance is 11"
)


history_response_body = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    example=[{
        "phone": "7710947920",
        "firstName": "Doe",
        "lastName": "J",
        "balance": 11
    }]
)

authorization_header = openapi.Parameter(
    'Authorization',
    in_=openapi.IN_HEADER,
    description="Authorization token",
    type=openapi.TYPE_STRING
)
