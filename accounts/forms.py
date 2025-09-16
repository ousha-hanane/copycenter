from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(label="Prénom", max_length=30, required=True)
    last_name = forms.CharField(label="Nom", max_length=30, required=True)
    email = forms.EmailField(label="Email", required=True)

    # 🔹 Nouveau champ rôle
    ROLE_CHOICES = [
        ("Professeur", "Professeur"),
        ("Administratif", "Administratif"),
    ]
    role = forms.ChoiceField(choices=ROLE_CHOICES, required=True, label="Rôle")

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password1", "password2", "role"]
