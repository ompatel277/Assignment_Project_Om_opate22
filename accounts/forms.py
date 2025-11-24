# accounts/forms.py
from django import forms
from django.contrib.auth.models import User
from .models import UserProfile


# =====================================================
#  USER AUTHENTICATION FORMS
# =====================================================

class SignupForm(forms.ModelForm):
    """
    Handles user registration using Django's built-in User model.
    Includes password hashing and email validation.
    """
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        label="Password",
    )

    class Meta:
        model = User
        fields = ["username", "email", "password"]
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
        }

    def clean_email(self):
        """
        Ensure email uniqueness (case-insensitive).
        """
        email = self.cleaned_data.get("email")
        if email and User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email.lower() if email else email

    def save(self, commit=True):
        """
        Hash the password and save the new user instance.
        """
        user = super().save(commit=False)
        user.username = user.username.lower()
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    """
    Simple login form for username/password authentication.
    """
    username = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"}),
        label="Username",
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        label="Password",
    )


# =====================================================
#  USER PROFILE FORM (Academic & Career Preferences)
# =====================================================

class UserProfileForm(forms.ModelForm):
    """
    Form for creating and editing user profile data.
    Integrates academic, career, and personal information.
    """
    class Meta:
        model = UserProfile
        fields = [
            "college", "major", "minors", "academic_year", "gpa",
            "personal_interests", "career_goals", "skills",
            "work_experience", "preferred_industries", "preferred_locations",
            "preferred_positions", "preferred_company",
            "clubs_interest", "clubs_user_is_a_part_of",
        ]

        # --- Input Styling ---
        widgets = {
            "college": forms.Select(attrs={"class": "form-select"}),
            "major": forms.Select(attrs={"class": "form-select"}),
            "minors": forms.SelectMultiple(attrs={"class": "form-select"}),
            "academic_year": forms.Select(attrs={"class": "form-select"}),

            "gpa": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01",
                    "min": "0",
                    "max": "4",
                    "placeholder": "e.g. 3.75",
                }
            ),

            # --- Text Areas (for descriptive fields) ---
            "personal_interests": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 2,
                    "maxlength": 300,
                    "placeholder": "e.g. AI, Web Dev, UI/UX",
                }
            ),
            "career_goals": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "maxlength": 500,
                    "placeholder": "Describe your career goals...",
                }
            ),
            "skills": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 2,
                    "maxlength": 300,
                    "placeholder": "List key skills...",
                }
            ),
            "work_experience": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "maxlength": 500,
                    "placeholder": "Internships, jobs, or projects...",
                }
            ),
            "preferred_industries": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 2,
                    "maxlength": 300,
                    "placeholder": "e.g. Tech, Healthcare, Finance",
                }
            ),
            "preferred_locations": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 2,
                    "maxlength": 300,
                    "placeholder": "e.g. New York, Remote",
                }
            ),
            "preferred_positions": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 2,
                    "maxlength": 300,
                    "placeholder": "e.g. Software Engineer, Data Analyst",
                }
            ),
            "preferred_company": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 2,
                    "maxlength": 300,
                    "placeholder": "e.g. Google, Tesla",
                }
            ),
            "clubs_interest": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 2,
                    "maxlength": 300,
                    "placeholder": "Clubs you’d like to join",
                }
            ),
            "clubs_user_is_a_part_of": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 2,
                    "maxlength": 300,
                    "placeholder": "Clubs you’re already in",
                }
            ),
        }

        # --- Help Texts for Key Fields ---
        help_texts = {
            "college": "Select your current college.",
            "major": "Choose your main field of study.",
            "academic_year": "For example: Freshman, Sophomore, etc.",
            "gpa": "Enter your cumulative GPA on a 4.0 scale.",
        }
