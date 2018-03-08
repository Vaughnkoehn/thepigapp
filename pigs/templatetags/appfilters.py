from django import template
from pigs.models import *
from django.db.models import Sum, F
import datetime
from itertools import chain
import re
from django.db.models import Count
from django.db.models.functions import Coalesce
register = template.Library()



@register.simple_tag
def getfeed(ration,pigpen,inpen,date):
    rat = pigration.objects.filter(pigpen=pigpen).filter(ration=ration).filter(date__lte=date).aggregate(Sum('ration_amount'))
    feed = rat['ration_amount__sum']
    amount = int(Ration.objects.values_list('feed_per_pig', flat = True).get(ration_number=ration))
    try:
        pigs = int(Pigsinpen.objects.filter(pigpen=pigpen).filter(id=inpen).values_list('pigs', flat =True).latest('date'))
    except:
        pigs = 0
    return amount*pigs-feed

@register.simple_tag
def deleteration(instance):
   return pigration.objects.get(id=instance).delete()
   
@register.simple_tag
def cost(pigpen,pigs,pigs_in_pen):
    try:
        return round(pigration.objects.filter(pigpen=pigpen).filter(pigsinapen=pigs).aggregate(total = Sum('ration_price'))['total'] / pigs_in_pen ,2)
    except:
        return 0
    

@register.simple_tag
def totalcost(pigpen):
   try:
        return round(pigration.objects.filter(pigpen=pigpen).aggregate(total= Sum('ration_price'))['total'],2)
       
   except:
        return 0

@register.filter
def divide(value,key):
  
        return round(value / key,2)
    

@register.simple_tag
def ration(pigpen,pigs):
    result = ("; ".join(str(e) for e in list(pigration.objects.values_list('ration').filter(pigpen=pigpen).filter(pigsinapen = pigs).annotate(Sum('ration_amount')).order_by('date'))))
    return result.translate({ord(r): None for r in "(')"})

@register.simple_tag
def rationtotal(pigpen):
     result = ("; ".join(str(e) for e in list(pigration.objects.values_list('ration').order_by('ration').filter(pigpen=pigpen).annotate(Sum('ration_amount')))))
     return result.translate({ord(r): None for r in "(')"})

@register.simple_tag
def deads(pigpen,date):
    d = str(deadculled.objects.filter(pigpen=pigpen).filter(date__lte=date).values_list('dead').aggregate(deads = Coalesce(Sum(F('dead')),0)))
    mod = d.translate({ord(r): None for r in "{}'"}) 
    return mod

@register.simple_tag
def culls(pigpen,date):
    c = str(deadculled.objects.filter(pigpen=pigpen).filter(date__lte=date).values_list('culled').aggregate(culls = Coalesce(Sum(F('culled')),0)))
    mod = c.translate({ord(r): None for r in "{}'"}) 
    return mod

@register.simple_tag
def totaldead(pigpen,date):
    td = deadculled.objects.filter(pigpen=pigpen).filter(date__lte=date).aggregate(total=Coalesce(Sum(F('culled')),0) + Coalesce(Sum(F('dead')),0))['total']
    return td
