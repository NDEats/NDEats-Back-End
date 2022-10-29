from django.db import models

class Users(models.Model):
    user_id = models.IntegerField()
    user_name = models.CharField(max_length = 100)
    user_email = models.CharField(max_length = 100)