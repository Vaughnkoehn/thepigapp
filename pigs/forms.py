from django import forms
from pigs.models import *

class addrationform(forms.ModelForm):
    
    class Meta:
        model = pigration
        fields = ['ration', 'ration_amount','date']
        exclude = {'pigpen','pigsinpen'}
        widgets = {'ration_amount': forms.NumberInput(attrs={'step': '10',}),'date': forms.DateInput(attrs={'type': 'date','default':timezone.now})}
      


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

class movepigsform(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        pigpen = kwargs.pop("pigpen")
        super(movepigsform,self).__init__(*args,**kwargs)
        self.fields['pigs'] = forms.IntegerField(max_value=Pigsinpen.objects.values('pigs').filter(pigpen=pigpen).latest('date')['pigs'])
    class Meta:
        model = Pigsinpen
        fields = ['pigpen','pigs','notes']
       

            