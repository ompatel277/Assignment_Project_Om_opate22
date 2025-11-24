# ============================================================
# A8: Forms, GET vs POST, and Function/Class-Based Views
# ============================================================
# This file now demonstrates:
#  - GET (search/filter) form: CollegeSearchForm
#  - POST (create/submit) form: MajorForm (ModelForm)
#  - Example of field-level validation using clean_<field>()
#
# These forms are still fully functional inside Traject.
# ============================================================

from django import forms
from .models import College, Major


# ------------------------------------------------------------
# Existing ModelForm for College (kept as-is for Traject)
# ------------------------------------------------------------
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


# ------------------------------------------------------------
# Modified ModelForm for Major (POST example for A8)
# ------------------------------------------------------------
class MajorForm(forms.ModelForm):
    """
    Form for creating or updating Major instances.
    Demonstrates POST method with CSRF protection and
    field-level validation (clean_code).
    """

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

    # Field-level validation (A8 requirement)
    def clean_code(self):
        code = self.cleaned_data.get("code", "").strip()
        if not code.isalpha():
            raise forms.ValidationError("Major code must contain only letters (e.g. CS, EE).")
        if len(code) < 2:
            raise forms.ValidationError("Major code must be at least 2 characters long.")
        return code.upper()


# ------------------------------------------------------------
# NEW: CollegeSearchForm (GET example for A8)
# ------------------------------------------------------------
class CollegeSearchForm(forms.Form):
    """
    Simple GET-based form for searching Colleges by name or abbreviation.
    Demonstrates how GET method passes data through the URL (?q=...).
    """

    q = forms.CharField(
        label="Search Colleges",
        required=False,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Search by college name or abbreviation..."
        })
    )
