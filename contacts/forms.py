from django import forms

from .models import Contact, InteractionLog,  Group, Invite


class LoginForm(forms.BaseForm):
    email = forms.EmailInput(attrs={"class": "form-control"})
    password = forms.PasswordInput(attrs={"class": "form-control"})


class InteractionForm(forms.ModelForm):
    class Meta:
        model = InteractionLog
        fields = ["feedback_title", "notes"]


class ContactForm(forms.ModelForm):
    id_number = forms.IntegerField(required=False,min_value=1000000)
    employment_number = forms.IntegerField(required=False)
    employer_name = forms.CharField(required=False)
    class Meta:
        model = Contact
        fields = [
            "name",
            "id_number",
            "employment_number",
            "employer_name",
            "phone",
            "status",
        ]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "id_number": forms.TextInput(attrs={"class": "form-control"}),
            "employment_number": forms.TextInput(attrs={"class": "form-control"}),
            "employer_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "phone": forms.TextInput(attrs={"class": "form-control"}),
        }


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ["name"]


class InviteForm(forms.ModelForm):
    class Meta:
        model = Invite
        fields = ["user"]
        widgets = {"username": forms.TextInput(attrs={"class": "form-control me-2"})}
