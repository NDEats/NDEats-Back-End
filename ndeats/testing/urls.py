from django.urls import path
from .views import Order, OrderUpdate

urlpatterns = [
    path('orders/', Order.as_view()),
    path('update-order/<int:order_id>', OrderUpdate.as_view()),
]
