from django.db import models

# Create your models here.

class Location(models.Model):
    city = models.CharField(max_length=50)

    def __str__(self):
        return self.city
    
class CarDealer(models.Model):
    username = models.CharField(max_length=10)
    email = models.CharField(max_length=10)
    phone = models.PositiveBigIntegerField(max_length=10)
    location = models.CharField(max_length=20)
    earnings = models.IntegerField(default=0)
    types = models.CharField(max_length=20, blank=True)
    password = models.CharField(max_length=50)

    def __str__(self):
        return str(self.username)

class Car(models.Model):
    car_dealer = models.ForeignKey(CarDealer, on_delete=models.PROTECT)
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to="")    
    capacity = models.CharField(max_length=2)
    location = models.CharField(max_length=20)
    is_available = models.BooleanField(default=True)
    rent = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return self.name

class Customer(models.Model):
    username = models.CharField(max_length=10)
    email = models.CharField(max_length=10)
    phone = models.PositiveBigIntegerField(max_length=10)
    location = models.CharField(max_length=20)    
    password = models.CharField(max_length=50)

    def __str__(self):
        return str(self.username)

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    dealer = models.ForeignKey(CarDealer, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    rent = models.CharField(max_length=10)
    days = models.CharField(max_length=3)
    is_complete = models.BooleanField(default=False)
    