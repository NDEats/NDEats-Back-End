from django.urls import path
from .views import Order

urlpatterns = [
    path('orders/', Orders.as_view()),
]
