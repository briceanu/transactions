from django.db import models
from django.contrib.auth.models import AbstractUser



class User(AbstractUser):
    balance = models.DecimalField(max_digits=6, decimal_places=2 ,default=0)

    def __str__(self):
        return self.username


    class Meta:
        db_table = 'client'
        ordering = ['username']
 
  