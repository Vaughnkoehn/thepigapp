from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save
from pigs.models import *
import uuid
# Create your models here.



class Pigpen(models.Model):
    pen = models.CharField(max_length=2,primary_key=True)
    def __str__(self):
        return str(self.pen)
    class Meta:
        ordering = ['pen']


class Commodity(models.Model):
    name = models.CharField(max_length=20,unique=True)
    price = models.DecimalField(max_digits=19,decimal_places=4)
    def __str__(self):
        return self.name

class Ration(models.Model):

    ration_number = models.CharField(max_length=15, unique=True)
    feed_per_pig = models.CharField(max_length=3,default = 55)
    created = False
    def __str__(self):
      return self.ration_number
for i in Commodity.objects.all():
    Ration.add_to_class(i.name,models.PositiveIntegerField(default=0))


   # milo = models.CharField(max_length=4)
   # sbm = models.CharField(max_length=4)
   # dynamin = models.CharField(max_length=3,default = 0)
   # pigpak = models.CharField(max_length=3,default = 0)
   # sixtyeighty = models.CharField(max_length=3,default = 0)
   # control = models.CharField(max_length=3,default = 0)
   # optimax = models.CharField(max_length=3,default = 0)
   # molderase = models.CharField(max_length=3,default = 0)
   # hitpork = models.CharField(max_length=3,default = 0)
   # oats = models.CharField(max_length=3,default = 0)
   # sowonehundred = models.CharField(max_length=3,default = 0)
   # porkperformance = models.CharField(max_length=3,default = 0)
   # spicepak = models.CharField(max_length=3,default = 0)
   # safeguard = models.CharField(max_length=3,default=0)


class additives(models.Model):
    additivename = models.CharField(max_length=20,unique=True)
    price = models.DecimalField(max_digits=19, decimal_places=4)
    amount_per_ton = models.DecimalField(max_digits=19, decimal_places=4)
    def __str__(self):
        return str(self.additivename)

class Pigsinpen(models.Model):
    pigpen = models.ForeignKey(Pigpen,on_delete=models.CASCADE)
    pigs = models.PositiveIntegerField()
    pig_cost_total = models.DecimalField(max_digits=6,decimal_places=2)
    date = models.DateTimeField()
    notes = models.CharField(max_length = 300,blank=True,null = True)
    def __str__(self):
        return str(self.pigs)

class pigration(models.Model):
    pigpen = models.ForeignKey(Pigpen, on_delete= models.CASCADE)
    ration = models.ForeignKey(Ration, on_delete=models.CASCADE,to_field='ration_number')
    ration_price = models.DecimalField(max_digits=19, decimal_places=4)
    pigsinapen = models.CharField(max_length=4)
    extras = models.CharField(max_length=15, null = True, blank=True)
    ration_amount = models.IntegerField()
    date = models.DateTimeField(blank=True)
    def __str__(self):
        return "Pen " + str(self.pigpen)+ " Ration " + str(self.ration)

class deadculled(models.Model):
    pigpen = models.ForeignKey(Pigpen, on_delete=models.CASCADE)
    dead = models.PositiveIntegerField(null = True,blank = True)
    culled = models.PositiveIntegerField(null=True, blank= True)
    date = models.DateTimeField(auto_now_add = True)


class Shipped(models.Model):
    pigpen = models.PositiveIntegerField()
    pigs = models.PositiveIntegerField()
    sold_price = models.DecimalField(max_digits=6,decimal_places=2)
    pig_cost = models.DecimalField(max_digits=6, decimal_places=2)
    ration_amount = models.CharField(max_length=500)
    pig_ration_cost = models.DecimalField(max_digits=6,decimal_places=2)
    shipped_date = models.DateTimeField(auto_now_add=True)
    notes = models.CharField(max_length=300,blank=True,null=True)