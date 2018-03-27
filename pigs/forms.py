from django import forms
from pigs.models import *

class addrationform(forms.ModelForm):
    
    class Meta:
        model = pigration
        fields = ['ration', 'ration_amount','date']
        exclude = {'pigpen','pigsinpen'}
        widgets = {'ration_amount': forms.NumberInput(),'date': forms.DateInput(attrs={'type': 'date','default':timezone.now})}
        labels = {'ration_amount': 'Amount'}


class changepigsform(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        pigpen = kwargs.pop("pigpen")
        super(changepigsform,self).__init__(*args,**kwargs)
        self.fields['pigs'] = forms.IntegerField(max_value=Pigsinpen.objects.values('pigs').filter(pigpen=pigpen).latest('date')['pigs'])
       
    class Meta:
        model = Pigsinpen
        fields= ['pigs','notes']
        exclude = {'pigpen'}
        

class addpigsform(forms.ModelForm):
    
    class Meta:
        model = Pigsinpen
        fields = ['pigs','pig_cost_total','notes']
        exclude = {'pigpen'} 
        labels = {'pig_cost_total': 'Cost Per Pig'}

class movepigsform(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        pigpen = kwargs.pop("pigpen")
        super(movepigsform,self).__init__(*args,**kwargs)
        self.fields['pigs'] = forms.IntegerField(max_value=Pigsinpen.objects.values('pigs').filter(pigpen=pigpen).latest('date')['pigs'])
    class Meta:
        model = Pigsinpen
        fields = ['pigpen','pigs','notes']
        labels = {'pigpen': "To Pigpen:"}
      
class shippigsform(forms.ModelForm):

    def __init__(self,*args,**kwargs):
        pigpen = kwargs.pop("pigpen")
        super(shippigsform,self).__init__(*args,**kwargs)
        self.fields['pigs'] = forms.IntegerField(max_value=Pigsinpen.objects.values('pigs').filter(pigpen=pigpen).latest('date')['pigs'])
   
    sold_price= forms.CharField()

    class Meta:
        model = Pigsinpen
        fields= ['pigs','notes']
        exclude = {'pigpen'}

class addpigletsform(forms.ModelForm):
    class Meta:
        model = piglets
        feilds = ['born_date','born','alive','dead','culled','wean','wean_date']
        exclude = {'Sow'}
           
class breedsowform(forms.ModelForm):
    class Meta:
        model = breed
        feilds = ['by_boar','date']
        exclude = {'Sow'}
        widgets = {'date': forms.DateInput(attrs={'type': 'date','default':timezone.now})}