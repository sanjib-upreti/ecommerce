from django import forms
from django.contrib.auth import get_user_model
from django.forms import DateInput


User = get_user_model()





class ContactForm(forms.Form):
    # add widgets and its attrs
    name = forms.CharField(widget=forms.TextInput(
        attrs={
            "class": "form-control",
            "placeholder": "Full Name",
            "required": "required",
        }
    )
    )
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={
            "class": "form-control",
            "required": "required",
            "placeholder": "Enter Email",
        }
    )
    )
    mobile = forms.CharField(widget=forms.TextInput(
        attrs={
            "class": "form-control",
            "placeholder": "Enter Mobile Number",
            "min_length": 10,
            "required": "required",

        }
    )
    )
    message = forms.CharField(widget=forms.Textarea(attrs={
        "class": "form-control",
        "placeholder": "Enter Your Message",
        "required": "required",
    }
    )
    )



class RegisterForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(
        attrs={
            "class": "form-control",
            "required": "required",
            "placeholder": "Enter Full Name",
        }
    )
    )
    # add widgets and its attrs

    email = forms.EmailField(widget=forms.EmailInput(
        attrs={
            "class": "form-control",
            "required": "required",
            "placeholder": "Enter Email",
        }
    )
    )
    username = forms.CharField(widget=forms.TextInput(
        attrs={
            "class": "form-control",
            "placeholder": "User Name",
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
    confirm_password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            "class": "form-control",
            "required": "required",
            "placeholder": "Confirm Password",
        }
    )
    )

    def clean(self):
        data = self.cleaned_data
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")
        if password != confirm_password:
            raise forms.ValidationError("Password and Confirm Password must match")
        else:
            return data

    def clean_username(self):
        username = self.cleaned_data.get("username")
        qs = User.objects.filter(username=username)
        if qs.exists():
            raise forms.ValidationError("Username already Exist")
        else:
            return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("Email already Exist")
        else:
            return email



