from django.shortcuts import render, get_object_or_404
from django.views import generic
from pigs.models import *
from pigs.forms import *
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.db.models import Sum, F
from django.db.models.functions import Coalesce
from pigs import models
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from collections import defaultdict
from django.views.decorators.cache import never_cache
# Create your views here.


class indexview(LoginRequiredMixin, generic.ListView):
    model = Pigpen
    template_name = 'pigs/indexview.html'
   
      
def getlatestpigchange(pigpen,number):
    try:
        latestpigs = Pigsinpen.objects.values('id','pigs','pig_cost_total','date','notes').filter(pigpen=pigpen).order_by('-date')[:number]
       
    except:
        latestpigs = '0'
    return latestpigs

class penview(LoginRequiredMixin, generic.DetailView):
    model = Pigpen
    template_name = 'pigs/penview.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pens'] = Pigpen.objects.all()
        context['latestpigs'] = getlatestpigchange(self.kwargs['pk'],3)
        return context


class pigsforpen(LoginRequiredMixin, generic.DetailView):
    model = Pigpen
    template_name = 'pigs/pigsforpen.html'

class shippedpigs(LoginRequiredMixin,generic.ListView):
    model = Shipped
    template_name = 'pigs/shipped.html'

@login_required
@never_cache
def addration(request,pigpen):
   
    try:
        piggy = Pigsinpen.objects.values('id').filter(pigpen=pigpen).latest('date') 
        pig = Pigsinpen.objects.filter(pigpen=pigpen).latest('date')
    except:
        messages.info(request,'Please add pigs!')
        return  HttpResponseRedirect(reverse('pigs:pen', args=(pigpen))) 

    
    if request.method == 'POST':
        form = addrationform(request.POST)
        
        if form.is_valid():
            ist = form.save(commit=False)
            ist.pigpen = Pigpen.objects.get(pk= pigpen)
            ist.pigs = pig
            ist.pigsinapen = piggy['id']
            if not ist.date:
                ist.date = timezone.now()

            ist.save()
            return HttpResponseRedirect(reverse('pigs:pen', args=(pigpen)))
        else:
            
            return render(request, 'pigs/rationview.html',{'error':"That did not perform correctly!",'form':form})


    else:
        form = addrationform()
        return render(request, 'pigs/rationview.html',{'form':form,'pigpen':pigpen})

@login_required
def updateration(request,pigpen,rationid):
    instance = get_object_or_404(pigration, id=rationid)

    if request.method == 'POST':
        form = addrationform(request.POST, instance=instance)
        
        if form.is_valid():
            ist = form.save(commit=False)
            ist.pigpen = Pigpen.objects.get(pk= pigpen)
            ist.save()
            return HttpResponseRedirect(reverse('pigs:pen', args=(pigpen)))
        else:
            
            return render(request, 'pigs/updateration.html',{'error':"That did not perform correctly!",'form':form,'pigpen':pigpen,'rationid':rationid})


    else:
        form = addrationform(instance=instance)
        return render(request, 'pigs/updateration.html',{'form':form,'pigpen':pigpen, 'rationid':rationid})

@login_required
def delete(request,pigpen,model,rationid):
    mod = getattr(models, model)
    mod.objects.get(id=rationid).delete()
    return HttpResponseRedirect(reverse('pigs:pen', args=(pigpen)))
@login_required
def deleteallfrompen(request,pigpen):
    Pigsinpen.objects.filter(pigpen=pigpen).delete()
    pigration.objects.filter(pigpen=pigpen).delete()
    deadculled.objects.filter(pigpen=pigpen).delete()
    return HttpResponseRedirect(reverse('pigs:pen', args=(pigpen)))


@login_required
def changepigs(request,pigpen):
    if request.method == 'POST':
        form = addpigsform(request.POST)

        if Pigsinpen.objects.filter(pigpen=pigpen).exists():
            pig = Pigsinpen.objects.values('pigs').filter(pigpen=pigpen).latest('date')
            pigs = pig['pigs']
            pigcost = Pigsinpen.objects.values('pig_cost_total').filter(pigpen=pigpen).latest('date')
            pigscost = pigcost['pig_cost_total']
        else:
            pigs = 0
            pigscost = 0

        if form.is_valid():
            ist = form.save(commit=False)
            ist.pigpen = Pigpen.objects.get(pk = pigpen)
            ist.pigs = pigs + form.cleaned_data['pigs']
            ist.pig_cost_total = pigscost + form.cleaned_data['pig_cost_total'] * form.cleaned_data['pigs']
            ist.date = timezone.now()
            ist.save()
            return HttpResponseRedirect(reverse('pigs:pen', args=(pigpen)))
        else:
            return render(request, 'pigs/pigaddview.html',{'error':"That did not work",'form':form, 'pigpen':pigpen})


    else:
        form = addpigsform()
        return render(request, 'pigs/pigaddview.html', {'form':form, 'pigpen':pigpen})


