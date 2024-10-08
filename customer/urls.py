from django.urls import path
from . import views

urlpatterns = [
    path('new/', views.open_account),
    path('balance/<str:phone>/', views.check_balance)
]
