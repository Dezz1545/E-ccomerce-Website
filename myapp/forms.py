from django import forms
from .models import Contact


class Contactform(forms.ModelForm):
        nom = forms.CharField(initial =  'your name' ,widget=forms.TextInput(attrs={
        'class':'form-control',}))
        email = forms.EmailField(initial =  'email' ,widget=forms.TextInput(attrs={
        'class':'form-control',}))
        objet = forms.CharField(initial =  'subject' ,widget=forms.TextInput(attrs={
        'class':'form-control',}))

        message= forms.CharField(initial =  'message' ,widget= forms.Textarea(attrs={
            'rows': '4',
            'class':'form-control',
        }))
        class Meta:
            model= Contact
            fields=('nom','email','objet','message')