from django.shortcuts import render, get_object_or_404
from django.views import generic
from pigs.models import *
from pigs.forms import *
from django.utils import timezone
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.urls import reverse
from django.db.models import Sum, F
from django.db.models.functions import Coalesce
from pigs import models
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from collections import defaultdict
from django.views.decorators.cache import never_cache
from datetime import date
import json
import calendar
from django.db.models import FloatField
from django.db.models.functions import Cast
from django.template.loader import render_to_string
# Create your views here.


class indexview(LoginRequiredMixin, generic.ListView):
    model = Pigpen
    template_name = 'pigs/indexview.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sows'] = Sows.objects.all()
        return context


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
        context['latestpigs'] = getlatestpigchange(self.kwargs['pk'],1)
        return context


class pigsforpen(LoginRequiredMixin, generic.DetailView):
    model = Pigpen
    template_name = 'pigs/pigsforpen.html'

class deadcull(LoginRequiredMixin, generic.DetailView):
    model = Pigpen
    template_name = 'pigs/deadcull.html'

class shippedpigs(LoginRequiredMixin,generic.ListView):
    model = Shipped
    template_name = 'pigs/shipped.html' 

@login_required
@never_cache
def mixsheet(request,pigpen):
    if request.method == "GET":
        try:
            pigpk = pigration.objects.values_list('id', flat = True).filter(pigpen=pigpen).latest('date')
            pigpk += 1
        except:
            pigpk = "1"
        amount = request.GET['ration_amount']
        ration = request.GET['ration']
        ratdict = Ration.objects.filter(ration_number=ration).values()[0]
        rat = {}
        for k,v in ratdict.items():
            if k != 'feed_per_pig' and k != 'id' and k != 'ration_number':
                if int(v) != 0:
                    rat[k]= round(int(v)/ 2000 * int(amount))
   
        add = additives.objects.all().values_list('additivename').annotate(price=Cast(F('amount_per_ton'),FloatField()) / 2000 * int(amount))
    
        data = render_to_string('pigs/Mixsheet.html',{'rat':rat,'ration':ration, 'amount':amount, 'pigpen':pigpen,'add':add,'pigpk':pigpk})
        return HttpResponse(data)

@login_required
def additive(request,pigpen,id,addn):
    if request.method == 'GET':

        if 'amount' in request.GET:
            am = request.GET['amount']
       
        
        newprice = int(additives.objects.values_list('price',flat = True).get(additivename=addn)) * int(am)
        
        rationprice += newprice
        pigration.objects.get_or_create(pk=id)
        

        data = {"it worked"}
        return JsonResponse(data)
        

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
            ist.pigsinapen = piggy['id']

            for r in Ration.objects.filter(ration_number=ist.ration):
                for c in Commodity.objects.all():
                    try:
                        price += getattr(r, c.name)*c.price
                    except:
                        price = getattr(r, c.name)*c.price

            ist.ration_price = price / 2000 * ist.ration_amount

            for i in additives.objects.values_list('additivename',flat= True).all():
                if i in request.POST and request.POST[i].isnumeric():
                   k = int(additives.objects.values_list('price',flat = True).get(additivename=i)) * int(request.POST[i])
                   ist.ration_price += k
                   try:
                        ist.extras += ' ' + i[0] + request.POST[i]
                   except:
                        ist.extras = i[0] + request.POST[i]

            if not ist.date:
                ist.date = timezone.now()
            ist.save()
            
            return HttpResponseRedirect(reverse('pigs:pen', args=(pigpen)))
        else:

            return render(request, 'pigs/rationview.html',{'error':"That did not perform correctly!",'form':form,'pigpk':pigpk})


    else:
       
        try:
            rt = pigration.objects.values('ration').filter(pigpen=pigpen).latest('date')['ration']
            feed = pigration.objects.filter(pigpen=pigpen).filter(ration=rt).aggregate(Sum('ration_amount'))['ration_amount__sum']
            amount = int(Ration.objects.values_list('feed_per_pig', flat = True).get(ration_number=rt))
            try:
                pigs = int(Pigsinpen.objects.values_list('pigs', flat =True).get(id=piggy['id']))
            except:
                pigs = 0

            total = amount * pigs - feed

            if total < 50:
                
                 rt = Ration.objects.values_list('ration_number', flat = True).get(id = int(Ration.objects.values_list('id',flat = True).get(ration_number=rt)+1))
                 newamount = int(Ration.objects.values_list('feed_per_pig', flat = True).get(ration_number=rt))
                 total = pigs * newamount
              
            if total > 2500 and total < 5000:
                total = int(total / 2)
        
            if total > 2499:
                total = 2000
            total = round(total,-1)
            form = addrationform(initial={'ration_amount':total,'ration':rt})
        except:
            amount = int(Ration.objects.values_list('feed_per_pig', flat = True).get(id=1))
            rationame = Ration.objects.values_list('ration_number', flat = True).get(id=1)
            try:
                pigs = int(Pigsinpen.objects.values_list('pigs', flat =True).get(id=piggy['id']))
            except:
                pigs = 0
        
            total = amount * pigs

            if total > 4200 and total < 5000:
                total = int(total / 2)
        
            if total > 2499:
                total = 2000
            form= addrationform(initial={'ration_amount':total, 'ration':rationame})
        today = date.today()
        if pigration.objects.filter(pigpen=pigpen, date__month=today.month).count() == 0:
             messages.info(request,"Add Pork Performance!")

        return render(request, 'pigs/rationview.html',{'form':form,'pigpen':pigpen})

