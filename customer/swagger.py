from drf_yasg import openapi

open_account_request_body = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=['phone', 'firstName', 'lastName', 'balance'],
    properties={
        'phone': openapi.Schema(type=openapi.TYPE_STRING),
        'firstName': openapi.Schema(type=openapi.TYPE_STRING),
        'lastName': openapi.Schema(type=openapi.TYPE_STRING),
        'balance': openapi.Schema(type=openapi.TYPE_NUMBER)
    },
    example={
        "phone": "7710947920",
        "firstName": "Doe",
        "lastName": "J",
        "balance": 11
    }
)


check_balance_response_201 = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=['balance'],
    properties={
        'balance': openapi.Schema(type=openapi.TYPE_NUMBER)
    },
    example={
        "balance": 11
    }
)

