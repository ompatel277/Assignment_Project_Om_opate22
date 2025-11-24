from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class TrajectSignUpForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        help_text="We'll use this email for account recovery and notifications."
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.is_staff = False
        user.is_superuser = False
        if commit:
            user.save()
        return user