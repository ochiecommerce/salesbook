from django import forms

from .models import Contact


class LoginForm(forms.BaseForm):
    email = forms.EmailInput(attrs={"class": "form-control"})
    password = forms.PasswordInput(attrs={"class": "form-control"})


class ContactForm(forms.ModelForm):
    id_number = forms.IntegerField(required=False,min_value=1000000)
    employment_number = forms.IntegerField(required=False)
    employer_name = forms.CharField(required=False)
    class Meta:
        model = Contact
        fields = [
            "name",
            "phone",
            "status",
        ]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "phone": forms.TextInput(attrs={"class": "form-control"}),
        }