@login_required
def updateration(request,pigpen,rationid):
    instance = get_object_or_404(pigration, id=rationid)

    if request.method == 'POST':
        form = addrationform(request.POST, instance=instance)

        if form.is_valid():
            ist = form.save(commit=False)
            ist.pigpen = Pigpen.objects.get(pk= pigpen)

            for r in Ration.objects.filter(ration_number=ist.ration):
                for c in Commodity.objects.all():
                    try:
                        price += getattr(r, c.name)*c.price
                    except:
                        price = getattr(r, c.name)*c.price

            ist.ration_price = price / 2000 * ist.ration_amount

            for i in additives.objects.values_list('additivename',flat= True).all():
                if i in request.POST and request.POST[i].isnumeric():
                   k= int(additives.objects.values_list('price',flat = True).get(additivename=i)) * int(request.POST[i])
                   ist.ration_price += k
                   try:
                        ist.extras += ' ' + i[0] + request.POST[i]
                   except:
                        ist.extras = i[0] + request.POST[i]

            ist.save()
            return HttpResponseRedirect(reverse('pigs:pen', args=(pigpen)))
        else:

            return render(request, 'pigs/updateration.html',{'error':"That did not perform correctly!",'form':form,'pigpen':pigpen,'rationid':rationid})


    else:
        form = addrationform(instance=instance)
        return render(request, 'pigs/updateration.html',{'form':form,'pigpen':pigpen, 'rationid':rationid})

@login_required
def delete(request,pigpen,model):
    mod = getattr(models, model)
    mod.objects.latest('date').delete()
    return HttpResponseRedirect(reverse('pigs:pen', args=(pigpen)))

@login_required
def deleteration(request,pigpen,id):
    pigration.objects.filter(id=id).delete()
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
    pig_cost = round(pigcost / pigsbefore,2)

    if request.method =='POST':
        form = changepigsform(request.POST,instance=instance,pigpen=pigpen)

        if form.is_valid():
            ist = form.save(commit=False)
            ist.pigpen = Pigpen.objects.get(pk = pigpen)
            ist.pigs = form.cleaned_data['pigs']
            ist.pig_cost_total = form.cleaned_data['pig_cost_total'] * form.cleaned_data['pigs']
            if ist.notes == "":
                ist.notes = str(form.cleaned_data['pigs']) + ' Added'

            ist.date = timezone.now()
            ist.save()
            pigration.objects.filter(pigsinapen=pigsbefore).update(pigsinapen=str(pigsbefore + form.cleaned_data['pigs']))
            return HttpResponseRedirect(reverse('pigs:pen', args=(pigpen)))

        else:
            return render(request, 'pigs/pigupdateview.html',{'error':"That did not work",'form':form,'pigpen':pigpen,'pidid':pigid})


    else:
        form = changepigsform(instance = instance, pigpen=pigpen, initial={'pig_cost_total':pig_cost})
        return render(request, 'pigs/pigupdateview.html', {'form':form, 'pigpen':pigpen, 'pigid':pigid})

@login_required
def dead(request,pigpen):

    pigbefore= Pigsinpen.objects.values('id','pigs','pig_cost_total').filter(pigpen=pigpen).latest('date')
    pigsbefore = pigbefore['pigs']
    pigscost = pigbefore['pig_cost_total']



    if request.method =='POST':
        if 'amount' in request.POST:
            amount = request.POST['amount']

        if pigsbefore - int(amount) >= 0:

            
            dead = models.deadculled(pigpen= Pigpen.objects.get(pen= pigpen),dead = int(amount))
            dead.save()

            pigdead = models.Pigsinpen(pigpen= Pigpen.objects.get(pen=pigpen),pigs = pigsbefore - int(amount), pig_cost_total=pigscost,date=timezone.now(),notes= amount + " Dead")
            pigdead.save()


            return HttpResponseRedirect(reverse('pigs:pen', args=(pigpen)))
        else:
            messages.info(request,"Cant have less than 0 pigs!")
            return HttpResponseRedirect(reverse('pigs:pen', args=(pigpen)))

    else:
        messages.info(request, "Adding dead pig did not work. Please try again!")
        return HttpResponseRedirect(reverse('pigs:pen', args=(pigpen)))


