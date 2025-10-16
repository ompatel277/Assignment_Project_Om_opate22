from django import forms
from .models import College, Major


class CollegeForm(forms.ModelForm):
    """Form for creating or updating College instances."""

    class Meta:
        model = College
        fields = ["college_name", "city", "state", "abbreviation", "logo_url"]
        widgets = {
            "college_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "e.g. University of Illinois"
            }),
            "city": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "City"
            }),
            "state": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "State"
            }),
            "abbreviation": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "e.g. UIUC"
            }),
            "logo_url": forms.URLInput(attrs={
                "class": "form-control",
                "placeholder": "Optional logo URL"
            }),
        }


class MajorForm(forms.ModelForm):
    """Form for creating or updating Major instances."""

    class Meta:
        model = Major
        fields = ["college", "name", "code"]
        widgets = {
            "college": forms.Select(attrs={"class": "form-select"}),
            "name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "e.g. Computer Science"
            }),
            "code": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "e.g. CS"
            }),
        }
