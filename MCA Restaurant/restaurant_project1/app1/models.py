from django.db import models
 
 
from django.db import models


# Payment Model
class Payment(models.Model):
    PAYMENT_CHOICES = [
        ('COD', 'Cash on Delivery'),
        ('Online', 'Online Payment'),
    ]

    method = models.CharField(max_length=20, choices=PAYMENT_CHOICES)
    amount = models.IntegerField()
    status = models.CharField(max_length=20, default='Paid')

    def __str__(self):
        return self.method


# Feedback Model
class Feedback(models.Model):
    name = models.CharField(max_length=100)
    rating = models.IntegerField()
    comment = models.TextField()

    def __str__(self):
        return self.name

# Food Model
class Food(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    category = models.CharField(max_length=100)
    image = models.ImageField(upload_to='menu/', null=True, blank=True)
 
    def __str__(self):
        return self.name
 
 
# Table Reservation
class TableReservation(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    date = models.DateField()
    time = models.TimeField()
    guests = models.IntegerField()
 
    def __str__(self):
        return self.name
 
 
# Kitchen Order
class KitchenOrder(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Preparing', 'Preparing'),
        ('Ready', 'Ready'),
        ('Served', 'Served'),
    ]
    food_name = models.CharField(max_length=100)
    quantity = models.IntegerField(default=1)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
 
    def __str__(self):
        return self.food_name