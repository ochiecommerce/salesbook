from django import forms

from .models import Contact, InteractionLog

class InteractionForm(forms.ModelForm):
    class Meta:
        model = InteractionLog
        fields = ['notes']


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'id_number', 'employment_number', 'employer_name', 'phone', 'status']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'id_number': forms.TextInput(attrs={'class': 'form-control'}),
            'employment_number': forms.TextInput(attrs={'class': 'form-control'}),
            'employer_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
        }
