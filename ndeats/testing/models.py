from email.policy import default
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

# User Class
class Person(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100, unique=True)

# Order Class w/ User as foreign key
class Order(models.Model):
    dropoff = models.CharField(max_length=200)
    pickup = models.CharField(max_length=200)
    tip = models.FloatField(
        default=1.0, validators=[MinValueValidator(0.0), MaxValueValidator(50.0)])
    delivererId = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='Deliverer',
        blank=True, null=True)
    ordererId = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='Orderer')
    available = models.BooleanField(default=True)
    readyBy = models.TimeField()


class OldOrder(models.Model):
    dropoff = models.CharField(max_length=200)
    pickup = models.CharField(max_length=200)
    tip = models.FloatField(
        default=1.0, validators=[MinValueValidator(0.0), MaxValueValidator(50.0)])
    delivererId = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='OldDeliverer',
        blank=True, null=True)
    ordererId = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='OldOrderer')
    readyBy = models.TimeField()
