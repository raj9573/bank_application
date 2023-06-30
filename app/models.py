from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    address=models.TextField()
    mobile_number=models.IntegerField()
    account_number=models.IntegerField()
    balance=models.DecimalField(max_digits=8,decimal_places=2)
    def __str__(self):
        return self.user.username
class history(models.Model):
    SENDER=models.CharField(max_length=100)
    RECEIVER=models.CharField(max_length=100)
    MONEY=models.DecimalField(max_digits=8,decimal_places=2)
    DATETIME=models.DateTimeField()
    
    def __str__(self):

        return self.SENDER 