from django import forms





class ReviewForm(forms.Form):
    # add widgets and its attrs
    reviewby = forms.EmailField(widget=forms.EmailInput(
        attrs={
            "class": "form-control",
            "required": "required",
            "placeholder": "Enter Email",
            "readonly":"readonly",
        }
    )
    )
    description = forms.CharField(widget=forms.Textarea(attrs={
        "class": "form-control",
        "placeholder": "Write Your Review",
        "required": "required",
    }
    )
    )
    productid = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control",
        "readonly":"readonly",
        "required": "required",
        "type":"hidden",
    }
    )
    )