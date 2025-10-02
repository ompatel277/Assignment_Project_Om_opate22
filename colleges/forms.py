from django import forms
from .models import College, Major

class CollegeForm(forms.ModelForm):
    class Meta:
        model = College
        fields = ["college_name", "city", "state", "abbreviation", "logo_url"]
        widgets = {
            "college_name": forms.TextInput(attrs={"class": "form-control"}),
            "city": forms.TextInput(attrs={"class": "form-control"}),
            "state": forms.TextInput(attrs={"class": "form-control"}),
            "abbreviation": forms.TextInput(attrs={"class": "form-control"}),
            "logo_url": forms.URLInput(attrs={"class": "form-control"}),
        }

class MajorForm(forms.ModelForm):
    class Meta:
        model = Major
        fields = ["college", "name", "code"]
        widgets = {
            "college": forms.Select(attrs={"class": "form-select"}),
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "code": forms.TextInput(attrs={"class": "form-control"}),
        }
