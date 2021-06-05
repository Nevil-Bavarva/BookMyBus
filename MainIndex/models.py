from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Agency(models.Model):
    AgencyName =  models.CharField(max_length=250)
    Agencynumber =  models.IntegerField(max_length=250)

    def __str__(self):
        return self.AgencyName


class Bus(models.Model):
    BusName = models.CharField(max_length=250)
    BusNumber =  models.CharField(max_length=250)
    BusCompany = models.ForeignKey( Agency, on_delete=models.SET_DEFAULT, default=1)
    BusImage = models.CharField(max_length=5000, default="https://i.ytimg.com/vi/FnKM_1TbWJU/hqdefault.jpg")

    def __str__(self):
        return self.BusName


class Customer(models.Model):
    Customer = models.OneToOneField(User,on_delete=models.CASCADE)