@login_required
def updatepigs(request,pigpen,pigid):
    instance = get_object_or_404(Pigsinpen, id=pigid)
    pigbefore = Pigsinpen.objects.values('pigs').get(id = pigid)
    pigsbefore = pigbefore['pigs']
    pigcost = Pigsinpen.objects.values('pig_cost_total').get(id=pigid)['pig_cost_total']
    

    if request.method =='POST':
        form = changepigsform(request.POST,instance=instance,pigpen=pigpen)

        if form.is_valid():
            ist = form.save(commit=False)
            ist.pigpen = Pigpen.objects.get(pk = pigpen)
            ist.pigs = pigsbefore + form.cleaned_data['pigs']
            ist.pig_cost_total = pigcost
            if ist.notes == "":
                ist.notes = str(form.cleaned_data['pigs']) + ' Added'

            ist.date = timezone.now()
            ist.save()
            pigration.objects.filter(pigsinpen=pigsbefore).update(pigsinpen=str(pigsbefore + form.cleaned_data['pigs']))
            return HttpResponseRedirect(reverse('pigs:pen', args=(pigpen)))
            
        else:
            return render(request, 'pigs/pigupdateview.html',{'error':"That did not work",'form':form,'pigpen':pigpen,'pidid':pigid})


    else:
        form = changepigsform(instance = instance, pigpen=pigpen)
        return render(request, 'pigs/pigupdateview.html', {'form':form, 'pigpen':pigpen, 'pigid':pigid})

@login_required
def dead(request,pigpen,pigid):
    pigbefore= Pigsinpen.objects.values('id','pigs','pig_cost_total').get(id=pigid)
    pigsbefore = pigbefore['pigs']
    pigscost = pigbefore['pig_cost_total']
    id = pigbefore['id']

   
    if request.method =='POST':
        form = changepigsform(request.POST,pigpen=pigpen)

        if form.is_valid():

            ist = form.save(commit=False)
            ist.pigpen = Pigpen.objects.get(pk = pigpen)
            ist.pigs = pigsbefore - form.cleaned_data['pigs']
            try:
                ist.pig_cost_total = pigscost + (pigsbefore / pigscost * (pigsbefore - form.cleaned_data['pigs']))
            except:
                ist.pig_cost_total = 0
            if ist.notes == "":
                ist.notes = str(form.cleaned_data['pigs']) + ' Died'
           
            ist.date = timezone.now()
            ist.save()
            pigration.objects.filter(pigsinapen=id).update(pigsinapen = ist.id)
            dead = models.deadculled(pigpen= Pigpen.objects.get(id= pigpen),dead = form.cleaned_data['pigs'])
            dead.save() 
            return HttpResponseRedirect(reverse('pigs:pen', args=(pigpen)))
        else:
            return render(request, 'pigs/pigupdateview.html',{'error':"That did not work",'form':form,'pigpen':pigpen,'pidid':pigid})


    else:
        form = changepigsform(pigpen=pigpen)
        return render(request, 'pigs/pigupdateview.html', {'form':form, 'pigpen':pigpen, 'pigid':pigid})


@login_required
def culled(request,pigpen,pigid):
    pigbefore= Pigsinpen.objects.values('id','pigs','pig_cost_total').get(id=pigid)
    pigsbefore = pigbefore['pigs']
    pigscost = pigbefore['pig_cost_total']
    id = pigbefore['id']

   
    if request.method =='POST':
        form = changepigsform(request.POST,pigpen=pigpen)

        if form.is_valid():

            ist = form.save(commit=False)
            ist.pigpen = Pigpen.objects.get(pk = pigpen)
            ist.pigs = pigsbefore - form.cleaned_data['pigs']
            try:
                ist.pig_cost_total = pigscost + (pigsbefore / pigscost * (pigsbefore - form.cleaned_data['pigs']))
            except:
                ist.pig_cost_total = 0
            if ist.notes == "":
                ist.notes = str(form.cleaned_data['pigs']) + ' Culled'
           
            ist.date = timezone.now()
            ist.save()
            pigration.objects.filter(pigsinapen=id).update(pigsinapen = ist.id)
            culled = models.deadculled(pigpen= Pigpen.objects.get(id= pigpen), culled = form.cleaned_data['pigs'])
            culled.save()
            return HttpResponseRedirect(reverse('pigs:pen', args=(pigpen)))
        else:
            return render(request, 'pigs/pigupdateview.html',{'error':"That did not work",'form':form,'pigpen':pigpen,'pidid':pigid})


    else:
        form = changepigsform(pigpen=pigpen)
        return render(request, 'pigs/pigupdateview.html', {'form':form, 'pigpen':pigpen, 'pigid':pigid})

