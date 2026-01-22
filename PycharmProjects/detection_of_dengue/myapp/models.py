from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Users(models.Model):
    name=models.CharField(max_length=100)
    dob=models.DateField()
    email=models.CharField(max_length=100)
    phone=models.CharField(max_length=100)
    gender=models.CharField(max_length=50)
    place=models.CharField(max_length=100)
    status=models.CharField(max_length=100)
    AUTHUSER=models.OneToOneField(User,on_delete=models.CASCADE)

class Complaint(models.Model):
    date=models.DateField()
    complaint=models.CharField(max_length=100)
    reply=models.CharField(max_length=100)
    status=models.CharField(max_length=100)
    USER=models.ForeignKey(Users,on_delete=models.CASCADE)

class Review(models.Model):
    date = models.DateField()
    review=models.CharField(max_length=100)
    rating=models.CharField(max_length=100)
    USER = models.ForeignKey(Users, on_delete=models.CASCADE)

class Logs(models.Model):
    date = models.DateField()
    time=models.DateTimeField()
    result=models.CharField(max_length=100)
    USER = models.ForeignKey(Users, on_delete=models.CASCADE)

class Alert(models.Model):
    date = models.DateField()
    time = models.DateTimeField()
    labels=models.CharField(max_length=100)
    USER = models.ForeignKey(Users, on_delete=models.CASCADE)
