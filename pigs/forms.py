from django import forms
from pigs.models import *

class addrationform(forms.ModelForm):
    class Meta:
        model = pigration
        fields = ['ration', 'ration_amount']
        exclude = {'pigpen','pigsinpen'}
        widgets = {'ration_amount': forms.NumberInput(attrs={'step': '10','default':'2000'}),}


class changepigsform(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        pigpen = kwargs.pop("pigpen")
        super(changepigsform,self).__init__(*args,**kwargs)
        self.fields['pigs'] = forms.IntegerField(max_value=Pigsinpen.objects.values('pigs').filter(pigpen=pigpen).latest('date')['pigs'])
    class Meta:
        model = Pigsinpen
        fields= ['pigs','notes']
        exclude = {'pigpen','pig_cost_total'}

class addpigsform(forms.ModelForm):
    
    class Meta:
        model = Pigsinpen
        fields = ['pigs','notes','pig_cost_total']
        exclude = {'pigpen'} 

class movepigsform(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        pigpen = kwargs.pop("pigpen")
        super(movepigsform,self).__init__(*args,**kwargs)
        self.fields['pigs'] = forms.IntegerField(max_value=Pigsinpen.objects.values('pigs').filter(pigpen=pigpen).latest('date')['pigs'])
    class Meta:
        model = Pigsinpen
        fields = ['pigpen','pigs','notes']
       

            