@login_required
def culled(request,pigpen):
    pigbefore= Pigsinpen.objects.values('id','pigs','pig_cost_total').filter(pigpen=pigpen).latest('date')
    pigsbefore = pigbefore['pigs']
    pigscost = pigbefore['pig_cost_total']



    if request.method =='POST':
         if 'amount' in request.POST:
            amount = request.POST['amount']

            if pigsbefore - int(amount) >= 0:
                dead = models.deadculled(pigpen= Pigpen.objects.get(pen= pigpen),culled = int(amount))
                dead.save()

                pigdead = models.Pigsinpen(pigpen= Pigpen.objects.get(pen=pigpen),pigs = pigsbefore - int(amount), pig_cost_total=pigscost,date = timezone.now(),notes= "Culled " + amount)
                pigdead.save()
                return HttpResponseRedirect(reverse('pigs:pen', args=(pigpen)))

            else:
                messages.info(request,"Cant have less than 0 pigs!")
                return HttpResponseRedirect(reverse('pigs:pen', args=(pigpen)))


    else:
        messages.info(request, "Adding culled pig did not work. Please try again!")
        return HttpResponseRedirect(reverse('pigs:pen', args=(pigpen)))


@login_required
def movepigs(request,pigpen):

        pig = Pigsinpen.objects.filter(pigpen=pigpen).values('id','pigs').latest('date')
        pigid = pig['id']
        pignumber = pig['pigs']
        pigcost = Pigsinpen.objects.values('pig_cost_total').get(id= pigid)
        pigscost = pigcost['pig_cost_total']
        perpigcost = pigscost / pignumber
        piggypen = Pigpen.objects.get(pen=pigpen)
        pigrations = pigration.objects.values_list('ration','ration_amount','ration_price','date').filter(pigpen=pigpen).filter(pigsinapen = pigid)



        if request.method == 'POST':
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

                if pigafter != 0:
                    newpig = models.Pigsinpen(pigpen=piggypen,pigs=pigafter, pig_cost_total=perpigcost * pigafter, date=timezone.now(), notes='Moved ' + str(form.cleaned_data['pigs']) + ' to ' + str(form.cleaned_data['pigpen']))
                    newpig.save()

                    for key,value,price,date in pigrations:
                        ration = int(value / pignumber * pigafter)
                        oldprice = price / value * ration
                        newrationamount = int(value / pignumber * form.cleaned_data['pigs'])
                        newprice = price / value * newrationamount
                        pigration.objects.filter(pigpen=pigpen).filter(ration=key).update(ration_amount = ration,pigsinapen = newpig.id,ration_price = oldprice)
                        newration = models.pigration(pigpen = form.cleaned_data['pigpen'], ration=Ration.objects.get(ration_number=key),ration_price = newprice, pigsinapen=ist.id, ration_amount = newrationamount,date = date)
                        newration.save()
                else:

                    for ration,amount,price,date in pigrations:
                        toration = models.pigration(pigpen= form.cleaned_data['pigpen'], ration= Ration.objects.get(ration_number=ration),ration_price = price, pigsinapen=ist.id, ration_amount=amount,date=date)
                        toration.save()
                        

                    Pigsinpen.objects.filter(pigpen=pigpen).delete()
                    pigration.objects.filter(pigpen=pigpen).delete()
                    deadculled.objects.filter(pigpen=pigpen).delete()

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
        form = shippigsform(request.POST,pigpen=pigpen)

        if form.is_valid():
            ist = form.save(commit=False)
            ist.pigpen = Pigpen.objects.get(pk = pigpen)
            ist.pigs = pigsbefore - form.cleaned_data['pigs']
            ist.pig_cost_total = (pigscost / pigsbefore) * ist.pigs
            if ist.notes == "":
                ist.notes = str(form.cleaned_data['pigs']) + ' Shipped'

            ist.date = timezone.now()
            ist.save()

            pigafter = pigsbefore - form.cleaned_data['pigs']
            pigrations=pigration.objects.values_list('ration','ration_price','date').filter(pigpen=pigpen).filter(pigsinapen=id)
            ration = pigration.objects.filter(pigpen=pigpen).filter(pigsinapen=id).aggregate(total=Coalesce(Sum(F('ration_price')),0))['total']
            rationcost = ration / pigsbefore * form.cleaned_data['pigs']
            newpigration = defaultdict(int)

            for key,value,date in pigrations:

                    cost = value / pigsbefore * pigafter
                    shippedra= int(round(value / pigsbefore * form.cleaned_data['pigs'],2))
                    pigration.objects.filter(pigpen=pigpen).filter(ration=key).update(ration_price = cost,pigsinapen = ist.id)
                    newpigration[key] += shippedra

            newpigration = '; '.join(str(e) for e in newpigration.items())
            newpigration = str(newpigration)
            newpigration = newpigration.translate({ord(r): None for r in "defaulticns[]{}<>()'"})

            if pigafter == 0:
                de = str(deadculled.objects.filter(pigpen=pigpen).values_list('dead').aggregate(deads = Coalesce(Sum(F('dead')),0))['deads'])
                cu = str(deadculled.objects.filter(pigpen=pigpen).values_list('culled').aggregate(culls = Coalesce(Sum(F('culled')),0))['culls'])

            shipped = models.Shipped(pigpen=pigpen,pigs = form.cleaned_data['pigs'],sold_price = form.cleaned_data['sold_price'], pig_cost = pigscost / pigsbefore,ration_amount= newpigration,pig_ration_cost = rationcost,deadculls= de + '/' + cu)
            shipped.save()
            return HttpResponseRedirect(reverse('pigs:pen', args=(pigpen)))
        else:
            return render(request, 'pigs/Ship.html',{'error':"That did not work",'form':form,'pigpen':pigpen, 'pigid':id})


    else:
        form = shippigsform(pigpen=pigpen)
        return render(request, 'pigs/Ship.html', {'form':form, 'pigpen':pigpen, 'pigid':id})