@login_required
def movepigs(request,pigpen):

        pig = Pigsinpen.objects.filter(pigpen=pigpen).values('id','pigs').latest('date')
        pigid = pig['id']
        pignumber = pig['pigs']
        pigcost = Pigsinpen.objects.values('pig_cost_total').get(id= pigid)
        pigscost = pigcost['pig_cost_total']
        perpigcost = pigscost / pignumber
        piggypen = Pigpen.objects.get(id=pigpen)
        pigrations = pigration.objects.values_list('ration','ration_amount','date').filter(pigpen=pigpen).filter(pigsinapen = pigid)
        

       
        if request.method =='POST':
            form = movepigsform(request.POST,pigpen=pigpen)

            if form.is_valid():
                ist = form.save(commit=False)
                ist.pig_cost_total = pigscost / pignumber * form.cleaned_data['pigs']

                try:
                   pigs = Pigsinpen.objects.values('pigs').filter(pigpen = ist.pigpen).latest('date')['pigs']
                except:
                    pigs = 0
                
                ist.pigs = form.cleaned_data['pigs'] + pigs
                if ist.notes == "":
                    ist.notes = str(form.cleaned_data['pigs']) + ' added from pen ' + pigpen

                ist.date = timezone.now()
                ist.save()

                pigafter = pignumber-form.cleaned_data['pigs']
               
                newpig = models.Pigsinpen(pigpen=piggypen,pigs=pigafter, pig_cost_total=perpigcost * pigafter, date=timezone.now(), notes='Moved ' + str(form.cleaned_data['pigs']) + ' to ' + str(form.cleaned_data['pigpen']))
                newpig.save()

                for key,value,date in pigrations:
                    ration = value / pignumber * pigafter
                    newrationamount = value / pignumber * form.cleaned_data['pigs']
                    pigration.objects.filter(pigpen=pigpen).filter(ration=key).update(ration_amount = ration,pigsinapen = newpig.id)
                    newration = models.pigration(pigpen= form.cleaned_data['pigpen'], ration=Ration.objects.get(id=key),pigsinapen=ist.id, ration_amount = newrationamount,date = date)
                    newration.save()

               
                return HttpResponseRedirect(reverse('pigs:pen', args=(pigpen)))
            
            else:
                return render(request, 'pigs/pigmoveview.html',{'error':"That did not work",'form':form,'pigpen':pigpen})


        else:
            form = movepigsform(pigpen=pigpen)
            return render(request, 'pigs/pigmoveview.html', {'form':form, 'pigpen':pigpen})

@login_required
def shippigs(request,pigpen):
    pigbefore= Pigsinpen.objects.values('id','pigs','pig_cost_total').filter(pigpen=pigpen).latest('date')
    pigsbefore = pigbefore['pigs']
    pigscost = pigbefore['pig_cost_total']
    id = pigbefore['id']
  
    if request.method =='POST':
        form = changepigsform(request.POST,pigpen=pigpen)

        if form.is_valid():
            ist = form.save(commit=False)
            ist.pigpen = Pigpen.objects.get(pk = pigpen)
            ist.pigs = pigsbefore - form.cleaned_data['pigs']
            ist.pig_cost_total = (pigscost / pigsbefore) * form.cleaned_data['pigs']
            if ist.notes == "":
                ist.notes = str(form.cleaned_data['pigs']) + ' Shipped'

            ist.date = timezone.now()
            ist.save()
            
            pigafter = pigsbefore - form.cleaned_data['pigs']
            pigrations=pigration.objects.values_list('ration','ration_amount','date').filter(pigpen=pigpen).filter(pigsinapen=id)
            ration = pigration.objects.filter(pigpen=pigpen).filter(pigsinapen=id).aggregate(total=Coalesce(Sum(F('ration__ration_price') * F('ration_amount')),0))['total']
            rationcost = ration / pigsbefore * form.cleaned_data['pigs']
            newpigration = defaultdict(int)

            for key,value,date in pigrations:
              
                    ration = value / pigsbefore * pigafter
                    newrationamount = int(round(value / pigsbefore * form.cleaned_data['pigs'],1))
                    pigration.objects.filter(pigpen=pigpen).filter(ration=key).update(ration_amount = ration,pigsinapen = ist.id)
                    newpigration[key] += newrationamount
            newpigration = '; '.join(str(e) for e in newpigration.items())
            newpigration = str(newpigration)
            newpigration = newpigration.translate({ord(r): None for r in "defaultictns[]{}<>()'"})
     
            shipped = models.Shipped(pigpen=pigpen,pigs = form.cleaned_data['pigs'],pig_cost = pigscost/pigsbefore,ration_amount= newpigration,pig_ration_cost = rationcost) 
            shipped.save()
            return HttpResponseRedirect(reverse('pigs:pen', args=(pigpen)))
        else:
            return render(request, 'pigs/Ship.html',{'error':"That did not work",'form':form,'pigpen':pigpen, 'pigid':id})


    else:
        form = changepigsform(pigpen=pigpen)
        return render(request, 'pigs/Ship.html', {'form':form, 'pigpen':pigpen, 'pigid':id})
        