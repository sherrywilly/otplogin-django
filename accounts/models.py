from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Profile(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,blank=True)
    otp_x = models.IntegerField(blank=True)
    phone = models.CharField(max_length=10,blank=True)

    def __str__(self):
        return str(self.phone)
