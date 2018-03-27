from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save
from pigs.models import *
import uuid




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
    id = models.PositiveIntegerField(primary_key=True)
    ration_number = models.CharField(max_length=15, unique=True)
    feed_per_pig = models.CharField(max_length=3,default = 55)
    created = False
    def __str__(self):
      return self.ration_number
    class Meta:
        ordering = ['id']

for i in Commodity.objects.all(): 
    Ration.add_to_class(i.name,models.PositiveIntegerField(default=0))   


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
    deadculls = models.CharField(max_length=40,blank=True,null=True)
    shipped_date = models.DateTimeField(auto_now_add=True)
    notes = models.CharField(max_length=300,blank=True,null=True)


class Sows(models.Model):
    sow_id = models.CharField(max_length=50,primary_key=True)
    secondary_id = models.CharField(max_length=50)
    description = models.CharField(max_length=300,null=True,blank=True)
    birth_date = models.DateField()
    bred = models.NullBooleanField(null=True,blank=True)
    farrowing = models.NullBooleanField(null=True,blank=True)
    def __str__(self):
        return self.sow_id

class boars(models.Model):
    boar_number = models.PositiveIntegerField()
    boar_secondaryid = models.CharField(max_length=50,null=True,blank=True)
    birth_date = models.DateField()
    def __str__(self):
        return str(self.boar_number)

class breed(models.Model):
    Sow = models.ForeignKey(Sows,on_delete=models.CASCADE)
    by_boar = models.ForeignKey(boars,on_delete=models.CASCADE)
    date = models.DateField()
    def __str__(self):
        return self.status

class piglets(models.Model):
    Sow = models.ForeignKey(Sows,on_delete=models.CASCADE)
    born_date = models.DateField()
    born = models.PositiveIntegerField()
    alive = models.PositiveIntegerField()
    dead = models.PositiveIntegerField(null=True,blank= True)
    culled = models.PositiveIntegerField(null=True,blank=True)
    wean = models.PositiveIntegerField(null=True,blank=True)
    wean_date = models.DateField(null=True,blank=True)

class operation(models.Model):
    operation_name = models.CharField(max_length=50)
    def __str__(self):
        return self.operation_name

class pigletoperation(models.Model):
    piglet = models.ForeignKey(piglets,on_delete=models.CASCADE)
    operation = models.ForeignKey(operation,on_delete=models.CASCADE)
    date = models.DateField()
    def __str__(self):
        return self.operation

class weanedpiglets(models.Model):
    Sowid = models.ForeignKey(Sows,on_delete=models.CASCADE)
    born_date = models.DateField()
    weaned = models.PositiveIntegerField()
    dead = models.PositiveIntegerField()
    culled = models.PositiveIntegerField()
    wean_date = models.DateField()
