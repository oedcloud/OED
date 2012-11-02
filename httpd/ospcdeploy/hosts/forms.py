#!/usr/bin/env pythoni
from django import forms
from models import Hosts
#from django.core.exceptions import ValidationError

#CHOICE = (('1','CC, KEYSTONE'), ('2','DASHBOARD'),('3','GLANCE'),('4','NC'))
CHOICE = (('1','CC, KEYSTONE,DASHBOARD,GLANCE'),('2','NC'))

class HostForm(forms.ModelForm):
    #hostname = forms.CharField(max_length=20)
    hostname = forms.ModelChoiceField(queryset=Hosts.objects.all(), error_messages={'required': 'Please choose the hostname'}, required=True)
    role = forms.ChoiceField(widget=forms.Select, choices=CHOICE)
    
    class Meta:
        model = Hosts
        fields = ('hostname','role')
    
    def __init__(self, *args,**kwargs):
        super(HostForm, self).__init__(*args,**kwargs)
        #self.fields['hostname']
    
    def clean_hostname(self):
        data = self.cleaned_data['hostname']
        if data == None :
            raise  forms.ValidationError('Hostname is required.') 
        else:
            print "the data is %s" % data
        
        return data
        
    def clean_role(self):
        data = self.cleaned_data['role']
        if data != '2': 
            if Hosts.objects.filter(role=data).count() > 0:
                raise  forms.ValidationError('Role CC already exists.')
        return data
