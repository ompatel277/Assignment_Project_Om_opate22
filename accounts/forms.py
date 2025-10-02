from django import forms
from django.contrib.auth.models import User
from .models import UserProfile


# Signup Form
class SignupForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = User
        fields = ["username", "email", "password"]
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])  # ensures hashing
        if commit:
            user.save()
        return user


# Login Form
class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))


# Profile Form
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            "college", "major", "gpa", "academic_year",
            "personal_interests", "career_goals",
            "skills", "work_experience",
            "preferred_industries", "preferred_locations",
            "preferred_positions", "preferred_skills",
            "preferred_title", "preferred_company",
        ]
        widgets = {
            "college": forms.Select(attrs={"class": "form-select"}),
            "major": forms.Select(attrs={"class": "form-select"}),
            "gpa": forms.NumberInput(attrs={"class": "form-control", "step": "0.01", "min": "0", "max": "4"}),
            "academic_year": forms.Select(attrs={"class": "form-select"}),
            "personal_interests": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
            "career_goals": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "skills": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
            "work_experience": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "preferred_industries": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
            "preferred_locations": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
            "preferred_positions": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
            "preferred_skills": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
            "preferred_title": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
            "preferred_company": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
        }
