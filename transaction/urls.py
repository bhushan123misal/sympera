from django.urls import path
from . import views

urlpatterns = [
    path('deposit/<str:phone>', views.deposit),
    path('withdraw/<str:phone>', views.withdraw),
    path('transfer/<str:from_phone>/<str:to_phone>', views.transfer),
    path('history/<str:phone>', views.history)
]