def Chartview(request):
    pen_list = list(Pigpen.objects.all().values_list('pen',flat = True).order_by('pen'))
    return render(request, 'pigs/Charts.html',{'pen':pen_list})

@login_required
def chartdata(request):
    if 'pen' in request.GET:
        pen = request.GET['pen']
        

    prelabel = list(pigration.objects.filter(pigpen=pen).datetimes('date','month'))
    loop= [prelabel.month for prelabel in prelabel]
    label = []
    for prelabel in prelabel:
        label.append(str(calendar.month_abbr[prelabel.month]))
    items = []
    for i in loop:
        
        b = pigration.objects.filter(pigpen=pen).filter(date__month=i).aggregate(Sum('ration_amount'))['ration_amount__sum']
      
        items.append(b)
    

    data = {
        "labels": label,
        "items": items,
        }

    return JsonResponse(data)

@login_required
def feedcostperday(request):
    
    if 'pen' in request.GET:
        pen = request.GET['pen']

    prelabel = list(pigration.objects.filter(pigpen=pen).datetimes('date','day'))
    loop = [prelabel.day for prelabel in prelabel]
    labels = []
    for prelabel in prelabel:
        labels.append(str(prelabel.month) + "/" + str(prelabel.day))
    items = []
    for i in loop:
        b = pigration.objects.filter(pigpen=pen).filter(date__day=i).aggregate(Sum('ration_price'))['ration_price__sum']
        items.append(b)
   
    data = {
        "labels": labels,
        "items": items
        }

    return JsonResponse(data)
def allpenfeed(request):
    
    prelabel = list(pigration.objects.datetimes('date','month'))
    loop= [prelabel.month for prelabel in prelabel]
    label = []
    for prelabel in prelabel:
        label.append(str(calendar.month_abbr[prelabel.month]))
    items=[]
    for i in loop:
        
        b = pigration.objects.filter(date__month=i).aggregate(Sum('ration_amount'))['ration_amount__sum']
      
        items.append(b)
    

    data = {
        "labels": label,
        "items": items
        }

    return JsonResponse(data)

def pigletamount(sow):
    try:
        return piglets.objects.filter(Sow = sow).latest('born_date')
    except:
        return ''


class sowview(generic.DetailView):
    model = Sows
    template_name = 'pigs/sowview.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['piglets'] = pigletamount(self.kwargs['pk'])
        return context

def breedsows(request,sow):
    if request.method == "POST":
        form = breedsowform(request.POST)
        if form.is_valid():
            ist = form.save(commit=False)
            ist.Sow = Sows.objects.get(sow_id=sow)
            if not ist.date:
                ist.date = timezone.now()
            ist.save()
            Sows.objects.filter(sow_id=sow).update(bred=True)
            return HttpResponseRedirect(reverse('pigs:sow', args=(sow)))
        else:
            return render(request,'pigs/breedsow.html',{'sow':sow})
    else:
        form = breedsowform()
        return render(request,'pigs/breedsow.html',{'sow':sow,'form':form})

def tablereport(request):
    if "date" in request.GET:
        date = request.GET['date']

    if "pen" in request.GET:
        pen = request.GET['pen']

        if pen != 'All':
            rat = pigration.objects.values_list('ration').filter(pigpen=pen).filter(date__month=date).annotate(Sum(F('ration_amount')))
        else:
            rat = pigration.objects.values_list('ration').filter(date__month=date).annotate(Sum(F('ration_amount')))
        tabledata = render_to_string('pigs/tablereport.html', {'rat':rat})
        return HttpResponse(tabledata)


