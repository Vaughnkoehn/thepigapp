from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
# Create your models here.



class Pigpen(models.Model):
    pen = models.CharField(max_length=2)
    def __str__(self):
        return self.pen

class Ration(models.Model):
   
    ration_text = models.CharField(max_length=2)
    ration_price = models.DecimalField(max_digits=19,decimal_places=4)
    feed_per_pig = models.CharField(max_length=3,default = 55)
    milo = models.CharField(max_length=4)
    sbm = models.CharField(max_length=4)
    dynamin = models.CharField(max_length=3,default = 0)
    pigpak = models.CharField(max_length=3,default = 0)
    sixtyeighty = models.CharField(max_length=3,default = 0)
    control = models.CharField(max_length=3,default = 0)
    optimax = models.CharField(max_length=3,default = 0)
    molderase = models.CharField(max_length=3,default = 0)
    hitpork = models.CharField(max_length=3,default = 0)
    oats = models.CharField(max_length=3,default = 0)
    sowonehundred = models.CharField(max_length=3,default = 0)
    porkperformance = models.CharField(max_length=3,default = 0)
    safeguard = models.CharField(max_length=3,default = 0)                      
    spicepak = models.CharField(max_length=3,default = 0)
    def __str__(self):
        return self.ration_text

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
    ration = models.ForeignKey(Ration, on_delete=models.CASCADE)
    pigsinapen = models.CharField(max_length=4)
    ration_amount = models.IntegerField()
    date = models.DateTimeField()

class deadculled(models.Model):
    pigpen = models.ForeignKey(Pigpen, on_delete=models.CASCADE)
    dead = models.PositiveIntegerField(null = True,blank = True)
    culled = models.PositiveIntegerField(null=True, blank= True)
    date = models.DateTimeField(auto_now_add = True)
    

class Shipped(models.Model):
    pigpen = models.PositiveIntegerField()
    pigs = models.PositiveIntegerField()
    pig_cost = models.DecimalField(max_digits=6, decimal_places=2)
    ration_amount = models.CharField(max_length=500)
    pig_ration_cost = models.DecimalField(max_digits=6,decimal_places=2)
    shipped_date = models.DateTimeField(auto_now_add=True)
    notes = models.CharField(max_length=300,blank=True,null=True)