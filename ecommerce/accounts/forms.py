from django import forms

from accounts.models import UserProfile
from django.contrib.auth import get_user_model
from django.forms import DateInput


User = get_user_model()


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields ='__all__'
        widgets = {
            'date': DateInput(attrs={'type': 'date','class':'form-control'}),
            'name': forms.TextInput(attrs={'class':'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'confirm_password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'gender':forms.Select(attrs={'class':'form-control'}),




        }
    def clean_email(self):
        email = self.cleaned_data.get("email")
        qs = UserProfile.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("Email already Exist")
        else:
            return email

    def clean(self):
        data = self.cleaned_data
        print(data)
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")
        print(password)
        print(confirm_password)
        if password != confirm_password:
            raise forms.ValidationError("Password and Confirm Password must match")
        else:
            return data

class GuestForm(forms.Form):
    # add widgets and its attrs
    username = forms.CharField(widget=forms.TextInput(
        attrs={
            "class": "form-control",
            "placeholder": "Email Address",
            "required": "required",
        }
    )
    )



class LoginForm(forms.Form):
    # add widgets and its attrs
    username = forms.CharField(widget=forms.TextInput(
        attrs={
            "class": "form-control",
            "placeholder": "Email Address",
            "required": "required",
        }
    )
    )
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            "class": "form-control",
            "required": "required",
            "placeholder": "Enter Password",
        }
    )
    )
