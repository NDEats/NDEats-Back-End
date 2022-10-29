from django.urls import path
from .views import Order

urlpatterns = [
    path('orders/', Order.as_view()),
]
