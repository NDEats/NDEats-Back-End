from django.urls import path
from .views import Order, OrderUpdate, Person

urlpatterns = [
    path('persons/<int:person_id>', Person.as_view()),
    path('persons/', Person.as_view()),
    path('orders/', Order.as_view()),
    path('update-order/<int:order_id>', OrderUpdate.as_view()),
]
